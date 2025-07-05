import customtkinter as ctk
import os
import uuid
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from matplotlib import colors as mcolors
import sqlite3
from CTkMessagebox import CTkMessagebox


# Configuração da aparência do CustomTkinter
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('blue')

# --- Caminho do Banco de Dados ---
DB_FILE = os.path.join(os.path.dirname(__file__), 'smme.db')

# --- Funções de Banco de Dados ---
def connect_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row # Garante que as linhas retornem como dicionários (acessíveis por nome de coluna)
    return conn

def setup_database():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            cargo TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS setores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dispositivos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            info TEXT,
            setor_id INTEGER NOT NULL,
            FOREIGN KEY (setor_id) REFERENCES setores (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS solicitacoes_servico (
            id TEXT PRIMARY KEY,
            titulo TEXT NOT NULL,
            descricao TEXT,
            local TEXT,
            categoria TEXT,
            tecnico_atribuido TEXT,
            status TEXT DEFAULT 'Aberta'
        )
    ''')

    # Inserção de dados iniciais se o banco estiver vazio
    if cursor.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0] == 0:
        usuarios_iniciais = [
            {'username': 'Nicollas Martins', 'password': '13122006', 'cargo': 'Técnico em Redes de Computadores'},
            {'username': 'Ricardo Gomes', 'password': '11031976', 'cargo': 'Técnico em Redes de Computadores'},
            {'username': 'Ana Silva', 'password': '87654321', 'cargo': 'Desenvolvedor(a) Back-end'},
            {'username': 'Bruno Costa', 'password': '12345678', 'cargo': 'Cientista de Dados'},
            {'username': 'Carla Dias', 'password': '98765432', 'cargo': 'Especialista em Cibersegurança'},
            {'username': 'Daniel Rocha', 'password': '34567890', 'cargo': 'Administrador(a) de Redes'},
            {'username': 'Eduarda Lima', 'password': '67890123', 'cargo': 'Arquiteto(a) de Software'},
            {'username': 'Felipe Mendes', 'password': '21098765', 'cargo': 'Engenheiro(a) de DevOps'},
            {'username': 'Gabriela Nunes', 'password': '54321098', 'cargo': 'Designer UX/UI'},
            {'username': 'Hugo Pereira', 'password': '90123456', 'cargo': 'Analista de Qualidade (QA)'},
            {'username': 'Isabela Santos', 'password': '78901234', 'cargo': 'Especialista em Banco de Dados'},
            {'username': 'Joao Oliveira', 'password': '45678901', 'cargo': 'Desenvolvedor(a) Front-end'}
        ]
        cursor.executemany("INSERT INTO usuarios (username, password, cargo) VALUES (?, ?, ?)",
                           [(u['username'], u['password'], u['cargo']) for u in usuarios_iniciais])

    if cursor.execute("SELECT COUNT(*) FROM setores").fetchone()[0] == 0:
        setores_e_dispositivos_iniciais = {
            'Produção': [
                {'name': 'Máquina CNC 01', 'info': 'Detalhes de produção: Utiliza 500W/h, uptime 98%.\nRegistros de manutenção: 10/05/2025 - Troca de broca.'},
                {'name': 'Linha de Montagem 03', 'info': 'Detalhes de produção: Consumo médio 1200W/h, produção diária de 500 peças.\nStatus: Operacional.'},
                {'name': 'Robô Soldador A', 'info': 'Detalhes de produção: Ciclos de solda 2000/dia, consumo 800W/h.\nPróxima calibração: 01/07/2025.'}
            ],
            'Administrativo': [
                {'name': 'Servidor Principal', 'info': 'Detalhes do servidor: Core i7, 32GB RAM, 2TB SSD.\nLocalização: Sala de Servidores, Rack 1.\nUptime: 120 dias.'},
                {'name': 'Impressora Multifuncional RH', 'info': 'Detalhes: Modelo HP LaserJet, consumo em espera 15W.\nÚltima manutenção: 01/06/2025.'},
                {'name': 'Roteador Wi-Fi Andar 2', 'info': 'Detalhes: Modelo Cisco, 5GHz, 802.11ac.\nUsuários conectados: 45.\nStatus: Estável.'}
            ],
            'Manutenção': [
                {'name': 'Estação de Trabalho Manut. 01', 'info': 'Detalhes: PC com software de diagnóstico.\nConsumo 250W, última atualização: 15/06/2025.'},
                {'name': 'Compressor de Ar Industrial', 'info': 'Detalhes: Capacidade 500L, consumo 3000W.\nPressão atual: 8 bar.\nAlerta: Necessita troca de filtro.'}
            ],
            'Segurança': [
                {'name': 'Câmera CCTV Corredor Principal', 'info': 'Detalhes: Câmera IP, 1080p, visão noturna.\nStatus: Gravando, acesso remoto OK.'},
                {'name': 'Sensor de Presença Entrada', 'info': 'Detalhes: Infravermelho passivo, alcance 10m.\nÚltimo disparo: 18/06/2025, 23:45.'}
            ]
        }
        for sector_name, devices in setores_e_dispositivos_iniciais.items():
            cursor.execute("INSERT INTO setores (nome) VALUES (?)", (sector_name,))
            sector_id = cursor.lastrowid
            for device in devices:
                # Usa 'name' aqui porque é a chave do dicionário de dados iniciais
                cursor.execute("INSERT INTO dispositivos (nome, info, setor_id) VALUES (?, ?, ?)",
                               (device['name'], device['info'], sector_id))

    if cursor.execute("SELECT COUNT(*) FROM solicitacoes_servico").fetchone()[0] == 0:
        solicitacoes_iniciais = [
            {
                'id': '1',
                'titulo': 'Problema com Impressora RH',
                'descricao': 'Impressora Multifuncional RH não está imprimindo.',
                'local': 'Administrativo',
                'categoria': 'Hardware',
                'tecnico_atribuido': 'Ricardo Gomes',
                'status': 'Aberta'
            },
            {
                'id': '2',
                'titulo': 'Rede lenta no 2º andar',
                'descricao': 'Usuários do 2º andar reportando lentidão na internet.',
                'local': 'Administrativo',
                'categoria': 'Rede',
                'tecnico_atribuido': 'Nicollas Martins',
                'status': 'Em Andamento'
            }
        ]
        cursor.executemany("INSERT INTO solicitacoes_servico (id, titulo, descricao, local, categoria, tecnico_atribuido, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
                           [(s['id'], s['titulo'], s['descricao'], s['local'], s['categoria'], s['tecnico_atribuido'], s['status']) for s in solicitacoes_iniciais])

    conn.commit()
    conn.close()

# --- Variáveis globais para armazenar o estado atual ---
current_sector = None
current_device = None # current_device agora conterá as chaves 'nome' e 'info'
current_user = None
chart_canvas = None
current_service_request_id = None

# --- Funções de Carregamento de Dados (do DB) ---
def load_tecnicos_disponiveis():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM usuarios WHERE cargo LIKE '%Técnico%'")
    tecnicos = [row['username'] for row in cursor.fetchall()]
    conn.close()
    return tecnicos

def load_categorias_servico():
    return ['Hardware', 'Software', 'Rede', 'Segurança', 'Manutenção Geral', 'Outros']

def load_locais_servico():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT nome FROM setores")
    locais = [row['nome'] for row in cursor.fetchall()]
    conn.close()
    return locais

# --- Funções de Funcionalidade da Aplicação ---

def validar_login():
    global current_user
    usuario_digitado = campo_usuario.get()
    senha_digitada = campo_senha.get()

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT username, cargo FROM usuarios WHERE username = ? AND password = ?", (usuario_digitado, senha_digitada))
    user_found = cursor.fetchone()
    conn.close()

    if user_found:
        current_user = {'username': user_found['username'], 'cargo': user_found['cargo']}
        resposta_login.configure(text=f'Login feito com sucesso!\nUsuário: {current_user["username"]}\nCargo: {current_user["cargo"]}', text_color='green')

        campo_usuario.delete(0, ctk.END)
        campo_senha.delete(0, ctk.END)

        app.after(1000, lambda: show_frame(sectors_frame))
    else:
        resposta_login.configure(text='Credenciais incorretas', text_color='red')
        campo_senha.delete(0, ctk.END)


def show_frame(frame_to_show):
    global chart_canvas
    if chart_canvas:
        chart_canvas.get_tk_widget().destroy()
        chart_canvas = None
        report_text_box.pack(pady=10, padx=10, fill="both", expand=True) # Garante que a textbox volte após o gráfico

    all_frames = [login_frame, sectors_frame, devices_frame, report_frame, service_requests_frame, sr_details_frame]
    for frame in all_frames:
        frame.pack_forget()

    frame_to_show.pack(expand=True, fill='both', padx=20, pady=20)


def select_sector(sector_name):
    global current_sector
    current_sector = sector_name
    populate_devices_frame()
    show_frame(devices_frame)

def select_device(device_data):
    """
    Define o dispositivo atualmente selecionado.
    device_data é um sqlite3.Row, que se comporta como um dicionário
    com as chaves das colunas do banco de dados ('id', 'nome', 'info').
    """
    global current_device
    # current_device já é um sqlite3.Row, que pode ser acessado como dicionário.
    # Não há necessidade de converter para dict explicitamente aqui se você usar
    # as chaves 'nome' e 'info' depois.
    current_device = device_data
    populate_report_frame()
    show_frame(report_frame)

def go_back_to_sectors():
    show_frame(sectors_frame)

def go_back_to_devices():
    populate_devices_frame()
    show_frame(devices_frame)

def go_to_service_requests():
    segmented_button_sr.set("Visualizar Solicitações")
    show_sr_section("Visualizar Solicitações")
    show_frame(service_requests_frame)

def go_back_to_service_requests_main():
    go_to_service_requests()


def filter_data():
    global chart_canvas
    if chart_canvas:
        chart_canvas.get_tk_widget().destroy()
        chart_canvas = None
        report_text_box.pack(pady=10, padx=10, fill="both", expand=True)

    if current_device:
        report_text_box.delete("1.0", ctk.END)
        # CORREÇÃO: Usando 'nome' ao invés de 'name'
        report_text_box.insert(ctk.END, f"Informações filtradas para '{current_device['nome']}' do '{current_sector}':\n\n")
        report_text_box.insert(ctk.END, f"Filtro aplicado: Dados dos últimos 7 dias.\n"
                                        f"Exemplo: Consumo médio de 450W/h, pico de 600W/h.\n"
                                        f"Nenhum alerta crítico encontrado nos últimos 7 dias após filtragem.")
    else:
        report_text_box.delete("1.0", ctk.END)
        report_text_box.insert(ctk.END, "Nenhum dispositivo selecionado para filtrar dados.")


def query_data():
    global chart_canvas
    if chart_canvas:
        chart_canvas.get_tk_widget().destroy()
        chart_canvas = None
        report_text_box.pack(pady=10, padx=10, fill="both", expand=True)

    if current_device:
        report_text_box.delete("1.0", ctk.END)
        # CORREÇÃO: Usando 'nome' ao invés de 'name'
        report_text_box.insert(ctk.END, f"Resultado da consulta para '{current_device['nome']}' do '{current_sector}':\n\n")
        report_text_box.insert(ctk.END, f"Consulta de desempenho: {current_device['nome']} operou com 95% de eficiência no último mês.\n"
                                        f"Último registro de erro: 12/06/2025 - Erro de comunicação (resolvido).")
    else:
        report_text_box.delete("1.0", ctk.END)
        report_text_box.insert(ctk.END, "Nenhum dispositivo selecionado para consultar dados.")


def generate_report():
    global chart_canvas
    if chart_canvas:
        chart_canvas.get_tk_widget().destroy()
        chart_canvas = None
        report_text_box.pack(pady=10, padx=10, fill="both", expand=True)

    if current_device:
        report_text_box.delete("1.0", ctk.END)
        # CORREÇÃO: Usando 'nome' ao invés de 'name'
        report_text_box.insert(ctk.END, f"Relatório completo para '{current_device['nome']}' do '{current_sector}':\n\n")
        report_text_box.insert(ctk.END, current_device['info'])
        report_text_box.insert(ctk.END, f"\n\n--- Fim do Relatório ---")
    else:
        report_text_box.delete("1.0", ctk.END)
        report_text_box.insert(ctk.END, "Nenhum dispositivo selecionado para gerar relatório.")


def show_chart():
    global chart_canvas

    if not current_device:
        report_text_box.delete("1.0", ctk.END)
        report_text_box.insert(ctk.END, "Selecione um dispositivo para ver os gráficos de dados.")
        if chart_canvas:
            chart_canvas.get_tk_widget().destroy()
            chart_canvas = None
        return

    report_text_box.pack_forget() # Esconde a textbox para mostrar o gráfico

    if chart_canvas:
        chart_canvas.get_tk_widget().destroy()

    hours = np.arange(24)
    base_consumption = np.random.normal(50, 10, 24)
    peak_morning = np.random.normal(150, 20, 3)
    peak_afternoon = np.random.normal(180, 25, 4)
    consumption = base_consumption
    consumption[7:10] += peak_morning
    consumption[13:17] += peak_afternoon
    consumption = np.maximum(0, consumption)

    fig, ax = plt.subplots(figsize=(7, 4), layout='constrained')
    ax.plot(hours, consumption, marker='o', linestyle='-', color='#2D88FF')
    # CORREÇÃO: Usando 'nome' ao invés de 'name'
    ax.set_title(f'Consumo Energético de {current_device["nome"]} (Últimas 24h)', color='white')
    ax.set_xlabel('Hora do Dia', color='white')
    ax.set_ylabel('Consumo (Watts)', color='white')
    ax.set_xticks(hours)
    ax.grid(True, linestyle='--', alpha=0.6)

    try:
        # Tenta obter a cor de fundo do CustomTkinter para o Matplotlib
        if ctk.get_appearance_mode() == "Dark":
            ctk_bg_color_str = "#242424" # Cor de fundo do CustomTkinter no modo escuro
        else:
            ctk_bg_color_str = "#dbdbdb" # Cor de fundo do CustomTkinter no modo claro

        matplotlib_bg_color = mcolors.to_rgb(ctk_bg_color_str)
    except ValueError:
        # Fallback caso a conversão falhe
        matplotlib_bg_color = 'dimgray'

    fig.patch.set_facecolor(matplotlib_bg_color)
    ax.set_facecolor(matplotlib_bg_color)
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.spines['left'].set_color('white')
    ax.spines['bottom'].set_color('white')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    chart_canvas = FigureCanvasTkAgg(fig, master=report_frame)
    chart_canvas_widget = chart_canvas.get_tk_widget()
    chart_canvas_widget.pack(pady=10, padx=10, fill="both", expand=True)
    chart_canvas.draw()


def confirm_open_service_request():
    titulo = entry_sr_titulo.get()
    descricao = textbox_sr_descricao.get("1.0", ctk.END).strip()
    local = combobox_sr_local.get()
    categoria = combobox_sr_categoria.get()
    tecnico = combobox_sr_tecnico.get()

    if not all([titulo, descricao, local, categoria, tecnico]):
        label_sr_status.configure(text="ERRO: Preencha TODOS os campos para abrir a solicitação!", text_color='red', font=('Inter', 16, 'bold'))
        return

    label_sr_status.configure(text="") # Limpa mensagem de erro anterior

    app.temp_sr_data = {
        'titulo': titulo,
        'descricao': descricao,
        'local': local,
        'categoria': categoria,
        'tecnico_atribuido': tecnico
    }

    # Diálogo de confirmação usando CTkToplevel (pode ser substituído por CTkMessagebox se preferir)
    confirmation_dialog = ctk.CTkToplevel(app)
    confirmation_dialog.title("Confirmar Abertura de Solicitação")
    confirmation_dialog.geometry("350x150")
    confirmation_dialog.transient(app) # Define como janela "filha" de 'app'

    # Centraliza o diálogo
    app_x = app.winfo_x()
    app_y = app.winfo_y()
    app_width = app.winfo_width()
    app_height = app.winfo_height()

    dialog_width = 350
    dialog_height = 150
    x = app_x + (app_width // 2) - (dialog_width // 2)
    y = app_y + (app_height // 2) - (dialog_height // 2)
    confirmation_dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")

    def setup_dialog_focus():
        confirmation_dialog.grab_set() # Captura o foco, impede interação com outras janelas
        confirmation_dialog.lift() # Traz a janela para a frente

    app.after(100, setup_dialog_focus) # Garante que a janela esteja pronta antes de focar

    ctk.CTkLabel(confirmation_dialog, text="Deseja confirmar a abertura deste chamado?", font=('Inter', 14)).pack(pady=20)

    button_frame = ctk.CTkFrame(confirmation_dialog, fg_color="transparent")
    button_frame.pack(pady=10)

    ctk.CTkButton(button_frame, text="Sim", command=lambda: finalize_open_service_request(confirmation_dialog),
                    width=80, fg_color='#28a745', hover_color='#218838').pack(side='left', padx=10)
    ctk.CTkButton(button_frame, text="Não", command=confirmation_dialog.destroy,
                    width=80, fg_color='#dc3545', hover_color='#c82333').pack(side='right', padx=10)


def finalize_open_service_request(dialog):
    dialog.destroy() # Fecha o diálogo de confirmação

    titulo = app.temp_sr_data['titulo']
    descricao = app.temp_sr_data['descricao']
    local = app.temp_sr_data['local']
    categoria = app.temp_sr_data['categoria']
    tecnico = app.temp_sr_data['tecnico_atribuido']
    new_id = str(uuid.uuid4())[:8] # Gera um ID único e curto

    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO solicitacoes_servico (id, titulo, descricao, local, categoria, tecnico_atribuido, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (new_id, titulo, descricao, local, categoria, tecnico, 'Aberta'))
        conn.commit()
        label_sr_status.configure(text=f"Solicitação '{titulo}' aberta com sucesso!", text_color='green')

        # Limpa os campos após a abertura
        entry_sr_titulo.delete(0, ctk.END)
        textbox_sr_descricao.delete("1.0", ctk.END)
        combobox_sr_local.set("")
        combobox_sr_categoria.set("")
        combobox_sr_tecnico.set("")

        # Volta para a seção de visualizar solicitações para mostrar a nova
        segmented_button_sr.set("Visualizar Solicitações")
        show_sr_section("Visualizar Solicitações")

    except sqlite3.Error as e:
        label_sr_status.configure(text=f"Erro ao abrir solicitação: {e}", text_color='red')
        conn.rollback() # Desfaz a transação em caso de erro
    finally:
        conn.close()


def populate_service_requests_list():
    """Preenche a lista de solicitações de serviço na interface."""
    for widget in requests_list_frame.winfo_children():
        widget.destroy() # Limpa widgets anteriores

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, titulo, descricao, local, categoria, tecnico_atribuido, status FROM solicitacoes_servico ORDER BY id DESC")
    solicitacoes_servico = cursor.fetchall()
    conn.close()

    if not solicitacoes_servico:
        ctk.CTkLabel(requests_list_frame, text="Nenhuma solicitação de serviço aberta.", font=('Inter', 14, 'italic')).pack(pady=10)
        return

    for request in solicitacoes_servico:
        request_dict = dict(request) # Converte sqlite3.Row para dicionário para fácil acesso
        request_frame = ctk.CTkFrame(requests_list_frame, fg_color="transparent", border_color="gray", border_width=1, corner_radius=8)
        request_frame.pack(pady=5, padx=5, fill='x', expand=True)

        ctk.CTkLabel(request_frame, text=f"ID: {request_dict['id']}", font=('Inter', 12, 'bold')).pack(anchor='nw', padx=10, pady=(5,0))
        ctk.CTkLabel(request_frame, text=f"Título: {request_dict['titulo']}", font=('Inter', 14, 'bold')).pack(anchor='nw', padx=10)
        ctk.CTkLabel(request_frame, text=f"Local: {request_dict['local']} | Categoria: {request_dict['categoria']}", font=('Inter', 12)).pack(anchor='nw', padx=10)
        ctk.CTkLabel(request_frame, text=f"Técnico: {request_dict['tecnico_atribuido']} | Status: {request_dict['status']}", font=('Inter', 12)).pack(anchor='nw', padx=10, pady=(0,5))

        ctk.CTkButton(request_frame, text="Ver Detalhes", command=lambda req=request_dict: show_service_request_details(req),
                        width=100, height=25, font=('Inter', 12), corner_radius=5).pack(anchor='se', padx=10, pady=5)

    requests_list_frame.update_idletasks() # Atualiza a exibição da rolagem

def show_service_request_details(request_data):
    global current_service_request_id
    current_service_request_id = request_data['id']

    label_sr_details_id.configure(text=f"ID: {request_data['id']}")
    label_sr_details_titulo.configure(text=f"Título: {request_data['titulo']}")
    textbox_sr_details_descricao.configure(state='normal') # Habilita para edição temporária
    textbox_sr_details_descricao.delete("1.0", ctk.END)
    textbox_sr_details_descricao.insert(ctk.END, request_data['descricao'])
    textbox_sr_details_descricao.configure(state='disabled') # Desabilita após inserir
    label_sr_details_local.configure(text=f"Local: {request_data['local']}")
    label_sr_details_categoria.configure(text=f"Categoria: {request_data['categoria']}")
    label_sr_details_tecnico.configure(text=f"Técnico Atribuído: {request_data['tecnico_atribuido']}")
    label_sr_details_status.configure(text=f"Status: {request_data['status']}")

    show_frame(sr_details_frame)


def delete_service_request():
    """
    Exclui a solicitação de serviço atualmente visualizada após confirmação.
    """
    global current_service_request_id
    if not current_service_request_id:
        return

    # Usando CTkMessagebox para confirmação de exclusão
    confirm_delete = CTkMessagebox(title="Confirmar Exclusão",
                                       message=f"Tem certeza que deseja excluir a solicitação ID: {current_service_request_id}?",
                                       icon="warning", option_1="Não", option_2="Sim")
    response = confirm_delete.get()

    if response == "Sim":
        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM solicitacoes_servico WHERE id = ?", (current_service_request_id,))
            conn.commit()
            CTkMessagebox(title="Sucesso", message=f"Solicitação ID: {current_service_request_id} excluída com sucesso!",
                              icon="info")
            current_service_request_id = None # Limpa o ID da solicitação atual
            go_back_to_service_requests_main() # Volta para a lista de solicitações
        except sqlite3.Error as e:
            CTkMessagebox(title="Erro", message=f"Erro ao excluir solicitação: {e}", icon="cancel")
            conn.rollback()
        finally:
            conn.close()


def show_sr_section(section_name):
    """Alterna entre as seções 'Visualizar Solicitações' e 'Abrir Nova Solicitação'."""
    if section_name == "Visualizar Solicitações":
        open_new_request_section.pack_forget()
        view_requests_section.pack(fill="both", expand=True)
        populate_service_requests_list() # Recarrega a lista
    else: # "Abrir Nova Solicitação"
        view_requests_section.pack_forget()
        open_new_request_section.pack(fill="both", expand=True)
        # Limpa os campos do formulário ao alternar para "Abrir Nova Solicitação"
        entry_sr_titulo.delete(0, ctk.END)
        textbox_sr_descricao.delete("1.0", ctk.END)
        combobox_sr_local.set("")
        combobox_sr_categoria.set("")
        combobox_sr_tecnico.set("")
        label_sr_status.configure(text="") # Limpa qualquer status anterior

# --- Criação da Interface Gráfica (CustomTkinter) ---

app = ctk.CTk()
app.title('Sistema Modular de Monitoramento Energético')
app.state('zoomed') # Inicia a janela maximizada

# --- ADD THIS FUNCTION ---
def on_closing():
    """Handles the window closing event for a clean shutdown."""
    if CTkMessagebox(title="Sair?", message="Tem certeza que deseja sair?",
                     icon="question", option_1="Não", option_2="Sim").get() == "Sim":
        app.destroy()
# --- END ADDITION ---

# --- ADD THIS LINE ---
app.protocol("WM_DELETE_WINDOW", on_closing) # Handle closing the window with the 'X' button
# --- END ADDITION ---


# --- Frame de Login ---
login_frame = ctk.CTkFrame(app)

label_titulo_login = ctk.CTkLabel(login_frame, text='Acesso ao Sistema', font=('Inter', 24, 'bold'))
label_titulo_login.pack(pady=20)

label_usuario = ctk.CTkLabel(login_frame, text='Usuário:')
label_usuario.pack(pady=(10, 2))
campo_usuario = ctk.CTkEntry(login_frame, placeholder_text='Digite seu usuário', width=280, height=35)
campo_usuario.pack(pady=(2, 10))

label_senha = ctk.CTkLabel(login_frame, text='Senha:')
label_senha.pack(pady=(10, 2))
campo_senha = ctk.CTkEntry(login_frame, placeholder_text='Digite sua senha', show='*', width=280, height=35)
campo_senha.pack(pady=(2, 15))

botao_login = ctk.CTkButton(login_frame, text='Login', command=validar_login, width=280, height=40,
                             font=('Inter', 16, 'bold'), fg_color='#2D88FF', hover_color='#1E6BB8', corner_radius=10)
botao_login.pack(pady=(15, 20))

resposta_login = ctk.CTkLabel(login_frame, text='', wraplength=260, font=('Inter', 14))
resposta_login.pack(pady=(5, 10))


# --- Frame de Seleção de Setores ---
sectors_frame = ctk.CTkFrame(app)

label_titulo_setores = ctk.CTkLabel(sectors_frame, text='Selecione uma Opção', font=('Inter', 24, 'bold'))
label_titulo_setores.pack(pady=20)

buttons_frame_sectors = ctk.CTkScrollableFrame(sectors_frame, width=300, height=300)
buttons_frame_sectors.pack(pady=10, padx=10, fill="both", expand=True)

# Botão de solicitações de serviço permanece fixo no topo da lista de opções
btn_service_requests = ctk.CTkButton(buttons_frame_sectors, text='Solicitações de Serviço', command=go_to_service_requests,
                                      width=250, height=40, font=('Inter', 14, 'bold'), corner_radius=8,
                                      fg_color='#28a745', hover_color='#218838')
btn_service_requests.pack(pady=5, padx=5, fill='x')

def populate_sectors_frame():
    """Popula o frame de setores com botões dinâmicos."""
    # Remove todos os botões EXCETO o de solicitações de serviço
    for widget in buttons_frame_sectors.winfo_children():
        if widget != btn_service_requests:
            widget.destroy()

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT nome FROM setores ORDER BY nome")
    setores = [row['nome'] for row in cursor.fetchall()]
    conn.close()

    for sector in setores:
        btn = ctk.CTkButton(buttons_frame_sectors, text=sector, command=lambda s=sector: select_sector(s),
                            width=250, height=40, font=('Inter', 14, 'bold'), corner_radius=8)
        btn.pack(pady=5, padx=5, fill='x')


botao_sair_sectors = ctk.CTkButton(sectors_frame, text='Sair', command=on_closing, width=100, height=30, # Changed command to on_closing
                                    fg_color='#FF4500', hover_color='#CD3700', corner_radius=8)
botao_sair_sectors.pack(side='bottom', pady=(10, 10))


# --- Frame de Seleção de Dispositivos ---
devices_frame = ctk.CTkFrame(app)

label_titulo_devices = ctk.CTkLabel(devices_frame, text='Selecione um Dispositivo', font=('Inter', 24, 'bold'))
label_titulo_devices.pack(pady=20)

label_current_sector = ctk.CTkLabel(devices_frame, text="", font=('Inter', 16, 'italic'))
label_current_sector.pack(pady=(0, 10))

buttons_frame_devices = ctk.CTkScrollableFrame(devices_frame, width=300, height=300)
buttons_frame_devices.pack(pady=10, padx=10, fill="both", expand=True)

def populate_devices_frame():
    """Popula o frame de dispositivos com base no setor selecionado."""
    for widget in buttons_frame_devices.winfo_children():
        widget.destroy()

    if current_sector:
        label_current_sector.configure(text=f"Setor: {current_sector}")
        conn = connect_db()
        cursor = conn.cursor()
        # Seleciona 'nome' e 'info' que são as colunas no DB
        cursor.execute("SELECT id, nome, info FROM dispositivos WHERE setor_id = (SELECT id FROM setores WHERE nome = ?)", (current_sector,))
        devices_in_sector = cursor.fetchall() # Retorna sqlite3.Row objetos
        conn.close()

        if not devices_in_sector:
            ctk.CTkLabel(buttons_frame_devices, text="Nenhum dispositivo neste setor.", font=('Inter', 14, 'italic')).pack(pady=20)

        for device in devices_in_sector:
            # device é um sqlite3.Row, que se comporta como um dicionário
            btn = ctk.CTkButton(buttons_frame_devices, text=device['nome'], command=lambda d=device: select_device(d),
                                width=250, height=40, font=('Inter', 14, 'bold'), corner_radius=8)
            btn.pack(pady=5, padx=5, fill='x')
    else:
        label_current_sector.configure(text="Nenhum setor selecionado.")

botao_voltar_devices = ctk.CTkButton(devices_frame, text='Voltar', command=go_back_to_sectors, width=100, height=30,
                                      fg_color='#555555', hover_color='#333333', corner_radius=8)
botao_voltar_devices.pack(side='bottom', pady=(10, 5))


# --- Frame de Relatório de Dispositivo ---
report_frame = ctk.CTkFrame(app)

label_titulo_report = ctk.CTkLabel(report_frame, text='Relatório do Dispositivo', font=('Inter', 24, 'bold'))
label_titulo_report.pack(pady=20)

label_current_device = ctk.CTkLabel(report_frame, text="", font=('Inter', 16, 'italic'))
label_current_device.pack(pady=(0, 10))

report_text_box = ctk.CTkTextbox(report_frame, width=600, height=300, font=('Inter', 14),
                                 wrap='word', corner_radius=8)
report_text_box.pack(pady=10, padx=10, fill="both", expand=True)

def populate_report_frame():
    """Popula o frame de relatório com informações do dispositivo selecionado."""
    global chart_canvas
    if chart_canvas: # Destroi o gráfico se existir ao voltar para a textbox
        chart_canvas.get_tk_widget().destroy()
        chart_canvas = None
    report_text_box.pack(pady=10, padx=10, fill="both", expand=True) # Garante que a textbox esteja visível

    if current_device:
        # CORREÇÃO: Usando 'nome' ao invés de 'name'
        label_current_device.configure(text=f"Dispositivo: {current_device['nome']}")
        report_text_box.delete("1.0", ctk.END)
        report_text_box.insert(ctk.END, current_device['info'])
    else:
        label_current_device.configure(text="Nenhum dispositivo selecionado.")
        report_text_box.delete("1.0", ctk.END)
        report_text_box.insert(ctk.END, "Selecione um dispositivo para ver seu relatório.")

report_buttons_frame = ctk.CTkFrame(report_frame, fg_color="transparent")
report_buttons_frame.pack(pady=(10, 5))

# Botões de ação para o relatório
botao_filtrar = ctk.CTkButton(report_buttons_frame, text='Filtrar Dados', command=filter_data,
                              width=150, height=35, font=('Inter', 14), corner_radius=8)
botao_filtrar.pack(side='left', padx=5)

botao_consultar = ctk.CTkButton(report_buttons_frame, text='Consultar Dados', command=query_data,
                                width=150, height=35, font=('Inter', 14), corner_radius=8)
botao_consultar.pack(side='left', padx=5)

botao_relatorios = ctk.CTkButton(report_buttons_frame, text='Gerar Relatório', command=generate_report,
                                 width=150, height=35, font=('Inter', 14), corner_radius=8)
botao_relatorios.pack(side='left', padx=5)

botao_ver_graficos = ctk.CTkButton(report_buttons_frame, text='Ver Gráficos', command=show_chart,
                                    width=150, height=35, font=('Inter', 14), corner_radius=8,
                                    fg_color='#17a2b8', hover_color='#138496')
botao_ver_graficos.pack(side='left', padx=5)

botao_voltar_report = ctk.CTkButton(report_frame, text='Voltar', command=go_back_to_devices, width=100, height=30,
                                     fg_color='#555555', hover_color='#333333', corner_radius=8)
botao_voltar_report.pack(side='bottom', pady=(10, 5))


# --- Frame de Solicitações de Serviço ---
service_requests_frame = ctk.CTkFrame(app)

label_titulo_sr = ctk.CTkLabel(service_requests_frame, text='Solicitações de Serviço', font=('Inter', 24, 'bold'))
label_titulo_sr.pack(pady=20)

segmented_button_sr = ctk.CTkSegmentedButton(service_requests_frame,
                                              values=["Visualizar Solicitações", "Abrir Nova Solicitação"],
                                              command=show_sr_section,
                                              font=('Inter', 14, 'bold'))
segmented_button_sr.pack(pady=(0, 10))

# Seção para visualizar solicitações (inicialmente visível)
view_requests_section = ctk.CTkFrame(service_requests_frame, fg_color="transparent")
view_requests_section.pack(fill="both", expand=True)

requests_list_frame = ctk.CTkScrollableFrame(view_requests_section, width=600, height=300)
requests_list_frame.pack(pady=10, padx=10, fill="both", expand=True)

# Seção para abrir novas solicitações (inicialmente oculta)
open_new_request_section = ctk.CTkFrame(service_requests_frame, fg_color="transparent")
open_new_request_section.pack_forget()

form_frame_sr = ctk.CTkFrame(open_new_request_section, width=600)
form_frame_sr.pack(pady=10, padx=10, fill="x", expand=False)

ctk.CTkLabel(form_frame_sr, text="Título:", anchor='w').pack(fill='x', padx=10, pady=(5,0))
entry_sr_titulo = ctk.CTkEntry(form_frame_sr, placeholder_text="Título da solicitação", height=35)
entry_sr_titulo.pack(fill='x', padx=10, pady=(0,5))

ctk.CTkLabel(form_frame_sr, text="Descrição:", anchor='w').pack(fill='x', padx=10, pady=(5,0))
textbox_sr_descricao = ctk.CTkTextbox(form_frame_sr, height=100, wrap='word')
textbox_sr_descricao.pack(fill='x', padx=10, pady=(0,5))

ctk.CTkLabel(form_frame_sr, text="Local:", anchor='w').pack(fill='x', padx=10, pady=(5,0))
combobox_sr_local = ctk.CTkComboBox(form_frame_sr, values=[], width=200, height=35, state="readonly")
combobox_sr_local.set("") # Define valor padrão vazio
combobox_sr_local.pack(anchor='w', padx=10, pady=(0,5))

ctk.CTkLabel(form_frame_sr, text="Categoria:", anchor='w').pack(fill='x', padx=10, pady=(5,0))
combobox_sr_categoria = ctk.CTkComboBox(form_frame_sr, values=[], width=200, height=35, state="readonly")
combobox_sr_categoria.set("") # Define valor padrão vazio
combobox_sr_categoria.pack(anchor='w', padx=10, pady=(0,5))

ctk.CTkLabel(form_frame_sr, text="Técnico Atribuído:", anchor='w').pack(fill='x', padx=10, pady=(5,0))
combobox_sr_tecnico = ctk.CTkComboBox(form_frame_sr, values=[], width=200, height=35, state="readonly")
combobox_sr_tecnico.set("") # Define valor padrão vazio
combobox_sr_tecnico.pack(anchor='w', padx=10, pady=(0,5))

botao_abrir_solicitacao = ctk.CTkButton(form_frame_sr, text='Abrir Solicitação', command=confirm_open_service_request,
                                         width=200, height=40, font=('Inter', 16, 'bold'),
                                         fg_color='#2D88FF', hover_color='#1E6BB8', corner_radius=10)
botao_abrir_solicitacao.pack(pady=15)

label_sr_status = ctk.CTkLabel(form_frame_sr, text='', wraplength=500, font=('Inter', 14))
label_sr_status.pack(pady=(5, 10))

sr_bottom_buttons_frame = ctk.CTkFrame(service_requests_frame, fg_color="transparent")
sr_bottom_buttons_frame.pack(side='bottom', pady=(10, 5))

botao_voltar_sr = ctk.CTkButton(sr_bottom_buttons_frame, text='Voltar', command=go_back_to_sectors, width=100, height=30,
                                 fg_color='#555555', hover_color='#333333', corner_radius=8)
botao_voltar_sr.pack(side='left', padx=5)

botao_abrir_nova_solicitacao_direto = ctk.CTkButton(sr_bottom_buttons_frame, text='Abrir Nova Solicitação',
                                                   command=lambda: segmented_button_sr.set("Abrir Nova Solicitação") or show_sr_section("Abrir Nova Solicitação"),
                                                   width=180, height=30, font=('Inter', 14, 'bold'), corner_radius=8,
                                                   fg_color='#2D88FF', hover_color='#1E6BB8')
botao_abrir_nova_solicitacao_direto.pack(side='right', padx=5)


# --- Frame de Detalhes da Solicitação de Serviço ---
sr_details_frame = ctk.CTkFrame(app)

label_sr_details_title = ctk.CTkLabel(sr_details_frame, text='Detalhes da Solicitação', font=('Inter', 24, 'bold'))
label_sr_details_title.pack(pady=20)

label_sr_details_id = ctk.CTkLabel(sr_details_frame, text="ID:", font=('Inter', 14, 'bold'), anchor='w')
label_sr_details_id.pack(fill='x', padx=20, pady=(5,0))

label_sr_details_titulo = ctk.CTkLabel(sr_details_frame, text="Título:", font=('Inter', 16, 'bold'), anchor='w')
label_sr_details_titulo.pack(fill='x', padx=20, pady=(5,0))

ctk.CTkLabel(sr_details_frame, text="Descrição:", font=('Inter', 14, 'bold'), anchor='w').pack(fill='x', padx=20, pady=(10,0))
textbox_sr_details_descricao = ctk.CTkTextbox(sr_details_frame, height=150, wrap='word', font=('Inter', 14))
textbox_sr_details_descricao.pack(fill='both', expand=True, padx=20, pady=(0,10))

label_sr_details_local = ctk.CTkLabel(sr_details_frame, text="Local:", font=('Inter', 14), anchor='w')
label_sr_details_local.pack(fill='x', padx=20, pady=(5,0))

label_sr_details_categoria = ctk.CTkLabel(sr_details_frame, text="Categoria:", font=('Inter', 14), anchor='w')
label_sr_details_categoria.pack(fill='x', padx=20, pady=(5,0))

label_sr_details_tecnico = ctk.CTkLabel(sr_details_frame, text="Técnico Atribuído:", font=('Inter', 14), anchor='w')
label_sr_details_tecnico.pack(fill='x', padx=20, pady=(5,0))

label_sr_details_status = ctk.CTkLabel(sr_details_frame, text="Status:", font=('Inter', 14), anchor='w')
label_sr_details_status.pack(fill='x', padx=20, pady=(5,10))

sr_details_buttons_frame = ctk.CTkFrame(sr_details_frame, fg_color="transparent")
sr_details_buttons_frame.pack(side='bottom', pady=(10, 5))

botao_voltar_sr_details = ctk.CTkButton(sr_details_buttons_frame, text='Voltar para Solicitações', command=go_back_to_service_requests_main,
                                         width=180, height=30, font=('Inter', 14),
                                         fg_color='#555555', hover_color='#333333', corner_radius=8)
botao_voltar_sr_details.pack(side='left', padx=5)

botao_excluir_solicitacao = ctk.CTkButton(sr_details_buttons_frame, text='Excluir Solicitação', command=delete_service_request,
                                          width=180, height=30, font=('Inter', 14),
                                          fg_color='#dc3545', hover_color='#c82333', corner_radius=8)
botao_excluir_solicitacao.pack(side='right', padx=5)


# --- Inicialização ---
setup_database()

# Carrega os dados para os comboboxes (lista de técnicos, categorias, locais)
TECNICOS_DISPONIVEIS = load_tecnicos_disponiveis()
CATEGORIAS_SERVICO = load_categorias_servico()
LOCAIS_SERVICO = load_locais_servico()

combobox_sr_local.configure(values=LOCAIS_SERVICO)
combobox_sr_categoria.configure(values=CATEGORIAS_SERVICO)
combobox_sr_tecnico.configure(values=TECNICOS_DISPONIVEIS)

populate_sectors_frame() # Preenche o frame de setores ao iniciar

show_frame(login_frame) # Inicia mostrando a tela de login

app.mainloop()
