import streamlit as st
import psycopg2
from psycopg2.extras import Json

st.title('Formulário em blocos')

#Cria a chave de etapa_atual no dicionario do session_state para permitir controle com os botões de avançar e voltar e também qual formulario exibir
if 'etapa_atual' not in st.session_state.keys():
    st.session_state['etapa_atual'] = 1

#Cria a chave 'dados_formulario' no dicionario session state - Existe unicamente para armazenar os dados já preenchidos nos campos
#Quando se avança de pagina os dados já preenchidos não se perdem, ficam armazenados no dicionario
#Podemos utilizar o atributo value ou default nos proprios campos do formulario para pegar a informação diretamento do dicionario 
if 'dados_formulario' not in st.session_state.keys():
    st.session_state['dados_formulario'] = {}

# verifica em qual etapa se esta, caso esteja na primeira inicia o primeiro formulario (etapa 1)
if st.session_state['etapa_atual'] == 1:

    st.subheader("Etapa 1: Identificação e Porte da Escola") #Subtitulo da etapa para ficar visivel ao usuário

    with st.form('Etapa 1'): # inicia os formulario, o with é apenas uma segurança para garantir segurança ao abrir ou fechar um documento (Padrão)

        #inicio dos campos de preenchimento desta etapa
        nome_pessoa = st.text_input(
            'Informe o seu nome',
            value= st.session_state['dados_formulario'].get('nome_pessoa', '') # o value ou default nos campos de preenchimento serve para pegar as informações diretamente do dicionario dados formulario
        )

        cargo_pessoa = st.text_input(
            'Informe o seu cargo na escola', 
            st.session_state['dados_formulario'].get('cargo_pessoa', '')
        )

        nome_escola = st.text_input(
            'Informe o nome da escola', 
            st.session_state['dados_formulario'].get('nome_escola', '')
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

        #Verificar conteudo do texto
        informativo = st.text('Texto avisando sobre o conteudo do preenchimento e para que seram utilizadas e com quem será compartilhada - trabalhoa acadêmico')
        
        #caixa para marcação que a pessoa consente com o compartilhamento das informações
        consentimento = st.checkbox(
            'Concordo com as informações contidas acima',
            value= st.session_state['dados_formulario'].get('consentimento', False)
        )

        #botão de enviar - sempre deve estar dentro do form - caso contrario da erro ao exibir o formulario
        btn_enviar_1 = st.form_submit_button('Seguir para a proxima etapa')

#faz o update das informações no dicionario caso a pessoa clique em enviar e também marque e também valida se alguns campos essenciais estão preenchidos
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
                                st.rerun() #roda o formulario todo novamente  
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
        
# inicia segunda etapa do formulario caso a primeira esteja preenchida - segue exatamente a mesma lógica do primeiro formulario
elif st.session_state['etapa_atual'] == 2:

    st.subheader("Etapa 2: Perfil Geral dos Alunos e Diagnósticos Consolidados")

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
            'Quais são as Etapas de Ensino Atendidas?',
            options=['TEA','TDAH','Def. Auditiva','Def. Visual','Def. Intelectual'],
            default=st.session_state['dados_formulario'].get('diagnosticos', [])
        )


        tendencia_matriculas = st.radio(
            'Qual a tendência no número de matriculas nos últimos anos?',
            options=['Aumentou','Manteve-se','Diminuiu'],
            index=['Aumentou','Manteve-se','Diminuiu'].index(st.session_state['dados_formulario'].get('tendencia_matriculas', 'Aumentou'))                                      
        )

        btn_enviar_2 = st.form_submit_button('Seguir para a proxima etapa')

        btn_voltar_2 = st.form_submit_button('Voltar a etapa anterior')

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

        st.rerun() #roda tudo novamente    
    
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

elif st.session_state['etapa_atual'] == 3:

    st.subheader('Etapa 3: Recursos Humanos e Déficit de Apoio')

    with st.form('Etapa 3'):

        professores_aee = st.number_input(
            'Quantos professores de AEE atuam na escola?',
              min_value=0,
              step=1,
              value=st.session_state['dados_formulario'].get('professores_aee', 0)
        )

        profissionais_apoio = st.number_input(
            'Quantos profissionais de apoio / auxilares ativos atuam na escola hoje?',
              min_value=0,
              step=1,
              value=st.session_state['dados_formulario'].get('profissionais_apoio', 0)
        )

        deficit_auxiliares = st.number_input(
            'Qual o déficit / quantidade Faltante de Auxiliares?',
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
        'Como é a frequência de rotativade da equipe?',
        options=['Baixa','Média','Alta (Prejudicial ao vínculo)'],
        index=['Baixa','Média','Alta (Prejudicial ao vínculo)'].index(st.session_state['dados_formulario'].get('rotatividade_equipe', 'Baixa'))
        )

        btn_enviar_3 = st.form_submit_button('Seguir para a proxima etapa')

        btn_voltar_3 = st.form_submit_button('Voltar a etapa anterior')

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

elif st.session_state['etapa_atual'] == 4:

    st.subheader('Etapa 4: Infraestrutura, AEE e Tecnologia Assistiva')

    with st.form('Etapa 4'):

        funcionamento_sala = st.radio(
            'Como está o funconamento das sala de recursos (AEE)?',
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

        btn_enviar_4 = st.form_submit_button('Seguir para a proxima etapa')

        btn_voltar_4 = st.form_submit_button('Voltar a etapa anterior')

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

elif st.session_state['etapa_atual'] == 5:

    st.subheader('Etapa 5: Infraestrutura, AEE e Tecnologia Assistiva')

    with st.form('Etapa 5'): 

        participacao_capacitacao = st.radio(
            'São ofertadas capcitações na área?',
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

        btn_enviar_5 = st.form_submit_button('Finalizar')

        btn_voltar_5 = st.form_submit_button('Voltar a etapa anterior')

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
                    dados.get("distribuicao_nivel_infatil"),  # se corrigir o typo, ajuste aqui também
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



    



    







        
    
        
    
