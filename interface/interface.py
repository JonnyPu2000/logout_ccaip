# interface/interface.py
import tkinter as tk
from tkinter import ttk
from services.getTeams import get_team_assignees
from services.postLogout import force_logout
from config.config import BASE_URL, TOKEN, TEAM_IDS
from datetime import datetime, timedelta
import requests

def coletar_nomes_times():
    try:
        assignees_data = get_team_assignees(BASE_URL, TOKEN, TEAM_IDS)
        return {team_id: team_data['name'] for team_id, team_data in assignees_data.items()}
    except Exception as e:
        return f"Erro ao coletar nomes dos times: {e}"

def obter_status_agentes():
    url = f"{BASE_URL}/manager/api/v1/agents/current_status"
    headers = {'Authorization': TOKEN}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar status dos agentes: {e}")
        return None

def calcular_tempo_inaatividade(status_time_str):
    try:
        status_time = datetime.strptime(status_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        delta = datetime.utcnow() - status_time
        return str(delta).split('.')[0]  # Exibe o tempo sem os microssegundos
    except Exception as e:
        return f"Erro ao calcular o tempo: {e}"

def coletar_ids(text_widget, selected_team_ids):
    try:
        assignees_data = get_team_assignees(BASE_URL, TOKEN, selected_team_ids)
        status_data = obter_status_agentes()

        if not status_data:
            text_widget.config(state=tk.NORMAL)
            text_widget.insert(tk.END, "Erro ao obter os status dos agentes.\n")
            text_widget.config(state=tk.DISABLED)
            return

        resultado = "Assignees organizados por time:\n"
        for team_id, team_data in sorted(assignees_data.items()):
            team_name = team_data['name']
            assignees = team_data['assignees']
            resultado += f"\n{team_name}:\n"
            for assignee in sorted(assignees, key=lambda x: x['id']):
                agent_status = next((item for item in status_data if item['id'] == assignee['id']), None)
                if agent_status:
                    status = agent_status['status']
                    last_updated = agent_status['status_updated_at']
                    tempo_inaatividade = calcular_tempo_inaatividade(last_updated)
                    resultado += f"  ID: {assignee['id']} - Nome: {assignee['name']} - Status: {status} - Tempo no status: {tempo_inaatividade}\n"
        
        text_widget.config(state=tk.NORMAL)
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, resultado)
        text_widget.config(state=tk.DISABLED)
    except Exception as e:
        text_widget.config(state=tk.NORMAL)
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, f"Erro ao coletar IDs: {e}")
        text_widget.config(state=tk.DISABLED)

def forcar_logout(text_widget, selected_team_ids):
    try:
        assignees_data = get_team_assignees(BASE_URL, TOKEN, selected_team_ids)
        assignees_ids = [assignee['id'] for team_data in assignees_data.values() for assignee in team_data['assignees']]
        status_data = obter_status_agentes()

        if not status_data:
            text_widget.config(state=tk.NORMAL)
            text_widget.insert(tk.END, "Erro ao obter os status dos agentes.\n")
            text_widget.config(state=tk.DISABLED)
            return

        for agent_id in assignees_ids:
            agent_status = next((item for item in status_data if item['id'] == agent_id), None)
            if agent_status:
                status = agent_status.get("status", "")
                last_updated = agent_status.get("status_updated_at", "")
                tempo_inaatividade = calcular_tempo_inaatividade(last_updated)

                text_widget.config(state=tk.NORMAL)
                text_widget.insert(tk.END, f"Agente {agent_id} - Status: {status} (Última atualização: {last_updated} - Tempo no status: {tempo_inaatividade})\n")
                text_widget.config(state=tk.DISABLED)

                if status != "Available" or (status == "Available" and datetime.utcnow() - datetime.strptime(last_updated, "%Y-%m-%dT%H:%M:%S.%fZ") > timedelta(hours=3)):
                    force_logout(BASE_URL, TOKEN, [agent_id])
                    text_widget.config(state=tk.NORMAL)
                    text_widget.insert(tk.END, f"Logout forçado realizado para o agente {agent_id} ({status}).\n")
                    text_widget.config(state=tk.DISABLED)
                else:
                    text_widget.config(state=tk.NORMAL)
                    text_widget.insert(tk.END, f"Agente {agent_id} está disponível e foi atualizado recentemente. Nenhum logout necessário.\n")
                    text_widget.config(state=tk.DISABLED)

    except Exception as e:
        text_widget.config(state=tk.NORMAL)
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, f"Erro ao realizar logout: {e}")
        text_widget.config(state=tk.DISABLED)

def criar_interface():
    janela = tk.Tk()
    janela.title("Gerenciador de Assignees")
    janela.geometry("700x600")

    frame_principal = ttk.Frame(janela)
    frame_principal.pack(fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(frame_principal, orient=tk.VERTICAL)
    text_widget = tk.Text(frame_principal, wrap=tk.WORD, yscrollcommand=scrollbar.set, width=90, height=20)
    scrollbar.config(command=text_widget.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    text_widget.config(state=tk.DISABLED)

    team_names = coletar_nomes_times()

    frame_checkboxes = ttk.Frame(janela)
    frame_checkboxes.pack(pady=10)

    team_checkboxes = {}
    for team_id, team_name in team_names.items():
        var = tk.BooleanVar()
        checkbox = tk.Checkbutton(frame_checkboxes, text=team_name, variable=var)
        checkbox.pack(anchor='w')
        team_checkboxes[team_id] = var

    def obter_times_selecionados():
        selected_team_ids = [team_id for team_id, var in team_checkboxes.items() if var.get()]
        return selected_team_ids

    frame_botoes = ttk.Frame(janela)
    frame_botoes.pack(pady=10)

    btn_coletar_ids = ttk.Button(frame_botoes, text="Coletar IDs e Nomes", command=lambda: coletar_ids(text_widget, obter_times_selecionados()))
    btn_coletar_ids.pack(side=tk.LEFT, padx=10)

    btn_forcar_logout = ttk.Button(frame_botoes, text="Forçar Logout", command=lambda: forcar_logout(text_widget, obter_times_selecionados()))
    btn_forcar_logout.pack(side=tk.LEFT, padx=10)

    janela.mainloop()
