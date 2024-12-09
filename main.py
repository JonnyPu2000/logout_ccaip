import os
import tkinter as tk
from tkinter import ttk
from dotenv import load_dotenv
from getTeams import get_team_assignees
from postLogout import force_logout

# Carregar variáveis de ambiente
load_dotenv()

# Configurações
BASE_URL = os.getenv('BASE_URL')
TOKEN = os.getenv('TOKEN')
TEAM_IDS = [8, 9, 10]

# Função para coletar e exibir os IDs e nomes dos assignees, organizados por time
def coletar_ids(text_widget):
    try:
        # Coleta os dados dos assignees e organiza por time
        assignees_data = get_team_assignees(BASE_URL, TOKEN, TEAM_IDS)
        
        # Organiza a saída para exibição
        resultado = "Assignees organizados por time:\n"
        for team_id, team_data in sorted(assignees_data.items()):
            team_name = team_data['name']
            assignees = team_data['assignees']
            resultado += f"\n{team_name}:\n"
            for assignee in sorted(assignees, key=lambda x: x['id']):
                resultado += f"  ID: {assignee['id']} - Nome: {assignee['name']}\n"
        
        # Exibe o resultado no widget de texto
        text_widget.config(state=tk.NORMAL)
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, resultado)
        text_widget.config(state=tk.DISABLED)
    except Exception as e:
        text_widget.config(state=tk.NORMAL)
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, f"Erro ao coletar IDs: {e}")
        text_widget.config(state=tk.DISABLED)

# Função para realizar o POST e forçar logout
def forcar_logout(text_widget):
    try:
        # Coleta os IDs para realizar o logout
        assignees_data = get_team_assignees(BASE_URL, TOKEN, TEAM_IDS)
        assignees_ids = [assignee['id'] for team_data in assignees_data.values() for assignee in team_data['assignees']]
        
        # Envia a requisição de logout
        force_logout(BASE_URL, TOKEN, assignees_ids)
        
        # Atualiza o texto para indicar sucesso
        text_widget.config(state=tk.NORMAL)
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, "Logout forçado realizado com sucesso!")
        text_widget.config(state=tk.DISABLED)
    except Exception as e:
        text_widget.config(state=tk.NORMAL)
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, f"Erro ao realizar logout: {e}")
        text_widget.config(state=tk.DISABLED)

# Criar interface gráfica
def criar_interface():
    janela = tk.Tk()
    janela.title("Gerenciador de Assignees")
    janela.geometry("700x400")  # Largura e altura da janela

    # Frame principal com barra de rolagem
    frame_principal = ttk.Frame(janela)
    frame_principal.pack(fill=tk.BOTH, expand=True)

    # Adicionar uma barra de rolagem
    scrollbar = ttk.Scrollbar(frame_principal, orient=tk.VERTICAL)
    text_widget = tk.Text(frame_principal, wrap=tk.WORD, yscrollcommand=scrollbar.set, width=90, height=20)
    scrollbar.config(command=text_widget.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    text_widget.config(state=tk.DISABLED)  # Apenas leitura inicialmente

    # Frame para os botões
    frame_botoes = ttk.Frame(janela)
    frame_botoes.pack(pady=10)

    # Botão para coletar IDs dos assignees
    btn_coletar_ids = ttk.Button(frame_botoes, text="Coletar IDs e Nomes", command=lambda: coletar_ids(text_widget))
    btn_coletar_ids.pack(side=tk.LEFT, padx=10)

    # Botão para realizar o POST de logout
    btn_forcar_logout = ttk.Button(frame_botoes, text="Forçar Logout", command=lambda: forcar_logout(text_widget))
    btn_forcar_logout.pack(side=tk.LEFT, padx=10)

    # Executar a janela
    janela.mainloop()

if __name__ == "__main__":
    criar_interface()

