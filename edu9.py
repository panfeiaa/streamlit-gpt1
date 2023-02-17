# -*- coding: utf-8 -*-
import streamlit as st
import openai
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
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
subject1=subject.encode('utf-8')
# 邮件服务器地址
smtp_server = 'smtp.163.com'
def send_email(response):
    # 接收邮件正文
    body = response

    # 发件箱配置
    from_email = 'pf305243464@163.com'

    msg = MIMEText(body, 'plain', 'utf-8')

    msg['From'] = formataddr(('Sender', from_email))
    msg['To'] = formataddr(('Recipient',to_email ))
    msg['Subject'] = subject


    return msg



if st.button('Check and send email'):
    statement = f"Is  the answer  to {question} {answer}?"
    response = generate_answer(statement)
    #    if  'you are good' in response.lower() :
    #        st.success("Answer is correct")
    #    else:
    #        st.error("Answer is incorrect")
    #
    st.write(f"GPT-3's answer:{response}")
    try:
        # 连接 SMTP 服务器，这里以 QQ 邮箱为例
        server = smtplib.SMTP_SSL(smtp_server, 465)
        server.login('pf305243464@163.com', "VRFQJIMZRCUFAPBB")  # 填写自己的邮箱和密码
        # 组装邮件内容
        message=send_email(response)
        # 发送邮件
        server.sendmail('pf305243464@163.com', to_email, message.as_string())
        server.quit()
        st.write(st.success("邮件已发送"))
    except Exception as e:
            st.write(st.error({e}))

