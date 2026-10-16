import streamlit as st
import psycopg2
from psycopg2.extras import Json
from fpdf import FPDF
from datetime import datetime

# ---------------------------
# CSS global (ajustado: paleta mais suave — primary teal, accent coral)
# ---------------------------
st.markdown(
    """
    <style>
    :root{
      --bg: #f6f8fa;
      --card: #ffffff;
      --primary: #0a7fa6;   /* teal suave */
      --primary-2: #066b8f; /* teal mais escuro para gradiente */
      --accent:  #ff8a65;   /* coral suave complementar */
      --muted:   #334155;
      --step-bg: #eef6f8;
      --field-border: rgba(10,127,166,0.12);
    }

    html, body, [class*="css"] {
      font-family: Inter, "Segoe UI", Roboto, Arial, sans-serif;
      background: var(--bg);
      color: #0f172a;
    }

    /* Headings maiores e limpos */
    .stApp h1 { font-size: 40px !important; font-weight:800; color:var(--primary); margin: 6px 0 8px 0; }
    .stApp h2 { font-size: 22px !important; font-weight:700; color:var(--muted); margin: 0 0 10px 0; }
    .stApp h3 { font-size: 20px !important; font-weight:700; color:var(--muted); margin: 0 0 10px 0; }

    /* Card principal */
    .form-card {
      background: var(--card);
      border-radius: 12px;
      padding: 18px;
      margin-bottom: 18px;
      border-left: 8px solid var(--accent);
      box-shadow: 0 12px 30px rgba(10,20,30,0.05);
    }

    /* Step card (cada etapa) */
    .step-card {
      background: var(--step-bg);
      border-radius: 10px;
      padding: 12px 14px;
      margin: 10px 0 14px 0;
      border-left: 6px solid rgba(75,85,99,0.08);
      color: var(--muted);
      font-size: 18px;
      font-weight:700;
    }
    .step-card small { display:block; font-weight:600; color:#334155; margin-top:6px; font-size:14px; }

    /* Consentimento com destaque */
    .consent-box {
      background: linear-gradient(180deg,#fffefc,#fffaf9);
      border-left: 6px solid var(--accent);
      padding: 14px;
      border-radius: 10px;
      color:#0b1220;
      margin-bottom: 12px;
      font-size:15px;
      line-height:1.45;
    }

    /* Inputs e selects com destaque e fonte maior */
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>select,
    .stMultiselect>div>div>div>div {
      border: 1.6px solid var(--field-border) !important;
      padding: 12px !important;
      border-radius: 10px !important;
      background: linear-gradient(180deg, #ffffff, #fbfdff);
      font-size: 17px !important;
      color: #0b1220 !important;
      box-shadow: 0 8px 20px rgba(10,127,166,0.03) inset;
    }
    .stTextInput>div>div>input:focus,
    .stNumberInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus,
    .stSelectbox>div>div>select:focus {
      outline: none;
      border-color: var(--primary) !important;
      box-shadow: 0 10px 30px rgba(10,127,166,0.10);
    }

    /* Labels maiores e mais fortes (garante visibilidade) */
    label, .stTextInput>div>label, .stNumberInput>div>label, .stMultiselect>div>label, .stRadio>div>label {
      font-weight:800;
      color:#0b1220;
      font-size:17px;
    }

    /* Radios e multiselect com fundo leve e rótulos visíveis */
    .stRadio, .stMultiselect {
      padding: 10px;
      border-radius: 10px;
      background: linear-gradient(180deg,#ffffff,#fbfdff);
      border: 1px solid rgba(10,127,166,0.04);
      box-shadow: 0 8px 20px rgba(10,127,166,0.03);
      margin-bottom: 12px;
      font-size:16px;
      color: #0b1220;
    }

    /* Força visibilidade dos rótulos internos (caso Streamlit gere classes diferentes) */
    .stRadio label, .stRadio div, .stRadio span, .stCheckbox label, .stCheckbox div, .stCheckbox span,
    div[data-testid="stCheckbox"] label, div[data-testid="stCheckbox"] span {
      color: #0b1220 !important;
      font-size: 17px !important;
      font-weight: 700 !important;
    }

    /* Seletores adicionais para checkbox label (garante cobertura) */
    input[type="checkbox"] + label,
    input[type="checkbox"] ~ label,
    .stCheckbox label,
    .stCheckbox span,
    div[data-testid="stCheckbox"] label {
      color: #0b1220 !important;
      font-size: 17px !important;
      font-weight: 800 !important;
    }

    /* Aumenta tamanho e cor dos inputs de radio/checkbox */
    input[type="radio"], input[type="checkbox"] {
      transform: scale(1.18);
      accent-color: var(--primary);
      margin-right: 8px;
    }

    /* Botões primários (avançar / finalizar / download) */
    .stButton>button, .stDownloadButton>button {
      background: linear-gradient(90deg, var(--primary), var(--primary-2)) !important;
      color: white !important;
      border: none !important;
      padding: 12px 18px !important;
      border-radius: 12px !important;
      font-weight:800 !important;
      font-size:15px !important;
      box-shadow: 0 12px 36px rgba(10,127,166,0.12) !important;
    }

    /* Botões "Voltar" (secundários) — estilo consistente */
    .stColumns > div:nth-child(1) .stButton>button {
      background: transparent !important;
      color: var(--accent) !important;
      border: 1.6px solid rgba(255,138,101,0.18) !important;
      padding: 10px 16px !important;
      border-radius: 10px !important;
      font-weight:700 !important;
      font-size:15px !important;
      box-shadow: none !important;
    }

    /* Garante altura mínima dos botões dentro de formulários */
    .stForm button {
      min-height: 44px;
    }

    /* Mobile adjustments */
    @media (max-width:720px) {
      .stApp h1 { font-size:34px !important; }
      .stApp h3 { font-size:18px !important; }
      .stTextInput>div>div>input, .stNumberInput>div>div>input { font-size:15px !important; padding:10px !important; }
      .stColumns > div:nth-child(1) .stButton>button, .stColumns > div:nth-child(2) .stButton>button { width:100% !important; display:block; margin-bottom:8px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------
# PDF generation (mantido)
# ---------------------------
class PDF(FPDF):
    def header(self):
        # título central
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Formulário - Perguntas e Respostas", ln=True, align="C")
        # timestamp no topo direito (posicionado sem sobrepor o título)
        self.set_font("Arial", size=9)
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.set_xy(-70, 8)
        self.cell(60, 6, f"Gerado: {ts}", align="R")
        # espaço maior para garantir que a tabela não suba sobre o header
        self.ln(10)

    def footer(self):
        self.set_y(-12)
        self.set_font("Arial", size=9)
        self.cell(0, 8, f"Página {self.page_no()}", align="C")

def gerar_pdf_dados(dados: dict) -> bytes:
    """
    Gera um PDF com tabela Pergunta | Resposta e retorna bytes.
    Sempre retorna bytes ou lança exceção controlada.
    """
    pdf = PDF()
    pdf.set_auto_page_break(auto=False, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    left_margin = 15
    right_margin = 15
    pdf.set_left_margin(left_margin)
    pdf.set_right_margin(right_margin)

    # Larguras e alturas
    col1_w = 70
    col2_w = pdf.w - left_margin - right_margin - col1_w
    base_line_h = 6  # altura base por linha

    campos = [
        ("nome_pessoa", "Nome"),
        ("cargo_pessoa", "Cargo"),
        ("nome_escola", "Nome da escola"),
        ("etapas_ensino", "Etapas de ensino"),
        ("alunos_matriculados", "Alunos matriculados"),
        ("consentimento", "Consentimento"),
        ("alunos_necessidades", "Alunos com necessidades especiais"),
        ("alunos_laudo", "Alunos com laudo"),
        ("distribuicao_nivel_infatil", "Distribuição - Educação Infantil"),
        ("distribuicao_nivel_anos_iniciais", "Distribuição - Anos iniciais"),
        ("distribuicao_nivel_anos_finais", "Distribuição - Anos finais"),
        ("diagnosticos", "Diagnósticos"),
        ("tendencia_matriculas", "Tendência de matrículas"),
        ("professores_aee", "Professores AEE"),
        ("profissionais_apoio", "Profissionais de apoio"),
        ("deficit_auxiliares", "Déficit de auxiliares"),
        ("modalidade_atendimento", "Modalidade de atendimento"),
        ("rotatividade_equipe", "Rotatividade da equipe"),
        ("funcionamento_sala", "Funcionamento da sala de recursos"),
        ("recursos_tecnologia", "Recursos de tecnologia assistiva"),
        ("aquisicao", "Recursos / Materiais de aquisição urgente"),
        ("participacao_capacitacao", "Participação em capacitação"),
        ("adequacao_formacao", "Adequação da formação"),
        ("articulaxao_externa", "Articulação com redes externas"),
        ("prioridade", "Prioridade Nº1")
    ]

    def format_valor(v):
        if isinstance(v, (list, tuple)):
            return ", ".join(map(str, v)) if v else "-"
        if isinstance(v, bool):
            return "Sim" if v else "Não"
        if v is None:
            return "-"
        s = str(v).strip()
        if s == "" or s == ".":
            return "-"
        return s

    def nb_lines(pdf_obj, width, txt):
        # calcula número de linhas que o texto ocupará em multi_cell com a largura dada
        if txt is None or txt == "":
            return 1
        txt = txt.replace('\r', '')
        avail_w = max(1, width - 4)  # margem interna
        words_lines = txt.split('\n')
        lines = 0
        for part in words_lines:
            if part == "":
                lines += 1
                continue
            cur_w = 0.0
            for word in part.split(' '):
                w = pdf_obj.get_string_width(word + ' ')
                if cur_w + w <= avail_w:
                    cur_w += w
                else:
                    lines += 1
                    cur_w = w
            lines += 1
        return max(1, lines)

    def draw_table_header():
        pdf.set_fill_color(230, 230, 230)
        pdf.set_font("Arial", "B", 11)
        pdf.set_x(left_margin)
        pdf.cell(col1_w, base_line_h + 2, "Pergunta", border=1, align="L", fill=True)
        pdf.cell(col2_w, base_line_h + 2, "Resposta", border=1, ln=1, align="L", fill=True)

    # desenha cabeçalho inicial
    draw_table_header()
    fill = False  # zebra

    # monta linhas
    for chave, rotulo in campos:
        valor = format_valor(dados.get(chave, ""))
        # calcula número de linhas para cada coluna
        pdf.set_font("Arial", "B", 11)
        n1 = nb_lines(pdf, col1_w - 4, rotulo)
        pdf.set_font("Arial", size=11)
        n2 = nb_lines(pdf, col2_w - 4, valor)
        n_lines = max(n1, n2)
        altura = n_lines * base_line_h + 6  # espaço extra para conforto

        # se não houver espaço suficiente, nova página e redesenha cabeçalho
        if pdf.get_y() + altura + 20 > pdf.h - pdf.b_margin:
            pdf.add_page()
            draw_table_header()

        y_start = pdf.get_y()
        x_start = left_margin

        # desenha fundo zebra somente quando houver conteúdo real (não "-")
        if fill and valor != "-":
            pdf.set_fill_color(245, 245, 245)
            # desenha retângulo de fundo para a linha inteira
            pdf.rect(x_start, y_start, col1_w + col2_w, altura, style='F')
        fill = not fill

        # desenha bordas (retângulos) para garantir alinhamento e visibilidade
        pdf.set_draw_color(0, 0, 0)
        pdf.set_line_width(0.2)
        pdf.rect(x_start, y_start, col1_w, altura)          # borda da pergunta
        pdf.rect(x_start + col1_w, y_start, col2_w, altura) # borda da resposta

        # escreve o texto dentro das células usando multi_cell com pequenas margens internas
        pdf.set_xy(x_start + 3, y_start + 3)
        pdf.set_font("Arial", "B", 11)
        pdf.multi_cell(col1_w - 6, base_line_h, rotulo, border=0, align="L")

        pdf.set_xy(x_start + col1_w + 3, y_start + 3)
        pdf.set_font("Arial", size=11)
        pdf.multi_cell(col2_w - 6, base_line_h, valor, border=0, align="L")

        # posiciona cursor abaixo da linha desenhada
        pdf.set_xy(left_margin, y_start + altura)
        pdf.ln(1)

    # Gera saída do PDF e garante bytes
    try:
        pdf_out = pdf.output(dest='S')
    except Exception as e:
        # retorna exceção para o chamador tratar (ou retorna None)
        raise RuntimeError(f"Erro ao gerar PDF: {e}")

    if isinstance(pdf_out, (bytes, bytearray)):
        return bytes(pdf_out)
    if isinstance(pdf_out, str):
        try:
            return pdf_out.encode('latin-1')
        except Exception:
            return pdf_out.encode('utf-8', errors='replace')

    # fallback: converte repr para bytes (não esperado)
    return str(pdf_out).encode('utf-8')

# ---------------------------
# Interface (base mantida, com step-card e consentimento formatado)
# ---------------------------

# Cabeçalho principal (visual)
st.markdown("<div class='form-card'><h1>Formulário - Projeto Integrador</h1></div>", unsafe_allow_html=True)

# Estado inicial
if 'etapa_atual' not in st.session_state:
    st.session_state['etapa_atual'] = 1

if 'dados_formulario' not in st.session_state:
    st.session_state['dados_formulario'] = {}

# Etapa 1
if st.session_state['etapa_atual'] == 1:

    # Step card visual (destaca a etapa)
    st.markdown("<div class='step-card'>Etapa 1: Identificação e Porte da Escola<small>Preencha os dados de identificação da escola e do responsável</small></div>", unsafe_allow_html=True)

    with st.form('Etapa 1'):

        nome_pessoa = st.text_input(
            'Informe o seu nome',
            value= st.session_state['dados_formulario'].get('nome_pessoa', '')
        )

        cargo_pessoa = st.text_input(
            'Informe o seu cargo na escola',
            st.session_state['dados_formulario'].get('cargo_pessoa', '')
        )

        nome_escola = st.text_input(
            'Informe o nome da escola',
            value=st.session_state['dados_formulario'].get('nome_escola', '')
        )

        etapas_ensino = st.multiselect(
            'Quais são as Etapas de Ensino Atendidas?',
            options=['Educ. Infantil','Anos Iniciais','Anos Finais','EJA'],
            default= st.session_state['dados_formulario'].get('etapas_ensino', [])
        )

        alunos_matriculados = st.number_input(
            'Qual o número total de alunos matriculados?',
            min_value=0,
            step=1,
            value=st.session_state['dados_formulario'].get('alunos_matriculados', 0)
        )

        # Consentimento formatado (rótulo HTML + checkbox sem texto para garantir visibilidade)
        st.markdown(
            """
            <div class="consent-box">
              <strong>🔒 Consentimento para uso e compartilhamento de dados</strong>
              <p style="margin:8px 0 0 0;">
              O preenchimento deste formulário contribui para a construção de uma base de dados sobre alunos com necessidades especiais nas escolas públicas de Santa Catarina. 
              Este levantamento faz parte de um trabalho acadêmico e tem por objetivo mapear demandas, recursos e prioridades para apoiar políticas públicas.
              As informações fornecidas serão tratadas de forma confidencial e serão compartilhadas apenas com órgãos governamentais competentes para fins de planejamento e formulação de políticas educacionais.
              </p>
              <p style="margin:8px 0 0 0; font-size:13px; color:#475569;">
              Ao marcar a caixa de consentimento, você autoriza o uso dos dados conforme descrito acima.
              </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # checkbox + rótulo em colunas para garantir visibilidade do texto
        col_chk, col_label = st.columns([0.08, 1])
        with col_chk:
            consentimento = st.checkbox("", value=st.session_state['dados_formulario'].get('consentimento', False), key="consent_etapa1")
        with col_label:
            # rótulo grande e visível com fundo em primary e texto branco (mais suave que o azul anterior)
            st.markdown(
                """
                <div style="display:flex; align-items:center; height:100%;">
                  <span style="background:var(--primary); color:#ffffff; padding:8px 12px; border-radius:8px; font-size:17px; font-weight:800; display:inline-block;">
                    Concordo com as informações contidas acima
                  </span>
                </div>
                """,
                unsafe_allow_html=True
            )

        btn_enviar_1 = st.form_submit_button('Seguir para a proxima etapa')

    if btn_enviar_1:
        if consentimento:
            if nome_pessoa != '':
                if cargo_pessoa != '':
                    if nome_escola != '':
                        if etapas_ensino:
                            if alunos_matriculados:
                                st.session_state['dados_formulario'].update({
                                    'nome_pessoa' :  nome_pessoa,
                                    'cargo_pessoa' :  cargo_pessoa,
                                    'nome_escola'   : nome_escola,
                                    'etapas_ensino' :  etapas_ensino,
                                    'alunos_matriculados' :  alunos_matriculados,
                                    'consentimento' : consentimento
                                })
                                st.session_state['etapa_atual'] = 2
                                st.rerun()
                            else:
                                st.warning('Você deve informar o número total de alunos matriculados na escola')
                        else:
                            st.warning('Você deve informar quais as etapas de ensino que a escola atende')
                    else:
                        st.warning('Você deve preencher o nome da escola antes de avançar')
                else:
                    st.warning('Você deve preencher o seu cargo antes de avançar')
            else:
                st.warning('Você deve preencher o seu nome antes de avançar')
        else:
            st.warning('Você deve marcar o botão de consentimento para avançar')

# Etapa 2
elif st.session_state['etapa_atual'] == 2:

    st.markdown("<div class='step-card'>Etapa 2: Perfil Geral dos Alunos e Diagnósticos Consolidados<small>Dados agregados sobre alunos e diagnósticos</small></div>", unsafe_allow_html=True)

    with st.form('Etapa 2'):

        alunos_necessidades = st.number_input(
            'Qual o número total de alunos com necessidades especiais?',
              min_value=0,
              step=1,
              value= st.session_state['dados_formulario'].get('alunos_necessidades', 0)
        )

        alunos_laudo = st.number_input(
            'Qual o número total de alunos com laudo comprovado?',
              min_value=0,
              step=1,
              value=st.session_state['dados_formulario'].get('alunos_laudo', 0)
        )

        distribuicao_nivel_infatil = st.number_input(
            'Quantos destes alunos estão na educação infantil?',
            min_value=0,
            step=1,
            value=st.session_state['dados_formulario'].get('distribuicao_nivel_infatil', 0)
        )

        distribuicao_nivel_anos_iniciais = st.number_input(
            'Quantos destes alunos estão nos anos iniciais?',
             min_value=0,
             step=1,
             value=st.session_state['dados_formulario'].get('distribuicao_nivel_anos_iniciais', 0)
        )

        distribuicao_nivel_anos_finais = st.number_input(
            'Quantos destes alunos estão nos anos finais?',
            min_value=0,
            step=1,
            value=st.session_state['dados_formulario'].get('distribuicao_nivel_anos_finais', 0)
        )

        diagnosticos = st.multiselect(
            'Quais são os diagnósticos presentes?',
            options=['TEA','TDAH','Def. Auditiva','Def. Visual','Def. Intelectual'],
            default=st.session_state['dados_formulario'].get('diagnosticos', [])
        )

        tendencia_matriculas = st.radio(
            'Qual a tendência no número de matriculas nos últimos anos?',
            options=['Aumentou','Manteve-se','Diminuiu'],
            index=['Aumentou','Manteve-se','Diminuiu'].index(st.session_state['dados_formulario'].get('tendencia_matriculas', 'Aumentou'))
        )

        col_left, col_right = st.columns([1,1])
        with col_left:
            btn_voltar_2 = st.form_submit_button('Voltar a etapa anterior')
        with col_right:
            btn_enviar_2 = st.form_submit_button('Seguir para a proxima etapa')

    if btn_enviar_2:
        st.session_state['dados_formulario'].update({
            'alunos_necessidades': alunos_necessidades,
            'alunos_laudo': alunos_laudo,
            'distribuicao_nivel_infatil' : distribuicao_nivel_infatil,
            'distribuicao_nivel_anos_iniciais' : distribuicao_nivel_anos_iniciais,
            'distribuicao_nivel_anos_finais' : distribuicao_nivel_anos_finais,
            'diagnosticos' : diagnosticos,
            'tendencia_matriculas' : tendencia_matriculas,
        })
        st.session_state['etapa_atual'] = 3
        st.rerun()

    if btn_voltar_2:
        st.session_state['dados_formulario'].update({
            'alunos_necessidades': alunos_necessidades,
            'alunos_laudo': alunos_laudo,
            'distribuicao_nivel_infatil' : distribuicao_nivel_infatil,
            'distribuicao_nivel_anos_iniciais' : distribuicao_nivel_anos_iniciais,
            'distribuicao_nivel_anos_finais' : distribuicao_nivel_anos_finais,
            'diagnosticos' : diagnosticos,
            'tendencia_matriculas' : tendencia_matriculas,
        })
        st.session_state['etapa_atual'] = 1
        st.rerun()

# Etapa 3
elif st.session_state['etapa_atual'] == 3:

    st.markdown("<div class='step-card'>Etapa 3: Recursos Humanos e Déficit de Apoio<small>Informações sobre equipe e déficit</small></div>", unsafe_allow_html=True)

    with st.form('Etapa 3'):

        professores_aee = st.number_input(
            'Quantos professores de AEE atuam na escola?',
              min_value=0,
              step=1,
              value=st.session_state['dados_formulario'].get('professores_aee', 0)
        )

        profissionais_apoio = st.number_input(
            'Quantos profissionais de apoio / auxiliares ativos atuam na escola hoje?',
              min_value=0,
              step=1,
              value=st.session_state['dados_formulario'].get('profissionais_apoio', 0)
        )

        deficit_auxiliares = st.number_input(
            'Qual o déficit / quantidade faltante de auxiliares?',
            min_value=0,
            step=1,
            value=st.session_state['dados_formulario'].get('deficit_auxiliares', 0)
        )

        modalidade_atendimento = st.radio(
            'Qual a modalidade de atendimento em sala?',
            options=['Exclusiva (1 para 1)','Compartilhada','Ambas'],
            index=['Exclusiva (1 para 1)','Compartilhada','Ambas'].index(st.session_state['dados_formulario'].get('modalidade_atendimento', 'Exclusiva (1 para 1)'))
        )

        rotatividade_equipe = st.radio(
            'Como é a frequência de rotatividade da equipe?',
            options=['Baixa','Média','Alta (Prejudicial ao vínculo)'],
            index=['Baixa','Média','Alta (Prejudicial ao vínculo)'].index(st.session_state['dados_formulario'].get('rotatividade_equipe', 'Baixa'))
        )

        col_left, col_right = st.columns([1,1])
        with col_left:
            btn_voltar_3 = st.form_submit_button('Voltar a etapa anterior')
        with col_right:
            btn_enviar_3 = st.form_submit_button('Seguir para a proxima etapa')

    if btn_enviar_3:
        st.session_state['dados_formulario'].update({
            'professores_aee' : professores_aee,
            'profissionais_apoio' : profissionais_apoio,
            'deficit_auxiliares' : deficit_auxiliares,
            'modalidade_atendimento' : modalidade_atendimento,
            'rotatividade_equipe' : rotatividade_equipe,
        })
        st.session_state['etapa_atual'] = 4
        st.rerun()

    if btn_voltar_3:
        st.session_state['dados_formulario'].update({
            'professores_aee' : professores_aee,
            'profissionais_apoio' : profissionais_apoio,
            'deficit_auxiliares' : deficit_auxiliares,
            'modalidade_atendimento' : modalidade_atendimento,
            'rotatividade_equipe' : rotatividade_equipe,
        })
        st.session_state['etapa_atual'] = 2
        st.rerun()

# Etapa 4
elif st.session_state['etapa_atual'] == 4:

    st.markdown("<div class='step-card'>Etapa 4: Infraestrutura, AEE e Tecnologia Assistiva<small>Recursos e necessidades de aquisição</small></div>", unsafe_allow_html=True)

    with st.form('Etapa 4'):

        funcionamento_sala = st.radio(
            'Como está o funcionamento das sala de recursos (AEE)?',
            options=['Em funcionamento','Inativa','Não possuí'],
            index=['Em funcionamento','Inativa','Não possuí'].index(st.session_state['dados_formulario'].get('funcionamento_sala', 'Em funcionamento'))
        )

        recursos_tecnologia = st.multiselect(
            'Quais são recursos de tecnologia assistiva existentes?',
            options=['CAA (Comunicação)','Jogos adaptados','Teclado adaptado'],
            default=st.session_state['dados_formulario'].get('recursos_tecnologia', [])
        )

        aquisicao = st.text_input(
            'Quais são os Recursos / Materiais de Aquisição Urgente necessários?',
            value=st.session_state['dados_formulario'].get('aquisicao', '')
        )

        col_left, col_right = st.columns([1,1])
        with col_left:
            btn_voltar_4 = st.form_submit_button('Voltar a etapa anterior')
        with col_right:
            btn_enviar_4 = st.form_submit_button('Seguir para a proxima etapa')

        if btn_enviar_4:
            st.session_state['dados_formulario'].update({
                'funcionamento_sala' : funcionamento_sala,
                'recursos_tecnologia' : recursos_tecnologia,
                'aquisicao' : aquisicao,
            })
            st.session_state['etapa_atual'] = 5
            st.rerun()

        if btn_voltar_4:
            st.session_state['dados_formulario'].update({
                'funcionamento_sala' : funcionamento_sala,
                'recursos_tecnologia' : recursos_tecnologia,
                'aquisicao' : aquisicao,
            })
            st.session_state['etapa_atual'] = 3
            st.rerun()

# Etapa 5
elif st.session_state['etapa_atual'] == 5:

    st.markdown("<div class='step-card'>Etapa 5: Gestão pedagógica, Rede Externa e Prioridades<small>Capacitação, articulação e prioridades</small></div>", unsafe_allow_html=True)

    with st.form('Etapa 5'):

        participacao_capacitacao = st.radio(
            'São ofertadas capacitações na área?',
            options=['Sim, ofertada pela rede','Não recebe','Por conta própria'],
            index=['Sim, ofertada pela rede','Não recebe','Por conta própria'].index(st.session_state['dados_formulario'].get('participacao_capacitacao', 'Sim, ofertada pela rede'))
        )

        adequacao_formacao = st.radio(
            'Como é a adequação da formação à prática?',
            options=['Suficiente','Razoável (Requer prática)','Insuficiente'],
            index=['Suficiente','Razoável (Requer prática)','Insuficiente'].index(st.session_state['dados_formulario'].get('adequacao_formacao', 'Suficiente'))
        )

        articulaxao_externa = st.multiselect(
            'Existem articulações com redes Externa de Apoio?',
            options=['APAE','CAPSi / Saúde','CRAS','Clínicas Univ.'],
            default=st.session_state['dados_formulario'].get('articulaxao_externa', [])
        )

        prioridade = st.radio(
            'Qual a prioridade Nº 1 para a escola hoje?',
            options=['Contratação de Apoio','Formação','Infraestrutura','Materiais'],
            index=['Contratação de Apoio','Formação','Infraestrutura','Materiais'].index(st.session_state['dados_formulario'].get('prioridade', 'Contratação de Apoio'))
        )

        col_left, col_right = st.columns([1,1])
        with col_left:
            btn_voltar_5 = st.form_submit_button('Voltar a etapa anterior')
        with col_right:
            btn_enviar_5 = st.form_submit_button('Finalizar')

    if btn_enviar_5:
        st.session_state['dados_formulario'].update({
            'participacao_capacitacao' : participacao_capacitacao,
            'adequacao_formacao' : adequacao_formacao,
            'articulaxao_externa' : articulaxao_externa,
            'prioridade' : prioridade,
        })
        st.text('Você completou o preenchimento')

    if btn_voltar_5:
        st.session_state['dados_formulario'].update({
            'participacao_capacitacao' : participacao_capacitacao,
            'adequacao_formacao' : adequacao_formacao,
            'articulaxao_externa' : articulaxao_externa,
            'prioridade' : prioridade,
        })
        st.session_state['etapa_atual'] = 4
        st.rerun()

    if btn_enviar_5:
        st.session_state['dados_formulario'].update({
            'participacao_capacitacao' : participacao_capacitacao,
            'adequacao_formacao' : adequacao_formacao,
            'articulaxao_externa' : articulaxao_externa,
            'prioridade' : prioridade,
        })

        DATABASE_URL = st.secrets.get("DATABASE_URL") or st.secrets["DATABASE_URL"]

        conexao = psycopg2.connect(DATABASE_URL, sslmode="require")
        cursor = conexao.cursor()
        dados = st.session_state.get("dados_formulario", {})

        cursor.execute(
                """
                INSERT INTO formulario (
                    nome_pessoa, cargo_pessoa, nome_escola, etapas_ensino, alunos_matriculados,
                    consentimento, alunos_necessidades, alunos_laudo,
                    distribuicao_nivel_infantil, distribuicao_nivel_anos_iniciais, distribuicao_nivel_anos_finais,
                    diagnosticos, tendencia_matriculas, professores_aee, profissionais_apoio, deficit_auxiliares,
                    modalidade_atendimento, rotatividade_equipe, funcionamento_sala, recursos_tecnologia,
                    aquisicao, participacao_capacitacao, adequacao_formacao, articulaxao_externa, prioridade,
                    updated_at
                ) VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s,
                    %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    now()
                )
                RETURNING id;
                """,
                (
                    dados.get("nome_pessoa"),
                    dados.get("cargo_pessoa"),
                    dados.get("nome_escola"),
                    dados.get("etapas_ensino"),
                    dados.get("alunos_matriculados"),
                    dados.get("consentimento"),
                    dados.get("alunos_necessidades"),
                    dados.get("alunos_laudo"),
                    dados.get("distribuicao_nivel_infatil"),
                    dados.get("distribuicao_nivel_anos_iniciais"),
                    dados.get("distribuicao_nivel_anos_finais"),
                    dados.get("diagnosticos"),
                    dados.get("tendencia_matriculas"),
                    dados.get("professores_aee"),
                    dados.get("profissionais_apoio"),
                    dados.get("deficit_auxiliares"),
                    dados.get("modalidade_atendimento"),
                    dados.get("rotatividade_equipe"),
                    dados.get("funcionamento_sala"),
                    dados.get("recursos_tecnologia"),
                    dados.get("aquisicao"),
                    dados.get("participacao_capacitacao"),
                    dados.get("adequacao_formacao"),
                    dados.get("articulaxao_externa"),
                    dados.get("prioridade")
                )
            )
        conexao.commit()
        st.success(f"Dados salvos com sucesso!")

        st.session_state['pdf_ready'] = True

        if st.session_state.get('pdf_ready') and st.session_state.get('etapa_atual') == 5:
            dados_para_pdf = st.session_state.get("dados_formulario", {})
            if dados_para_pdf:
                pdf_bytes = gerar_pdf_dados(dados_para_pdf)
                if pdf_bytes is None:
                    st.error("Ocorreu um erro ao gerar o PDF. Tente novamente ou verifique os dados.")
                else:
                    nome_arquivo = f"formulario_{dados_para_pdf.get('nome_escola','resposta')}.pdf"
                    st.download_button(
                        label="Baixar PDF com perguntas e respostas",
                        data=pdf_bytes,
                        file_name=nome_arquivo,
                        mime="application/pdf"
                    )
            else:
                st.warning("Nenhum dado encontrado para gerar o PDF.")
