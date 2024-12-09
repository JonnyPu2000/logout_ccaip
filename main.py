import os
from dotenv import load_dotenv
from getTeams import get_assignees_ids
from postLogout import force_logout

# Carregar variáveis de ambiente
load_dotenv()

# Configurações
BASE_URL = os.getenv('BASE_URL')
TOKEN = os.getenv('TOKEN')
TEAM_IDS = [8,9,10]

def main():
    # Passo 1: Coletar os IDs dos assignees
    assignees_ids = get_assignees_ids(BASE_URL, TOKEN, TEAM_IDS)
    print("IDs coletados dos assignees:", assignees_ids)

    #Passo 2: Realizar o POST para forçar logout
    # force_logout(BASE_URL, TOKEN, assignees_ids)

if __name__ == "__main__":
    main()
