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

# Email configuration
EMAIL_ADDRESS ="pesquisa.uni9.2024@gmail.com"
EMAIL_PASSWORD ="yzdfkblyoirritz"
DESTINATION_EMAIL = "ferrari_cesar@hotmail.com"

def send_email(message):
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
        msg['Subject'] = "Test Email"
        msg.attach(MIMEText(message, 'plain'))

        # Send the email
        print("Sending the email...")
        server.send_message(msg)
        server.quit()
        st.success("Hello World email sent successfully.")
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
    "Eu sinto que a liderança me apoia",
    # ... additional questions ...
]

responses = ""
for i, question in enumerate(questions):
    response = st.radio(question, ['Concordo totalmente', 'Concordo', 'Neutro', 'Discordo', 'Discordo totalmente'])
    responses += f"{question}: {response}\n"

if st.button('Enviar Respostas'):
    # Here, instead of sending the responses, we send a "Hello World" message.
    send_email("Hello World")
