import streamlit as st
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Email configuration
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
DESTINATION_EMAIL = "ferrari_cesar@hotmail.com"

# Print environment variables to diagnose
st.write(f"EMAIL_ADDRESS: {EMAIL_ADDRESS}")
st.write(f"EMAIL_PASSWORD: {EMAIL_PASSWORD}")

def send_email(message):
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        st.error("Email address or password not set in environment variables.")
        return

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

st.title("Send Test Email")

if st.button('Send Hello World Email'):
    send_email("Hello World")
