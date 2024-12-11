# config/config.py
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

BASE_URL = os.getenv('BASE_URL')
TOKEN = os.getenv('TOKEN')
TEAM_IDS = [8, 9, 10]
