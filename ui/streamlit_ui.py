# --------------------------------------------------------------------------
# Streamlit User Interface Setup
# --------------------------------------------------------------------------

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

print("sys.path após a modificação:")
for p in sys.path:
    print(f"  - {p}")

import os
import logging
import pandas as pd
from datetime import datetime, timezone, time
import streamlit as st # type: ignore
from services.bq_service import get_marketing_clusters # type: ignore
from services.gemini_service import suggest_campaign_from_cluster
from config.settings import MODEL_GEMINI, get_api_key

from dotenv import load_dotenv
load_dotenv()


# --------------------------------------------------------------------------
# Support Functions
# --------------------------------------------------------------------------

# Use this function to handle the Timestamp conversion
def convert_timestamp_to_days_ago(timestamp):
    # Get the current time with the same timezone information as the timestamp
    now = datetime.now(timezone.utc)
    # Calculate the time difference and return the number of days
    if pd.isna(timestamp):
        return 0  # Handle potential missing values
    return (now - timestamp).days

@st.cache_data
def load_and_prepare_data():
    BQ_TABLE_PROJECT_ID = 'BQ_TABLE_PROJECT_ID'
    BQ_DATASET_ID = 'BQ_DATASET_ID'
    BQ_TABLE_ID = 'BQ_TABLE_ID'
    
    all_cluster_rows = get_marketing_clusters(BQ_TABLE_PROJECT_ID, BQ_DATASET_ID, BQ_TABLE_ID)
    
    if not all_cluster_rows:
        return pd.DataFrame(), []
    
    df = pd.DataFrame(all_cluster_rows)
    print(df)
    
    # Check if the 'last_access' column exists before processing
    if 'last_access' in df.columns:
        # Convert the timestamp column to a timedelta representing days since last access
        df['last_access'] = df['last_access'].apply(convert_timestamp_to_days_ago)
        
    # Return the processed DataFrame and the list of cluster IDs
    return df, df['cluster_id'].tolist()

# --------------------------------------------------------------------------
# Streamlit UI
# --------------------------------------------------------------------------

st.set_page_config(
    page_title = "Copiloto Marketing",
    layout = "wide", # Use wide layout for more space
    initial_sidebar_state = "auto" # Keep sidebar visible initially
)

st.title("🎯 Marketing Assistant (Powered by ADK & Gemini)")
st.markdown("""
Interact with an AI agent that can fetch marketing insights.
*   Choose a `cluster` to get a campaign idea.
""")
st.divider() # Add a visual separator
# --- API Key Availability Check ---
# Verify that the GEMINI_API_KEY is loaded and not the placeholder value.
api_key = get_api_key()
if not api_key:
    st.error(
        "🚨 **Action Required: Gemini API Key Not Found or Invalid!** 🚨\n\n"
        "1. Create a file named `.env` in the same directory as `news_app.py`.\n"
        "2. Add the following line to the `.env` file:\n"
        "   `GEMINI_API_KEY='YOUR_ACTUAL_GEMINI_API_KEY'`\n"
        "3. Replace `YOUR_ACTUAL_GEMINI_API_KEY` with your valid key from Google AI Studio.\n"
        "4. **Restart the Streamlit application.**",
        icon="🔥"
    )
    st.stop() # Halt further execution if the key is missing or invalid

# Initialize the session state for filters
if "filter_state" not in st.session_state:
    st.session_state.filter_state = {
        "content_interest": [],
        "location": [],
        "previous_engagement": [],
        "is_subscriber": [],
        "device_type": [],
        "access_time_range": None,
        "daily_minutes_range": None,
        "age": []
    }
    
st.subheader("💡 Selecione um Cluster de Marketing")

# Reset button. It must be placed BEFORE the filter widgets.
if st.button("Resetar Filtros", key="reset_button"):
    st.session_state.filter_state = {
        "content_interest": [],
        "location": [],
        "previous_engagement": [],
        "is_subscriber": [],
        "device_type": [],
        "access_time_range": None,
        "daily_minutes_range": None,
        "age": []
    }
    st.rerun()

all_df, cluster_ids_for_selectbox = load_and_prepare_data()

if all_df.empty:
    st.warning("⚠️ Não foi possível carregar os clusters do BigQuery.", icon="🚨")
