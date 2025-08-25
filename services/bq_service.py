import os
from google.cloud import bigquery
from google.oauth2 import service_account
import streamlit as st

# The path is read from the GOOGLE_APPLICATION_CREDENTIALS environment variable
credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

if credentials_path:
    # If the variable is set, use the path to the credentials
    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    client = bigquery.Client(credentials=credentials)
else:
    # If not, the client will try to find the credentials automatically.
    # This may work if gcloud auth login was used.
    client = bigquery.Client()

def get_marketing_clusters(table_project_id: str, dataset_id: str, table_id: str):
    """
    Gets the list of clusters from a specific table in BigQuery.

    Args:
        table_project_id: ID of the project in Google Cloud.
        dataset_id: ID of the dataset in BigQuery.
        table_id: ID of the table containing the clusters column.

    Returns:
        A list of strings with the cluster names, or an empty list in case of error.
    """
    try:
        query = f"""
            SELECT *
            FROM `{table_project_id}.{dataset_id}.{table_id}`
            ORDER BY cluster_id
        """
        query_job = client.query(query)
        
        # Converte cada linha do resultado em um dicionário para garantir o tipo de dado correto
        rows = [dict(row) for row in query_job.result()]
        return rows

    except Exception as e:
        st.error(f"Erro ao buscar clusters do BigQuery: {e}")
        # Retorna uma lista vazia em caso de erro
        return []