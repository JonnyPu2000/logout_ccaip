import tkinter as tk
from tkinter import ttk, messagebox
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

def criar_tabela_para_time(frame, team_name, assignees, status_data):
    table_frame = ttk.Frame(frame)
    table_frame.pack(fill=tk.BOTH, padx=10, pady=5)

    table_label = ttk.Label(table_frame, text=f"Time: {team_name}")
    table_label.pack(anchor="w", pady=5)

    treeview = ttk.Treeview(table_frame, columns=("ID", "Nome", "Status", "Tempo no status"), show="headings", height=6)
    treeview.pack(fill=tk.BOTH, expand=True)

    treeview.heading("ID", text="ID")
    treeview.heading("Nome", text="Nome")
    treeview.heading("Status", text="Status")
    treeview.heading("Tempo no status", text="Tempo no status")

    treeview.column("ID", width=50)
    treeview.column("Nome", width=150)
    treeview.column("Status", width=100)
    treeview.column("Tempo no status", width=150)

    for assignee in assignees:
        agent_status = next((item for item in status_data if item['id'] == assignee['id']), None)
        if agent_status:
            status = agent_status['status']
            last_updated = agent_status['status_updated_at']
            tempo_inaatividade = calcular_tempo_inaatividade(last_updated)
            treeview.insert("", "end", values=(assignee['id'], assignee['name'], status, tempo_inaatividade))

    return treeview

def coletar_ids_e_exibir_tabelas(selected_team_ids, frame_principal):
    try:
        assignees_data = get_team_assignees(BASE_URL, TOKEN, selected_team_ids)
        status_data = obter_status_agentes()

        if not status_data:
            return "Erro ao obter os status dos agentes."

        for team_id, team_data in assignees_data.items():
            team_name = team_data['name']
            assignees = team_data['assignees']
            criar_tabela_para_time(frame_principal, team_name, assignees, status_data)

    except Exception as e:
        return f"Erro ao coletar e exibir os dados: {e}"

def forcar_logout(selected_team_ids):
    try:
        assignees_data = get_team_assignees(BASE_URL, TOKEN, selected_team_ids)
        assignees_ids = [assignee['id'] for team_data in assignees_data.values() for assignee in team_data['assignees']]
        status_data = obter_status_agentes()

        if not status_data:
            messagebox.showerror("Erro", "Não foi possível obter os status dos agentes.")
            return "Erro ao obter os status dos agentes."

        logout_success = False  # Flag para controlar o sucesso do logout

        for agent_id in assignees_ids:
            agent_status = next((item for item in status_data if item['id'] == agent_id), None)
            if agent_status:
                status = agent_status.get("status", "")
                last_updated = agent_status.get("status_updated_at", "")
                tempo_inaatividade = calcular_tempo_inaatividade(last_updated)

                # Verificando se o status é diferente de "Available" e se está há mais de 3 horas no mesmo status
                if status != "Available" and (datetime.utcnow() - datetime.strptime(last_updated, "%Y-%m-%dT%H:%M:%S.%fZ")) > timedelta(hours=3):
                    force_logout(BASE_URL, TOKEN, [agent_id])
                    logout_success = True
                    messagebox.showinfo("Logout", f"Logout bem-sucedido para o agente ID {agent_id}.")
                else:
                    # Se não for possível forçar logout, mostramos o motivo
                    messagebox.showinfo("Logout Não Realizado", f"O agente ID {agent_id} não atingiu os critérios para logout.")
        
        if not logout_success:
            messagebox.showinfo("Logout", "Nenhum agente foi desconectado, pois não atendem aos critérios.")
        
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao realizar logout: {e}")
        return f"Erro ao realizar logout: {e}"

def criar_interface():
    janela = tk.Tk()
    janela.title("Gerenciador de Assignees")
    janela.geometry("800x600")

    frame_principal = ttk.Frame(janela)
    frame_principal.pack(fill=tk.BOTH, expand=True)

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

    btn_coletar_ids = ttk.Button(frame_botoes, text="Coletar IDs e Nomes", command=lambda: coletar_ids_e_exibir_tabelas(obter_times_selecionados(), frame_principal))
    btn_coletar_ids.pack(side=tk.LEFT, padx=10)

    btn_forcar_logout = ttk.Button(frame_botoes, text="Forçar Logout", command=lambda: forcar_logout(obter_times_selecionados()))
    btn_forcar_logout.pack(side=tk.LEFT, padx=10)

    janela.mainloop()
