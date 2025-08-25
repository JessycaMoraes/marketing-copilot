# 🎯 Copiloto de Marketing Personalizado

Um **Assistente de Marketing com IA** que ajuda profissionais a criarem campanhas digitais personalizadas em múltiplos canais (push, email, notificações, etc.), desenvolvido com **Streamlit + Python** e impulsionado pelo **Gemini 2.5-pro**.  

Este projeto foi desenvolvido durante o **Hackday 2025 da Globo**, em colaboração com **Laura Muller, Bruno Farias, Ighor Miranda e Leonardo Belchior**.  

---

## 👤 Perfil do Usuário

Profissionais de marketing responsáveis por campanhas digitais em múltiplos canais (push, email, redes sociais) para produtos como **streaming, portais de conteúdo, entretenimento e receitas**.  

---

## 🚀 Jornada do Usuário

### 1. Acesso à Ferramenta
- O usuário acessa o **painel do Copiloto de Marketing** pelo navegador.  
- A interface foi criada em **Streamlit**.  
- Os **clusters comportamentais** são exibidos com base em dados simulados do **BigQuery**.  

📊 **Exemplo de clusters**:  
- Cluster 1: Jovens esportistas (alto tráfego, não assinantes)  
- Cluster 2: Fãs de receitas que acessam à noite  
- Cluster 3: Ex-assinantes com reengajamento recente  

---

### 2. Exploração de Perfis
- O usuário seleciona um **cluster**.  
- Adiciona um **objetivo de negócio** (ex.: *"Quero divulgar a cobertura da COP30"*).  

---

### 3. Geração de Campanha
Com **um clique**, o usuário solicita ao agente de IA (Gemini) uma campanha personalizada contendo:  
- Texto sugerido da mensagem  
- Canal ideal  
- Melhor horário de envio  
- Oferta recomendada  
- Estimativa de engajamento (probabilidade de cliques/visualizações)    

🧠 **Exemplo de resposta da IA**:  
- **Mensagem**: "Já escolheu o prato do dia? Assista agora à nossa série culinária exclusiva que está dando o que falar."  
- **Canal**: Push Notification  
- **Horário**: 20h  
- **Oferta**: Episódio bônus exclusivo  
- **Estimativa de engajamento**: 32% CTR    

---

## 📌 Questões de Negócio Respondidas pelo Agente
- Como personalizar campanhas para aumentar o **engajamento** em diferentes clusters?  
- Qual é o **melhor canal** para cada perfil (push, email, social)?  
- Qual é o **horário ideal** para maximizar cliques e visualizações?  
- Como criar estratégias diferentes para **assinantes vs. não assinantes**?  
- Qual é a **oferta mais relevante** (teste grátis, episódio bônus, desconto)?  

---

## 🛠️ Stack Tecnológica
- **Python**  
- **Streamlit** (interface web)  
- **BigQuery** (dataset simulado)  
- **Gemini 2.5-pro** (geração de campanhas personalizadas com IA)  

---

## 🗄️ Dataset Fake no BigQuery

O dataset foi gerado via SQL, produzindo:  
- **10.000 linhas simuladas**  
- **10.000 clusters distintos** (cada um com um `cluster_id` único)  
- Atributos de usuário incluindo:  
  - `content_interest` (esportes, receitas, notícias)  
  - `device_type` (mobile, smart_tv, web)  
  - `previous_engagement` (push, email, etc.)  
  - `is_subscriber` (assinante ou não)  
  - `last_access`, `access_time`, `avg_daily_minutes`, `location`, `age`  

---

## 📷 Demo

- Tela de seleção de clusters  
<img width="1920" height="1027" alt="image" src="https://github.com/user-attachments/assets/3db18d6f-294f-4003-b91a-89935c96bf6e" />

- Sugestão de campanha gerada por IA  
<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/c5221170-d06c-4ec9-906c-73888488bc6b" />

---

## 🙌 Agradecimentos

Desenvolvido durante o **Hackday 2025 da Globo** por:  

- Laura Muller  
- Bruno Farias  
- Ighor Miranda  
- Leonardo Belchior  
- Jessyca Moraes  
