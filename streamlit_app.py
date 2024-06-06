from pyngrok import ngrok
import subprocess

# Adicione o código adaptado acima aqui
code = """
import streamlit as st
import pandas as pd
import altair as alt

idade_options = ['até 20 anos', '20-30 anos', '30-40 anos', '40-50 anos', '50-60 anos', 'mais de 60 anos']
experiencia_options = ['até 5 anos', '5-10 anos', '10-20 anos', '20-30 anos', 'mais de 30 anos']

st.title("Pesquisa sobre Liderança Transformadora")

idade = st.selectbox('Faixa Etária:', idade_options)
experiencia = st.selectbox('Experiência:', experiencia_options)

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

likert_values = []
for question in questions:
    value = st.slider(question, 1, 7, 4)
    likert_values.append(value)

if st.button('Enviar'):
    idade_value = idade_options.index(idade) + 1
    experiencia_value = experiencia_options.index(experiencia) + 1
    A = idade_value + experiencia_value
    B = sum(likert_values) / len(likert_values)

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
    hline = alt.Chart(pd.DataFrame({'y': [5]})).mark_rule(strokeDash=[5,5], color='gray').encode(y='y')
    vline = alt.Chart(pd.DataFrame({'x': [5]})).mark_rule(strokeDash=[5,5], color='gray').encode(x='x')

    chart = base + hline + vline + labels

    st.altair_chart(chart, use_container_width=True)
    st.write("Obrigado pela sua utilização dessa ferramenta!")
"""

with open('app.py', 'w') as f:
    f.write(code)

# Inicie o Streamlit em segundo plano
command = ["streamlit", "run", "app.py"]
process = subprocess.Popen(command)

# Crie um túnel ngrok para a porta 8501
public_url = ngrok.connect(port='8501')
print(f"Streamlit app is live at {public_url}")
