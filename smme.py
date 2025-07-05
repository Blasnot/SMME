import customtkinter as ctk 
import os 
import uuid # Para gerar IDs únicos para as solicitações
import matplotlib.pyplot as plt # Importar matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # Para integrar o gráfico ao Tkinter
import numpy as np # Para gerar dados de exemplo para o gráfico
from matplotlib import colors as mcolors # Importar colors do matplotlib para conversão

# Configuração da aparência do CustomTkinter
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('blue') # Um tema azul para a UI 

# --- Credenciais e Dados Hardcoded ---
USUARIOS = [
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

# Dados de setores e dispositivos
SETORES_E_DISPOSITIVOS = {
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

# Variáveis globais para armazenar o estado atual
current_sector = None
current_device = None
current_user = None
chart_canvas = None # Para manter uma referência ao canvas do gráfico e poder destruí-lo

# --- Dados de Solicitações de Serviço ---
SOLICITACOES_SERVICO = [
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

# Listas para comboboxes
TECNICOS_DISPONIVEIS = [user['username'] for user in USUARIOS if 'Técnico' in user['cargo']]
CATEGORIAS_SERVICO = ['Hardware', 'Software', 'Rede', 'Segurança', 'Manutenção Geral', 'Outros']
LOCAIS_SERVICO = list(SETORES_E_DISPOSITIVOS.keys())


# --- Funções de Funcionalidade da Aplicação ---

def validar_login():
    """
    Valida as credenciais de login do usuário comparando com os dados hardcoded.
    Se o login for bem-sucedido, navega para a tela de setores.
    """
    global current_user
    usuario_digitado = campo_usuario.get()
    senha_digitada = campo_senha.get()

    user_found = None
    for user_data in USUARIOS:
        if user_data['username'] == usuario_digitado and user_data['password'] == senha_digitada:
            user_found = user_data
            break

    if user_found:
        current_user = user_found
        resposta_login.configure(text=f'Login feito com sucesso!\nUsuário: {user_found["username"]}\nCargo: {user_found["cargo"]}', text_color='green')
        
        campo_usuario.delete(0, ctk.END)
        campo_senha.delete(0, ctk.END)

        app.after(1000, lambda: show_frame(sectors_frame))
    else:
        resposta_login.configure(text='Credenciais incorretas', text_color='red')
        campo_senha.delete(0, ctk.END)


def show_frame(frame_to_show):
    """
    Esconde todos os frames e mostra o frame especificado.
    Também limpa qualquer gráfico existente ao mudar de frame.
    """
    global chart_canvas
    if chart_canvas:
        chart_canvas.get_tk_widget().destroy()
        chart_canvas = None
        # Garante que a textbox volte a ocupar o espaço total
        report_text_box.pack(pady=10, padx=10, fill="both", expand=True)

    all_frames = [login_frame, sectors_frame, devices_frame, report_frame, service_requests_frame, sr_details_frame]
    for frame in all_frames:
        frame.pack_forget()

    frame_to_show.pack(expand=True, fill='both', padx=20, pady=20)


def select_sector(sector_name):
    """Define o setor atual e navega para a tela de seleção de dispositivos."""
    global current_sector
    current_sector = sector_name
    populate_devices_frame()
    show_frame(devices_frame)

def select_device(device_data):
    """Define o dispositivo atual e navega para a tela de relatório."""
    global current_device
    current_device = device_data
    populate_report_frame()
    show_frame(report_frame)

def go_back_to_sectors():
    """Volta para a tela de seleção de setores."""
    show_frame(sectors_frame)

def go_back_to_devices():
    """Volta para a tela de seleção de dispositivos."""
    populate_devices_frame()
    show_frame(devices_frame)

def go_to_service_requests():
    """Navega para a tela de solicitações de serviço."""
    segmented_button_sr.set("Visualizar Solicitações")
    show_sr_section("Visualizar Solicitações")
    show_frame(service_requests_frame)

def go_back_to_service_requests_main():
    """Volta para a tela principal de solicitações de serviço."""
    go_to_service_requests()


def filter_data():
    """Função para filtrar dados (placeholder)."""
    # Remove o gráfico se estiver visível
    global chart_canvas
    if chart_canvas:
        chart_canvas.get_tk_widget().destroy()
        chart_canvas = None
        report_text_box.pack(pady=10, padx=10, fill="both", expand=True) # Retorna a textbox ao tamanho normal

    if current_device:
        report_text_box.delete("1.0", ctk.END)
        report_text_box.insert(ctk.END, f"Informações filtradas para '{current_device['name']}' do '{current_sector}':\n\n")
        report_text_box.insert(ctk.END, f"Filtro aplicado: Dados dos últimos 7 dias.\n"
                                        f"Exemplo: Consumo médio de 450W/h, pico de 600W/h.\n"
                                        f"Nenhum alerta crítico encontrado nos últimos 7 dias após filtragem.")
    else:
        report_text_box.delete("1.0", ctk.END)
        report_text_box.insert(ctk.END, "Nenhum dispositivo selecionado para filtrar dados.")


def query_data():
    """Função para consultar dados (placeholder)."""
    # Remove o gráfico se estiver visível
    global chart_canvas
    if chart_canvas:
        chart_canvas.get_tk_widget().destroy()
        chart_canvas = None
        report_text_box.pack(pady=10, padx=10, fill="both", expand=True) # Retorna a textbox ao tamanho normal

    if current_device:
        report_text_box.delete("1.0", ctk.END)
        report_text_box.insert(ctk.END, f"Resultado da consulta para '{current_device['name']}' do '{current_sector}':\n\n")
        report_text_box.insert(ctk.END, f"Consulta de desempenho: {current_device['name']} operou com 95% de eficiência no último mês.\n"
                                        f"Último registro de erro: 12/06/2025 - Erro de comunicação (resolvido).")
    else:
        report_text_box.delete("1.0", ctk.END)
        report_text_box.insert(ctk.END, "Nenhum dispositivo selecionado para consultar dados.")


def generate_report():
    """Função para gerar relatório (placeholder)."""
    # Remove o gráfico se estiver visível
    global chart_canvas
    if chart_canvas:
        chart_canvas.get_tk_widget().destroy()
        chart_canvas = None
        report_text_box.pack(pady=10, padx=10, fill="both", expand=True) # Retorna a textbox ao tamanho normal

    if current_device:
        report_text_box.delete("1.0", ctk.END)
        report_text_box.insert(ctk.END, f"Relatório completo para '{current_device['name']}' do '{current_sector}':\n\n")
        report_text_box.insert(ctk.END, current_device['info'])
        report_text_box.insert(ctk.END, f"\n\n--- Fim do Relatório ---")
    else:
        report_text_box.delete("1.0", ctk.END)
        report_text_box.insert(ctk.END, "Nenhum dispositivo selecionado para gerar relatório.")


def show_chart():
    """
    Gera e exibe um gráfico de exemplo (consumo energético) para o dispositivo selecionado.
    Usa matplotlib para criar o gráfico e FigureCanvasTkAgg para integrá-lo ao CustomTkinter.
    """
    global chart_canvas

    if not current_device:
        report_text_box.delete("1.0", ctk.END)
        report_text_box.insert(ctk.END, "Selecione um dispositivo para ver os gráficos de dados.")
        # Limpa qualquer gráfico anterior
        if chart_canvas:
            chart_canvas.get_tk_widget().destroy()
            chart_canvas = None
        return

    # Limpa a caixa de texto para dar espaço ao gráfico
    report_text_box.pack_forget()

    # Remove o gráfico anterior se existir
    if chart_canvas:
        chart_canvas.get_tk_widget().destroy()

    # Gerar dados de exemplo para o gráfico
    hours = np.arange(24)
    # Simular consumo energético com picos e vales
    base_consumption = np.random.normal(50, 10, 24)
    peak_morning = np.random.normal(150, 20, 3) # Ex: 7h, 8h, 9h
    peak_afternoon = np.random.normal(180, 25, 4) # Ex: 13h, 14h, 15h, 16h
    consumption = base_consumption
    consumption[7:10] += peak_morning
    consumption[13:17] += peak_afternoon
    consumption = np.maximum(0, consumption) # Garante que não haja consumo negativo

    # Criar a figura e o eixo do gráfico
    fig, ax = plt.subplots(figsize=(7, 4), layout='constrained')
    ax.plot(hours, consumption, marker='o', linestyle='-', color='#2D88FF')
    ax.set_title(f'Consumo Energético de {current_device["name"]} (Últimas 24h)', color='white')
    ax.set_xlabel('Hora do Dia', color='white')
    ax.set_ylabel('Consumo (Watts)', color='white')
    ax.set_xticks(hours)
    ax.grid(True, linestyle='--', alpha=0.6)

    # --- INÍCIO DA CORREÇÃO ---
    # Tenta obter a cor de fundo do CustomTkinter
    try:
        # Pega a cor diretamente do tema, que é mais estável.
        # Assegura que seja uma string hexadecimal ou um nome de cor CSS válido.
        if ctk.get_appearance_mode() == "Dark":
            ctk_bg_color_str = "#242424" # Cor padrão para tema escuro do CTk
        else:
            ctk_bg_color_str = "#dbdbdb" # Cor padrão para tema claro do CTk
            
        # Tenta converter para RGB. Matplotlib geralmente aceita hex ou nomes comuns.
        matplotlib_bg_color = mcolors.to_rgb(ctk_bg_color_str)
    except ValueError:
        # Se falhar, usa uma cor padrão sólida que o Matplotlib certamente reconhece
        matplotlib_bg_color = 'dimgray' # Uma tonalidade de cinza escura
    # --- FIM DA CORREÇÃO ---

    # Personalizar cores para o tema escuro do Matplotlib
    fig.patch.set_facecolor(matplotlib_bg_color)
    ax.set_facecolor(matplotlib_bg_color) # Usar a mesma cor de fundo para o eixo
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.spines['left'].set_color('white')
    ax.spines['bottom'].set_color('white')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    # Integrar o gráfico ao CustomTkinter
    chart_canvas = FigureCanvasTkAgg(fig, master=report_frame)
    chart_canvas_widget = chart_canvas.get_tk_widget()
    chart_canvas_widget.pack(pady=10, padx=10, fill="both", expand=True)
    chart_canvas.draw()


def confirm_open_service_request():
    """
    Mostra um diálogo de confirmação antes de abrir a solicitação de serviço.
    """
    titulo = entry_sr_titulo.get()
    descricao = textbox_sr_descricao.get("1.0", ctk.END).strip()
    local = combobox_sr_local.get()
    categoria = combobox_sr_categoria.get()
    tecnico = combobox_sr_tecnico.get()

    if not all([titulo, descricao, local, categoria, tecnico]):
        label_sr_status.configure(text="ERRO: Preencha TODOS os campos para abrir a solicitação!", text_color='red', font=('Inter', 16, 'bold'))
        return

    label_sr_status.configure(text="")

    app.temp_sr_data = {
        'titulo': titulo,
        'descricao': descricao,
        'local': local,
        'categoria': categoria,
        'tecnico_atribuido': tecnico
    }

    confirmation_dialog = ctk.CTkToplevel(app)
    confirmation_dialog.title("Confirmar Abertura de Solicitação")
    confirmation_dialog.geometry("350x150")
    confirmation_dialog.transient(app)

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
        confirmation_dialog.grab_set()
        confirmation_dialog.lift()

    app.after(100, setup_dialog_focus)

    ctk.CTkLabel(confirmation_dialog, text="Deseja confirmar a abertura deste chamado?", font=('Inter', 14)).pack(pady=20)

    button_frame = ctk.CTkFrame(confirmation_dialog, fg_color="transparent")
    button_frame.pack(pady=10)

    ctk.CTkButton(button_frame, text="Sim", command=lambda: finalize_open_service_request(confirmation_dialog),
                  width=80, fg_color='#28a745', hover_color='#218838').pack(side='left', padx=10)
    ctk.CTkButton(button_frame, text="Não", command=confirmation_dialog.destroy,
                  width=80, fg_color='#dc3545', hover_color='#c82333').pack(side='right', padx=10)


def finalize_open_service_request(dialog):
    """
    Finaliza a abertura da solicitação após a confirmação.
    """
    dialog.destroy()

    titulo = app.temp_sr_data['titulo']
    descricao = app.temp_sr_data['descricao']
    local = app.temp_sr_data['local']
    categoria = app.temp_sr_data['categoria']
    tecnico = app.temp_sr_data['tecnico_atribuido']

    new_request = {
        'id': str(uuid.uuid4())[:8],
        'titulo': titulo,
        'descricao': descricao,
        'local': local,
        'categoria': categoria,
        'tecnico_atribuido': tecnico,
        'status': 'Aberta'
    }
    SOLICITACOES_SERVICO.append(new_request)
    label_sr_status.configure(text=f"Solicitação '{titulo}' aberta com sucesso!", text_color='green')

    entry_sr_titulo.delete(0, ctk.END)
    textbox_sr_descricao.delete("1.0", ctk.END)
    combobox_sr_local.set("")
    combobox_sr_categoria.set("")
    combobox_sr_tecnico.set("")

    segmented_button_sr.set("Visualizar Solicitações")
    show_sr_section("Visualizar Solicitações")


def populate_service_requests_list():
    """Popula a lista de solicitações de serviço."""
    for widget in requests_list_frame.winfo_children():
        widget.destroy()

    if not SOLICITACOES_SERVICO:
        ctk.CTkLabel(requests_list_frame, text="Nenhuma solicitação de serviço aberta.", font=('Inter', 14, 'italic')).pack(pady=10)
        return

    for request in SOLICITACOES_SERVICO:
        request_frame = ctk.CTkFrame(requests_list_frame, fg_color="transparent", border_color="gray", border_width=1, corner_radius=8)
        request_frame.pack(pady=5, padx=5, fill='x', expand=True)

        ctk.CTkLabel(request_frame, text=f"ID: {request['id']}", font=('Inter', 12, 'bold')).pack(anchor='nw', padx=10, pady=(5,0))
        ctk.CTkLabel(request_frame, text=f"Título: {request['titulo']}", font=('Inter', 14, 'bold')).pack(anchor='nw', padx=10)
        ctk.CTkLabel(request_frame, text=f"Local: {request['local']} | Categoria: {request['categoria']}", font=('Inter', 12)).pack(anchor='nw', padx=10)
        ctk.CTkLabel(request_frame, text=f"Técnico: {request['tecnico_atribuido']} | Status: {request['status']}", font=('Inter', 12)).pack(anchor='nw', padx=10, pady=(0,5))
        
        ctk.CTkButton(request_frame, text="Ver Detalhes", command=lambda req=request: show_service_request_details(req),
                      width=100, height=25, font=('Inter', 12), corner_radius=5).pack(anchor='se', padx=10, pady=5)
    
    requests_list_frame.update_idletasks()


def show_service_request_details(request_data):
    """Exibe os detalhes de uma solicitação de serviço em uma nova tela."""
    label_sr_details_id.configure(text=f"ID: {request_data['id']}")
    label_sr_details_titulo.configure(text=f"Título: {request_data['titulo']}")
    textbox_sr_details_descricao.configure(state='normal')
    textbox_sr_details_descricao.delete("1.0", ctk.END)
    textbox_sr_details_descricao.insert(ctk.END, request_data['descricao'])
    textbox_sr_details_descricao.configure(state='disabled')
    label_sr_details_local.configure(text=f"Local: {request_data['local']}")
    label_sr_details_categoria.configure(text=f"Categoria: {request_data['categoria']}")
    label_sr_details_tecnico.configure(text=f"Técnico Atribuído: {request_data['tecnico_atribuido']}")
    label_sr_details_status.configure(text=f"Status: {request_data['status']}")

    show_frame(sr_details_frame)


def show_sr_section(section_name):
    """Controla qual seção (visualizar ou abrir) é mostrada no frame de solicitações."""
    if section_name == "Visualizar Solicitações":
        open_new_request_section.pack_forget()
        view_requests_section.pack(fill="both", expand=True)
        populate_service_requests_list()
    else: # "Abrir Nova Solicitação"
        view_requests_section.pack_forget()
        open_new_request_section.pack(fill="both", expand=True)
        entry_sr_titulo.delete(0, ctk.END)
        textbox_sr_descricao.delete("1.0", ctk.END)
        combobox_sr_local.set("")
        combobox_sr_categoria.set("")
        combobox_sr_tecnico.set("")
        label_sr_status.configure(text="")


# --- Criação da Interface Gráfica (CustomTkinter) ---

app = ctk.CTk()
app.title('Sistema Modular de Monitoramento Energético')
app.state('zoomed')

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

btn_service_requests = ctk.CTkButton(buttons_frame_sectors, text='Solicitações de Serviço', command=go_to_service_requests,
                                     width=250, height=40, font=('Inter', 14, 'bold'), corner_radius=8,
                                     fg_color='#28a745', hover_color='#218838')
btn_service_requests.pack(pady=5, padx=5, fill='x')

for sector in SETORES_E_DISPOSITIVOS.keys():
    btn = ctk.CTkButton(buttons_frame_sectors, text=sector, command=lambda s=sector: select_sector(s),
                        width=250, height=40, font=('Inter', 14, 'bold'), corner_radius=8)
    btn.pack(pady=5, padx=5, fill='x')

botao_sair_sectors = ctk.CTkButton(sectors_frame, text='Sair', command=app.destroy, width=100, height=30,
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
    """Preenche o frame de dispositivos com base no setor atual."""
    for widget in buttons_frame_devices.winfo_children():
        widget.destroy()

    if current_sector:
        label_current_sector.configure(text=f"Setor: {current_sector}")
        devices_in_sector = SETORES_E_DISPOSITIVOS.get(current_sector, [])
        for device in devices_in_sector:
            btn = ctk.CTkButton(buttons_frame_devices, text=device['name'], command=lambda d=device: select_device(d),
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

# Área de texto para exibir o relatório (pode ser escondida para mostrar o gráfico)
report_text_box = ctk.CTkTextbox(report_frame, width=600, height=300, font=('Inter', 14),
                                 wrap='word', corner_radius=8)
report_text_box.pack(pady=10, padx=10, fill="both", expand=True)

def populate_report_frame():
    """Preenche o frame de relatório com base no dispositivo atual."""
    # Garante que a textbox esteja visível e limpa qualquer gráfico anterior
    global chart_canvas
    if chart_canvas:
        chart_canvas.get_tk_widget().destroy()
        chart_canvas = None
    report_text_box.pack(pady=10, padx=10, fill="both", expand=True) # Garante que a textbox esteja visível

    if current_device:
        label_current_device.configure(text=f"Dispositivo: {current_device['name']}")
        report_text_box.delete("1.0", ctk.END)
        report_text_box.insert(ctk.END, current_device['info'])
    else:
        label_current_device.configure(text="Nenhum dispositivo selecionado.")
        report_text_box.delete("1.0", ctk.END)
        report_text_box.insert(ctk.END, "Selecione um dispositivo para ver seu relatório.")

# Frame para agrupar os botões de ações do relatório
report_buttons_frame = ctk.CTkFrame(report_frame, fg_color="transparent")
report_buttons_frame.pack(pady=(10, 5))

botao_filtrar = ctk.CTkButton(report_buttons_frame, text='Filtrar Dados', command=filter_data,
                              width=150, height=35, font=('Inter', 14), corner_radius=8)
botao_filtrar.pack(side='left', padx=5)

botao_consultar = ctk.CTkButton(report_buttons_frame, text='Consultar Dados', command=query_data,
                                width=150, height=35, font=('Inter', 14), corner_radius=8)
botao_consultar.pack(side='left', padx=5)

botao_relatorios = ctk.CTkButton(report_buttons_frame, text='Relatórios', command=generate_report,
                                 width=150, height=35, font=('Inter', 14), corner_radius=8)
botao_relatorios.pack(side='left', padx=5)

# NOVO BOTÃO: Ver Gráficos
botao_ver_graficos = ctk.CTkButton(report_buttons_frame, text='Ver Gráficos', command=show_chart,
                                   width=150, height=35, font=('Inter', 14), corner_radius=8,
                                   fg_color='#17a2b8', hover_color='#138496') # Cor para destaque
botao_ver_graficos.pack(side='left', padx=5)

# Botão Voltar para a tela de dispositivos
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

view_requests_section = ctk.CTkFrame(service_requests_frame, fg_color="transparent")
view_requests_section.pack(fill="both", expand=True)

requests_list_frame = ctk.CTkScrollableFrame(view_requests_section, width=600, height=300)
requests_list_frame.pack(pady=10, padx=10, fill="both", expand=True)

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
combobox_sr_local = ctk.CTkComboBox(form_frame_sr, values=LOCAIS_SERVICO, width=200, height=35, state="readonly")
combobox_sr_local.set("")
combobox_sr_local.pack(anchor='w', padx=10, pady=(0,5))

ctk.CTkLabel(form_frame_sr, text="Categoria:", anchor='w').pack(fill='x', padx=10, pady=(5,0))
combobox_sr_categoria = ctk.CTkComboBox(form_frame_sr, values=CATEGORIAS_SERVICO, width=200, height=35, state="readonly")
combobox_sr_categoria.set("")
combobox_sr_categoria.pack(anchor='w', padx=10, pady=(0,5))

ctk.CTkLabel(form_frame_sr, text="Técnico Atribuído:", anchor='w').pack(fill='x', padx=10, pady=(5,0))
combobox_sr_tecnico = ctk.CTkComboBox(form_frame_sr, values=TECNICOS_DISPONIVEIS, width=200, height=35, state="readonly")
combobox_sr_tecnico.set("")
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
label_sr_details_status.pack(fill='x', padx=20, pady=(5,15))

botao_voltar_sr_details = ctk.CTkButton(sr_details_frame, text='Voltar', command=go_back_to_service_requests_main,
                                        width=100, height=30, fg_color='#555555', hover_color='#333333', corner_radius=8)
botao_voltar_sr_details.pack(side='bottom', pady=(10, 5))


# --- Rodapé ---
botao_sair_app_global = ctk.CTkButton(app, text='Sair do Aplicativo', command=app.destroy, width=150, height=30,
                                      fg_color='#FF4500', hover_color='#CD3700', corner_radius=8)
botao_sair_app_global.pack(side='bottom', pady=(5, 5))

label_creditos = ctk.CTkLabel(app, text='Programado por Nicollas d\'Lucca L. Martins', font=('Inter', 12), text_color='gray')
label_creditos.pack(side='bottom', pady=(0, 10))


# Iniciar a aplicação mostrando o frame de login
show_frame(login_frame)

app.mainloop()