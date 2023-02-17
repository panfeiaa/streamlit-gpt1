import streamlit as st
import openai
import os
import smtplib
#import platform
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import tkinter as tk
try:
    from google.protobuf.internal import api_implementation
except ImportError:
    # For older versions of protobuf
    from google.protobuf import api_implementation
#if platform.system() == "Darwin":
#    os.environ['TCL_LIBRARY'] = "/Library/Frameworks/Tcl.framework/Versions/8.6/Resources/Scripts"
#    os.environ['TK_LIBRARY'] = "/Library/Frameworks/Tk.framework/Versions/8.6/Resources/Scripts"

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
    window = tk.Tk()
    window.title("发送邮件")
    email_entry = tk.Entry(window)
    email_entry.grid(row=0, column=1)
    tk.Label(window, text="收件人地址：").grid(row=0, column=0)
    recipient = email_entry.get()
    subject = "OpenAI GPT Answer Checker"
    message = f"GPT-3's answer: {response}"
    # 邮件服务器地址
    smtp_server = 'smtp.163.com'

    # 发件人地址
    from_email = 'pf305243464@163.com'
    print(question)
    # 收件人地址
    to_email = recipient

    # 邮件主题
    subject = 'chatgpt Email'

    # 邮件正文
    body = 'This is a chatgptanswer email.'

    # 创建一个带附件的邮件对象
    msg = MIMEMultipart()

    # 设置邮件主题、发件人和收件人
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    # 将正文添加到邮件中
    text = MIMEText(body)
    msg.attach(text)


    # 发送邮件
#    with smtplib.SMTP(smtp_server) as server:
#       server.login(from_email, 'zdmpzrjrpqeqbgdc')
#       server.sendmail(from_email, to_email, msg.as_string())
    try:
        smtpObj = smtplib.SMTP_SSL(smtp_server, 465)  # 启用SSL发信, 端口一般是465
        smtpObj.login(from_email, 'VRFQJIMZRCUFAPBB')  # 登录验证
        smtpObj.sendmail(from_email, to_email, msg.as_string())  # 发送
        print("mail has been send successfully.")
    except smtplib.SMTPException as e:
         print(e)

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
    window1 = tk.Tk()
    tk.Button(window1, text="发送邮件", command=send_email(response)).grid(row=2, column=1)

