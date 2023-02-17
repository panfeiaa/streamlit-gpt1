# -*- coding: utf-8 -*-
import streamlit as st
import openai
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

try:
    from google.protobuf.internal import api_implementation
except ImportError:
    # For older versions of protobuf
    from google.protobuf import api_implementation

openai.api_key = os.environ.get("OPENAI_API_KEY")
st.title('OpenAI GPT Answer Checker')

question = st.text_input("Q: What is your question?")
answer = st.text_input("A: What is the answer?")
model_engine = "text-davinci-003"


def generate_answer(question):
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=question,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = completions.choices[0].text
    return message


# 接收邮件地址
to_email = st.text_input("请输入收件人邮箱地址")
# 接收邮件主题
subject = st.text_input("请输入邮件主题")


def send_email(response):
    # 接收邮件正文
    body = response

    # 邮件服务器地址
    smtp_server = 'smtp.163.com'

    # 发件箱配置
    from_email = 'pf305243464@163.com'

    email_info = [body, smtp_server, from_email]
    return email_info



if st.button('Check'):
    statement = f"Is  the answer  to {question} {answer}?"
    response = generate_answer(statement)
    #    if  'you are good' in response.lower() :
    #        st.success("Answer is correct")
    #    else:
    #        st.error("Answer is incorrect")
    #
    st.write(f"GPT-3's answer:{response}")


if st.button("发送邮件"):
    try:
        # 连接 SMTP 服务器，这里以 QQ 邮箱为例
        server = smtplib.SMTP_SSL(send_email(generate_answer(question))[1], 465)
        server.login(send_email(generate_answer(question))[2], "VRFQJIMZRCUFAPBB")  # 填写自己的邮箱和密码

        # 组装邮件内容
        message = f"Subject: {subject}\n\n{send_email(generate_answer(question))[0]}"

        # 发送邮件
        server.sendmail(send_email(generate_answer(question))[2], to_email, message)
        server.quit()

        st.write(st.success("邮件已发送"))
    except Exception as e:
        st.write(st.write(""))
