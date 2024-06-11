import streamlit as st
import pandas as pd
import altair as alt
import os
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import uuid

# Load environment variables from .env file
load_dotenv()

# Email configuration
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
DESTINATION_EMAIL = os.getenv('DESTINATION_EMAIL')  # Use a test email address

def send_email(responses_html, submission_id):
    try:
        print("Setting up the server...")
        # Set up the server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        print("Server setup complete.")

        # Create the email
        print("Creating the email...")
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = DESTINATION_EMAIL
        msg['Subject'] = f"Survey Responses: Submission ID {submission_id}"
        msg.attach(MIMEText(responses_html, 'html'))

        # Send the email
        print("Sending the email...")
        server.send_message(msg)
        server.quit()
        st.success("Avaliação da ferramenta enviada com sucesso - obrigado pela participação!")
        print("Email sent successfully.")
    except Exception as e:
        st.error(f"Failed to send email. Error: {e}")
        print(f"Failed to send email. Error: {e}")

# Display welcome message
st.title("Pesquisa sobre Liderança Transformacional")

# Initialize session state
if 'survey_started' not in st.session_state:
    st.session_state.survey_started = False
if 'age_experience_submitted' not in st.session_state:
    st.session_state.age_experience_submitted = False
if 'likert_questions_submitted' not in st.session_state:
    st.session_state.likert_questions_submitted = False
if 'graph_displayed' not in st.session_state:
    st.session_state.graph_displayed = False
if 'feedback_submitted' not in st.session_state:
    st.session_state.feedback_submitted = False

# Create placeholders for the greeting message and the "Iniciar" button
welcome_placeholder = st.empty()
button_placeholder = st.empty()

if not st.session_state.survey_started:
    welcome_placeholder.write("Bem-Vindo(a) a essa pesquisa sobre Liderança Transformacional - esperamos que o resultado dessa pesquisa seja útil para seu desenvolvimento como gestor!")
    if button_placeholder.button('Iniciar'):
        st.session_state.survey_started = True
        welcome_placeholder.empty()
        button_placeholder.empty()

# Define the questions for the Likert scale
questions = [
    "Eu tenho uma compreensão clara de onde estamos indo",
    "Eu tenho uma noção clara de onde quer que nossa unidade estará em 5 anos",
    "Eu não tenho ideia de onde a organização está indo",
    "Eu digo coisas que deixam os funcionários orgulhosos de pertencer a essa organização",
    "Eu digo coisas positivas sobre o grupo de trabalho",
    "Eu incentivo as pessoas a ver os ambientes em mudança como situações cheias de oportunidades",
    "Eu desafio os membros da minha equipe a pensar sobre velhos problemas de novas maneiras",
    "Eu tenho ideias que forçam os membros da equipe a repensarem algumas coisas que nunca questionei antes",
    "Eu desafio os membros da minha equipe a repensarem algumas das minhas suposições básicas sobre o meu trabalho",
    "Eu considero os sentimentos pessoais dos membros da minha equipe antes de agir",
    "Eu me comporto de uma maneira que considera as necessidades pessoais dos membros da minha equipe",
    "Eu estou atento a que os interesses dos funcionários recebem a devida consideração",
    "Eu elogio os membros da equipe quando fazem um trabalho acima da média",
    "Eu reconheço a melhora na qualidade do trabalho dos membros da minha equipe",
    "Eu elogio pessoalmente os membros da minha equipe quando fazem um trabalho"
]

# Generate a unique Submission ID
submission_id = str(uuid.uuid4())

