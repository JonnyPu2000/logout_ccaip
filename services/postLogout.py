# services/postLogout.py
import requests

def force_logout(base_url, token, agent_ids):
    if not agent_ids:
        print("Nenhum ID de assignee encontrado. POST não enviado.")
        return

    url = f"{base_url}/apps/api/v1/agent_statuses/force_logout"
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    payload = {
        "agent_ids": agent_ids
    }

    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        print("Logout forçado realizado com sucesso.")
        print("Resposta:", response.json())
    else:
        print(f"Erro ao realizar logout: {response.status_code} - {response.text}")