else:
    # Create columns for the filters
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    # 1. Filter Widgets
    with col1:
        options = all_df['content_interest'].unique().tolist()
        selected_options = st.multiselect(
            "Interesse",
            options=options,
            default=st.session_state.filter_state.get("content_interest", [])
        )
        st.session_state.filter_state["content_interest"] = selected_options
    
    with col2:
        options = all_df['location'].unique().tolist()
        selected_options = st.multiselect(
            "Localização",
            options=options,
            default=st.session_state.filter_state.get("location", [])
        )
        st.session_state.filter_state["location"] = selected_options
    
    with col3:
        options = all_df['previous_engagement'].unique().tolist()
        selected_options = st.multiselect(
            "Engajamento Anterior",
            options=options,
            default=st.session_state.filter_state.get("previous_engagement", [])
        )
        st.session_state.filter_state["previous_engagement"] = selected_options
    
    with col4:
        options = all_df['is_subscriber'].unique().tolist()
        selected_options = st.multiselect(
            "É Assinante",
            options=options,
            default=st.session_state.filter_state.get("is_subscriber", [])
        )
        st.session_state.filter_state["is_subscriber"] = selected_options
        
    with col5:
        options = all_df['device_type'].unique().tolist()
        selected_options = st.multiselect(
            "Tipo de Dispositivo",
            options=options,
            default=st.session_state.filter_state.get("device_type", [])
        )
        st.session_state.filter_state["device_type"] = selected_options

    with col6:
        options = all_df['age'].unique().tolist()
        selected_options = st.multiselect(
            "Idade",
            options=options,
            default=st.session_state.filter_state.get("age", [])
        )
        st.session_state.filter_state["age"] = selected_options


    # 2. Apply the filters to the DataFrame
    filtered_df = all_df.copy()

    # Apply filters only if the list of selected options is not empty
    if st.session_state.filter_state["content_interest"]:
        filtered_df = filtered_df[filtered_df['content_interest'].isin(st.session_state.filter_state["content_interest"])]
    
    if st.session_state.filter_state["location"]:
        filtered_df = filtered_df[filtered_df['location'].isin(st.session_state.filter_state["location"])]
        
    if st.session_state.filter_state["previous_engagement"]:
        filtered_df = filtered_df[filtered_df['previous_engagement'].isin(st.session_state.filter_state["previous_engagement"])]

    if st.session_state.filter_state["is_subscriber"]:
        filtered_df = filtered_df[filtered_df['is_subscriber'].isin(st.session_state.filter_state["is_subscriber"])]
        
    if st.session_state.filter_state["device_type"]:
        filtered_df = filtered_df[filtered_df['device_type'].isin(st.session_state.filter_state["device_type"])]

    if st.session_state.filter_state["age"]:
        filtered_df = filtered_df[filtered_df['age'].isin(st.session_state.filter_state["age"])]

    # 3. Display the filtered table
    st.markdown("<br>", unsafe_allow_html = True)
    st.markdown("##### 📊 Dados dos Clusters Filtrados")
    st.dataframe(filtered_df, use_container_width=True)
    st.markdown("<br>", unsafe_allow_html = True)

    # Allow user to select cluster
    cluster_ids_for_filtered_selectbox = filtered_df['cluster_id'].unique().tolist()
    
    if not cluster_ids_for_filtered_selectbox:
        st.warning("Nenhum cluster encontrado com os filtros selecionados.")
        selected_cluster_id = None
    else:
        cluster_ids_for_filtered_selectbox.insert(0, "Selecione um cluster")
        selected_cluster_id = st.selectbox("Escolha um cluster para obter informações detalhadas:", cluster_ids_for_filtered_selectbox, index=0)
    
    if selected_cluster_id and selected_cluster_id != "Selecione um cluster":
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Additional notes field appears here after cluster selection
        st.markdown("### 📝 Objetivo de negócio/campanha")
        additional_notes = st.text_area("Adicione o objetivo de negócio ou campanha para este cluster:", value=st.session_state.filter_state.get("additional_notes", ""), key="additional_notes_input")
        st.session_state.filter_state["additional_notes"] = additional_notes

        cluster_details = filtered_df[filtered_df['cluster_id'] == selected_cluster_id].iloc[0]
        cluster_details_dict = cluster_details.to_dict()
        
        for key, value in cluster_details_dict.items():
            if isinstance(value, time):
                cluster_details_dict[key] = value.strftime('%H:%M:%S')

        cluster_details_dict["additional_notes"] = st.session_state.filter_state.get("additional_notes", "")
        
        st.markdown(f"### ✨ Dados de Entrada para o Gemini do Cluster `{selected_cluster_id}`")
        st.json(cluster_details_dict)
        
        if st.button("Gerar Sugestão de Campanha com Gemini", key="generate_button"):
            with st.spinner("Gerando sugestão de campanha... (isso pode levar alguns segundos)"):
                try:
                    # Pass the API key explicitly
                    gemini_api_key = os.environ.get('GEMINI_API_KEY')
                    if not gemini_api_key:
                        st.error("Erro: A chave da API do Gemini não foi encontrada. Verifique sua configuração.")
                        st.stop()
                    
                    campaign_suggestion = suggest_campaign_from_cluster(
                        cluster_details_dict,
                        st.session_state.filter_state.get("additional_notes", ""),
                        api_key=gemini_api_key
                    )
                    st.success("Sugestão de campanha gerada com sucesso!")
                    st.markdown("### 🤖 Resposta do Gemini")
                    st.json(campaign_suggestion)
                except Exception as e:
                    st.error(f"Ocorreu um erro ao chamar o Gemini: {e}")
                    st.exception(e)

# --- Sidebar Information Display ---
st.sidebar.divider()
st.sidebar.header("Detalhes do Assistente")
st.sidebar.caption(f"**LLM:** `{MODEL_GEMINI}`")
st.sidebar.caption("Powered by Google Agent Development Kit.")

print("✅ Renderização da UI do Streamlit completa.")