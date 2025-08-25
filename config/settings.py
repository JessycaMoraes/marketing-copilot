# -*- coding: utf-8 -*-
"""
Configuration module for environment and global variables.
"""
import os
import logging
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Load environment variables from the .env file
logging.basicConfig(level=logging.ERROR)

# --------------------------------------------------------------------------
# Application Settings
# --------------------------------------------------------------------------

# Specifies the Gemini model to use for campaign suggestions.
MODEL_GEMINI = "gemini-2.5-pro"

# --------------------------------------------------------------------------
# Support Functions
# --------------------------------------------------------------------------
def get_api_key():
    """
    Retrieves the Google API Key from environment variables.
    Returns None if the key is not found or is the default.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key or "YOUR_GEMINI_API_KEY" in api_key:
        return None
    return api_key