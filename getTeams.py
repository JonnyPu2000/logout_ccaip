import requests

def get_assignees_ids(base_url, token, team_ids):
    """
    Faz chamadas para as APIs de equipes e retorna uma lista com os IDs de todos os assignees.
    """
    headers = {
        'Authorization': token
    }
    all_assignees_ids = []

    for team_id in team_ids:
        url = f"{base_url}/manager/api/v1/teams/{team_id}"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            assignees = data.get('assignees', [])
            all_assignees_ids.extend([assignee['id'] for assignee in assignees])
        else:
            print(f"Erro ao chamar API para o team ID {team_id}: {response.status_code} - {response.text}")
    
    return all_assignees_ids
