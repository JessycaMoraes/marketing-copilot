# -*- coding: utf-8 -*-
"""
Service module for calling Gemini.
It defines the input and output schemas and the function that interacts with the API.
"""
import os
import json
from enum import Enum
from typing import List, Optional
import logging

import google.generativeai as genai
from pydantic import BaseModel, Field

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ------------------------------
#1) Define the exit CONTRACT
# ------------------------------
class Channel(str, Enum):
    EMAIL = "EMAIL"
    PUSH = "PUSH"

class Message(BaseModel):
    channel: Channel
    audience_notes: List[str] = Field(
        description="Notas sobre subalvos/segmentos dentro do cluster"
    )
    message: str
    cta: str
    preferred_send_window: str  # Ex.: "Tue 10:00-12:00 (America/Sao_Paulo)"
    kpis: List[str]  # Ex.: ["open_rate", "ctr", "conversion_rate"]

class CampaignSuggestion(BaseModel):
    campaign_title: str
    objective: str  # Ex.: "awareness" | "engagement" | "conversion" | "retention"
    rationale: str
    budget_hint: Optional[str] = None
    messages: List[Message]

# ---------------------------------
#2) System prompt (fixed rules)
# ---------------------------------
SYSTEM_INSTRUCTION = """
Você é um estrategista de marketing multicanal do Globoplay. Receberá um JSON:
{
  "rows": [
    {
      "cluster_id": "...",
      "access_time": "2025-08-20T19:08:00-03:00",
      "avg_time_day": 123.4,
      "interest": "noticias|esportes|receitas",
      "location": "cidade/região",
      "prev_engagement": "push|email",
      "subscriber": true|false,
      "last_access": "2025-08-20T19:17:00-03:00",
      "device_type": "mobile|desktop|tablet",
      "age": 18
    }, ...
  ],
  "tz": "America/Sao_Paulo"
}

OBJETIVO: para CADA item de 'rows', produza UMA campanha (não agrupar), preservando a ordem.

SAÍDA OBRIGATÓRIA:
Responda SOMENTE com JSON válido no schema:
{ "campanhas": [ { "mensagem": str, "canal": str, "horario": str, "oferta": str, "estimativa_engajamento": str }, ... ] }
- 'canal' deve ser EXATAMENTE "Push" ou "Email".
- 'horario' deve ser "HH:mm" (ex.: "12:45") OU uma janela curta (ex.: "10h ou 14h").
- 'estimativa_engajamento' deve ser uma string com percentual e, opcionalmente, comentário em parênteses (ex.: "2.3% (alto tempo de leitura)").

REGRAS POR CLUSTER:

1) MENSAGEM (copy curta e com CTA; usar a fórmula: [GANCHO específico] + [BENEFÍCIO] + [OFERTA] + [CTA curto])
   - Ajuste ao interesse:
     * esportes → chame "melhores momentos", "rodada", "ao vivo".
     * noticias → "análise exclusiva", "guia prático" (ex.: eleições).
     * receitas → "cardápio/coleção da semana", "lista de compras", "em X minutos".
   - Tom por idade:
     * 18–24: direto/energético (ex.: "Veja agora", "Corre").
     * 25–44: benefício prático + ação clara (ex.: "Entenda e comece hoje").
     * 45–64: credibilidade e clareza (ex.: "Análise exclusiva", "Guia prático").
     * 65+: simples e didático (ex.: "Passo a passo", "Acesso fácil").
   - Limites por canal:
     * Push: 60–90 caracteres, sem jargão.
     * Email (assunto/linha curta): 35–45 caracteres. (A mensagem deve caber como linha de assunto.)
   - Para noticias sensíveis (ex.: eleições), evite emoji e sensacionalismo; enfatize utilidade e serenidade.
   - Se subscriber = false e houver oferta, inclua-a na mensagem (ex.: "7 dias grátis", "24h premium").

2) CANAL (somente "Push" ou "Email")
   - Preferência por histórico:
     * Se prev_engagement = "push" → recomende "Push".
     * Se prev_engagement = "email" → recomende "Email".
   - Empate/ambiguidade: use device e idade como desempate:
     * mobile + 18–44 → favoreça "Push".
     * 45+ → favoreça "Email".
   - Nunca sugerir canais fora de "Push" ou "Email".

3) HORÁRIO
   - Base: use a hora de pico do cluster. Se a hora pico for H (derivada de 'access_time'), sugira "H:45".
   - Se não houver sinal claro, use:
     * 18–24 → "12:45" ou "20:45".
     * 25–44 → "12:45" ou "18:45".
     * 45–64 → "10:45" ou "14:45".
     * 65+ → "09:30" ou "10:45".
   - Se permanecer ambíguo, retorne uma janela: "10h ou 14h".

4) OFERTA
   - Não assinante → priorize "Teste gratuito", "Acesso por 24h a conteúdos premium", ou (para esportes) "7 dias grátis do streaming esportivo".
   - Assinante → priorize "conteúdo exclusivo", "série especial", "benefício de fidelidade".
   - Por interesse:
     * noticias (tema quente) → "Acesso gratuito por 24h a conteúdos premium".
     * esportes → "7 dias grátis do streaming esportivo".
     * receitas → "Coleção/ebook da semana" ou "cardápio da semana".


CONTRA-EXEMPLOS (NÃO FAZER):
- Não retornar texto fora do JSON especificado.
- Não usar canais diferentes de "Push" ou "Email".
- Não escrever mensagens longas, vagas ou sem CTA.
- Não invente dados PII e não compartilhe dados sensíveis, respeitando as normas da LGPD (Lei de Proteção de Dados Pessoais) conforme a constituição Brasileira.

NÃO incluir explicações fora do JSON.
"""

# ------------------------------------------------
# 3) Function that calls Gemini with Structured JSON
# ------------------------------------------------
def suggest_campaign_from_cluster(cluster_dict: dict, user_notes: str, api_key: str) -> dict:
    """
    Sends the cluster and user notes to Gemini and returns a validated dictionary.

    Args:
      cluster_dict (dict): Dictionary with cluster information.
      user_notes (str): Additional user notes about the campaign objective.
      api_key (str): The Gemini API key for authentication.

    Returns:
      dict: A dictionary with the campaign suggestion.
    """
    try:
        # Configure the API with the key passed as an argument.
        genai.configure(api_key=api_key)
        logger.info("Configuração da API do Gemini concluída.")

        # Attempt to initialize the model.
        model = genai.GenerativeModel("gemini-1.5-pro")
        logger.info("Modelo 'gemini-1.5-pro' carregado com sucesso.")
        
        user_prompt = (
            f"Instruções do sistema: {SYSTEM_INSTRUCTION}\n\n"
            "Com base no cluster e nas notas do usuário a seguir, proponha uma campanha coesa, "
            "com 1 a 3 mensagens por canal. "
            "Use janelas de envio compatíveis com a timezone do cluster. "
            f"Cluster JSON:\n{json.dumps(cluster_dict, ensure_ascii=False)}\n\n"
            f"Notas do usuário/Objetivo da Campanha:\n{user_notes}"
        )

        resp = model.generate_content(
            contents=user_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.5,
                response_mime_type="application/json"
            )
        )
        
        return resp.text
        return suggestion.model_dump()
        
    except Exception as e:
        logger.error(f"Ocorreu um erro ao chamar o Gemini: {e}")
        raise e