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
    "Eu tenho uma noção clara de onde quer que nossa unidade se encaixe",
    "Eu tenho as ferramentas e recursos necessários para realizar o meu trabalho",
    "Eu recebo feedback regular sobre o meu desempenho",
    "Eu me sinto valorizado pelo meu trabalho",
    "Eu confio na liderança da minha unidade",
    "Eu entendo como o meu trabalho contribui para os objetivos da empresa",
    "Eu sinto que há oportunidades de crescimento na empresa",
    "Eu me sinto parte de uma equipe",
    "Eu sinto que minha opinião é valorizada"
]

# Collect responses
responses = {}
for question in questions:
    response = st.slider(question, 1, 5, 3)
    responses[question] = response

# Display collected responses
st.write("Respostas coletadas:")
st.write(responses)

# When the user is ready to submit the responses
if st.button('Enviar Respostas'):
    responses_str = "\n".join([f"{k}: {v}" for k, v in responses.items()])
    send_email(responses_str)
