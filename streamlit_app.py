import streamlit as st
import pandas as pd
import altair as alt
import os
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Print loaded environment variables for debugging
st.write("Loaded environment variables:")
st.write("EMAIL_ADDRESS:", os.getenv('EMAIL_ADDRESS'))
st.write("EMAIL_PASSWORD:", os.getenv('EMAIL_PASSWORD'))
st.write("DESTINATION_EMAIL:", os.getenv('DESTINATION_EMAIL'))

# Email configuration
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
DESTINATION_EMAIL = os.getenv('DESTINATION_EMAIL')  # Use a test email address

def send_email(responses):
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
        msg['Subject'] = "Survey Responses"
        msg.attach(MIMEText(responses, 'plain'))

        # Send the email
        print("Sending the email...")
        server.send_message(msg)
        server.quit()
        st.success("Responses sent via email successfully.")
        print("Email sent successfully.")
    except Exception as e:
        st.error(f"Failed to send email. Error: {e}")
        print(f"Failed to send email. Error: {e}")

# Define the options for the dropdown menus
idade_options = ['até 20 anos', '20-30 anos', '30-40 anos', '40-50 anos', '50-60 anos', 'mais de 60 anos']
experiencia_options = ['até 5 anos', '5-10 anos', '10-20 anos', '20-30 anos', 'mais de 30 anos']

st.title("Pesquisa sobre Liderança Transformadora")

# Collect user inputs
idade = st.selectbox('Faixa Etária:', idade_options)
experiencia = st.selectbox('Experiência:', experiencia_options)

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


# Collect responses
responses = {}
for question in questions:
    response = st.slider(question, 1, 7, 4)
    responses[question] = response

# Convert responses to DataFrame for visualization
df_responses = pd.DataFrame(list(responses.items()), columns=['Question', 'Response'])

# Display collected responses
st.write("Respostas coletadas:")
st.write(df_responses)

# Data visualization
st.write("Distribuição das Respostas")
chart = alt.Chart(df_responses).mark_bar().encode(
    x=alt.X('Response:Q', bin=True),
    y='count()',
    color='Question'
).properties(
    width=600,
    height=400
)
st.altair_chart(chart)

# When the user is ready to submit the responses
if st.button('Enviar Respostas'):
    responses_str = "\n".join([f"{k}: {v}" for k, v in responses.items()])
    send_email(responses_str)
