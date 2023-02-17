import streamlit as st
import openai 
import os
import smtplib
from email.mime.text import MIMEText

openai.api_key = os.environ.get("OPENAI_API_KEY")
st.title('OpenAI GPT Answer Checker')

question = st.text_input("Q: What is your question?")
answer = st.text_input("A: What is the answer?")
model_engine = "text-davinci-003"

def generate_answer(question):
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=question,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = completions.choices[0].text
    return message

def send_email(response):
    question = st.text_input("Q: What is your email?")
    subject = "OpenAI GPT Answer Checker"
    message = f"GPT-3's answer: {response}"
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = '305243464@qq.com'
    msg['To'] = question

    s = smtplib.SMTP('smtp.qq.com', 587)
    s.starttls()
    s.login('305243464@qq.com', 'zdmpzrjrpqeqbgdc')
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()


if st.button('Check'):
    statement = f"Is  the answer  to {question} {answer}?"
    print(statement)
    response = generate_answer(statement)
    
#    if  'you are good' in response.lower() :
#        st.success("Answer is correct")
#    else:
#        st.error("Answer is incorrect")
#   
    st.write(f"GPT-3's answer:{response}")
    send_email(response)