# Display the survey questions if the survey has started
if st.session_state.survey_started:
    # Define the options for the dropdown menus
    idade_options = ['até 20 anos', '20-30 anos', '30-40 anos', '40-50 anos', '50-60 anos', 'mais de 60 anos']
    experiencia_options = ['até 5 anos', '5-10 anos', '10-20 anos', '20-30 anos', 'mais de 30 anos']

    age_experience_placeholder = st.empty()
    if not st.session_state.age_experience_submitted:
        with age_experience_placeholder.form(key='age_experience_form'):
            idade = st.selectbox('Faixa Etária:', idade_options)
            experiencia = st.selectbox('Experiência:', experiencia_options)
            submit_button = st.form_submit_button(label='Próximo')
            if submit_button:
                st.session_state.age_experience_submitted = True
                st.session_state.idade = idade
                st.session_state.experiencia = experiencia
                age_experience_placeholder.empty()
                st.experimental_rerun()

    if st.session_state.age_experience_submitted and not st.session_state.likert_questions_submitted:
        likert_placeholder = st.empty()
        with likert_placeholder.form(key='likert_form'):
            # Collect Likert scale responses
            likert_values = []
            for question in questions:
                value = st.slider(question, 1, 7, 4)
                likert_values.append(value)

            # Process and display the results
            submit_button = st.form_submit_button(label='Computar')
            if submit_button:
                st.session_state.likert_values = likert_values
                st.session_state.likert_questions_submitted = True
                likert_placeholder.empty()
                st.session_state.graph_displayed = True
                st.experimental_rerun()

    if st.session_state.graph_displayed and not st.session_state.feedback_submitted:
        result_placeholder = st.empty()
        with result_placeholder.container():
            st.write("Processing and displaying results...")
            idade_value = idade_options.index(st.session_state.idade) + 1
            experiencia_value = experiencia_options.index(st.session_state.experiencia) + 1
            A = idade_value + experiencia_value
            B = sum(st.session_state.likert_values) / len(st.session_state.likert_values)

            data = pd.DataFrame({'A': [A], 'B': [B]})

            quadrant_labels = pd.DataFrame({
                'A': [7.5, 2.5, 7.5, 2.5],
                'B': [7.5, 7.5, 2.5, 2.5],
                'label': ['Estrategistas Experientes', 'Profissionais em Ascensão', 'Veteranos Eficazes', 'Novos Visionários']
            })

            base = alt.Chart(data).mark_point(filled=True, size=100).encode(
                x=alt.X('B:Q', scale=alt.Scale(domain=[0, 10]), title='Liderança Transformadora (LTM)'),
                y=alt.Y('A:Q', scale=alt.Scale(domain=[0, 10]), title='Experiência e Idade Combinadas')
            )
            labels = alt.Chart(quadrant_labels).mark_text(
                align='center',
                baseline='middle',
                fontSize=12,
                dy=-10
            ).encode(
                x='B:Q',
                y='A:Q',
                text='label:N'
            )
            hline = alt.Chart(pd.DataFrame({'y': [5]})).mark_rule(strokeDash=[5, 5], color='gray').encode(y='y')
            vline = alt.Chart(pd.DataFrame({'x': [5]})).mark_rule(strokeDash=[5, 5], color='gray').encode(x='x')

            chart = base + hline + vline + labels

            st.altair_chart(chart, use_container_width=True)

            st.write("Obrigado por preencher o questionário! Abaixo estão as definições de cada quadrante:")
            st.write("""
            - **Estrategistas Experientes**: Líderes que combinam alta experiência e alta liderança transformadora.
            - **Profissionais em Ascensão**: Líderes com alta liderança transformadora, mas ainda em fase de acumulação de experiência.
            - **Veteranos Eficazes**: Líderes com muita experiência, mas com oportunidades de desenvolvimento em liderança transformadora.
            - **Novos Visionários**: Líderes novos ou menos experientes que demonstram forte potencial em liderança transformadora.
            """)

            if st.button('Próximo'):
                st.session_state.graph_displayed = False
                result_placeholder.empty()
                st.experimental_rerun()

    if not st.session_state.graph_displayed and not st.session_state.feedback_submitted:
        # Use st.form to manage the state of the form
        with st.form("feedback_form"):
            st.write("Responda as seguintes perguntas sobre sua experiência:")
            question1 = st.slider("Como você avalia a facilidade de uso desta ferramenta?", 1, 7, 4)
            question2 = st.slider("O que você mais gostou na ferramenta?", 1, 7, 4)
            question3 = st.slider("O que você acha que poderia ser melhorado?", 1, 7, 4)
            question4 = st.slider("Você recomendaria esta ferramenta a outros? Por quê?", 1, 7, 4)

            submitted = st.form_submit_button("Enviar Respostas")
            if submitted:
                st.session_state.feedback_values = [
                    ("Como você avalia a facilidade de uso desta ferramenta?", question1),
                    ("O que você mais gostou na ferramenta?", question2),
                    ("O que você acha que poderia ser melhorado?", question3),
                    ("Você recomendaria esta ferramenta a outros? Por quê?", question4)
                ]
                st.session_state.feedback_submitted = True
                st.experimental_rerun()

    if st.session_state.feedback_submitted:
        st.write("Processing form submission...")
        feedback_values = st.session_state.feedback_values
        all_responses = {
            "Submission ID": submission_id,
            "Idade": st.session_state.idade,
            "Experiência": st.session_state.experiencia,
            **{q: v for q, v in zip(questions, st.session_state.likert_values)},
            **{q: v for q, v in feedback_values}
        }

        # Create HTML formatted string with semi-colon after question and answer
        responses_html = f"Submission ID: {submission_id}<br>" + "<br>".join([f"{k}:; {v};" for k, v in all_responses.items()])

        print("Sending email with responses...")
        send_email(responses_html, submission_id)
        print("Form submitted. Responses:", responses_html)
