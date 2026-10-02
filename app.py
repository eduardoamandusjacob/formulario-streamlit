import streamlit as st
import psycopg2

DATABASE_URL = st.secrets.get("DATABASE_URL")

st.title('Formulário em blocos')

if not st.session_state.get('primeiro_bloco_ok', False):
    with st.form('primeiro Bloco'):
        nome = st.text_input('Informe o seu nome')
        nascimento = st.date_input('informe a sua data de nascimento')
        enviar_1 = st.form_submit_button('enviar primeiro bloco')

    if enviar_1:
        st.session_state['primeiro_bloco_ok'] = True
        st.session_state['nome'] =  nome
        st.session_state['nascimento'] = nascimento
        st.rerun() #roda tudo novamente

if st.session_state.get('primeiro_bloco_ok', False):
    with st.form('segundo bloco'):
        cidade = st.text_input('Informe sua cidade')
        enviar_2 = st.form_submit_button('enviar segundo bloco')

    if enviar_2:
        st.session_state['cidade']= cidade
        st.success('segundo bloco enviado com sucesso!')

        #conexao com o banco de dados PostgreSQL - Neon
        dados_conexao = st.secrets["DATABASE_URL"]
        conexao = psycopg2.connect(DATABASE_URL, sslmode="require")
        cursor = conexao.cursor()

        cursor.execute('''
        INSERT INTO dados (nome, nascimento, cidade)
        VALUES (%s, %s, %s)''', 
        (st.session_state['nome'], st.session_state['nascimento'],st.session_state['cidade'])
    )
        conexao.commit()
        cursor.close()
        conexao.close()

        st.success('Dados salvos com sucesso!')
        
    
        
    
