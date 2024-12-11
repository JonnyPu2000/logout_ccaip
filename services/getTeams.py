# services/getTeams.py
import requests

def get_team_assignees(base_url, token, team_ids):
    headers = {'Authorization': token}
    teams_data = {}
    
    for team_id in team_ids:
        response = requests.get(f"{base_url}/manager/api/v1/teams/{team_id}", headers=headers)
        response.raise_for_status()
        team_info = response.json()
        
        teams_data[team_id] = {
            "name": team_info["name"],  # Nome do time
            "assignees": [
                {"id": assignee["id"], "name": assignee["name"]} for assignee in team_info["assignees"]
            ]
        }
    
    return teams_data
