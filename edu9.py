import streamlit as st
import openai 
import os
import smtplib
import pdfkit
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
try:
    from google.protobuf.internal import api_implementation
except ImportError:
    # For older versions of protobuf
    from google.protobuf import api_implementation
import jinja2


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
    question = st.text_input("Q: What is your email,if you want receive the results?")
    subject = "OpenAI GPT Answer Checker"
    message = f"GPT-3's answer: {response}"
    # 邮件服务器地址
    smtp_server = 'smtp.qq.com'

    # 发件人地址
    from_email = '305243464@qq.com'
    print(question)
    # 收件人地址
    to_email = question

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
    # 将回答生成为 HTML 页面
   template = jinja2.Template("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>OpenAI API Response</title>
    </head>
    <body>
        <p>{{ text }}</p>
    </body>
    </html>
    """)
    html = template.render(text=message)

    # 使用 pdfkit 将 HTML 页面转换为 PDF 文件
    html_filename = "openai_response.html"
    with open(html_filename, "w") as f:
        f.write(html)
        
    # 使用 pdfkit 将 HTML 文件转换为 PDF 文件
    pdf_filename = "openai_response.pdf"
    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None
    }
    pdfkit.from_file(html_filename, pdf_filename, options=options)

    # 添加附件
    with open(pdf_filename, 'rb') as f:
        attachment = MIMEApplication(f.read(), _subtype='pdf')
        attachment.add_header('Content-Disposition', 'attachment', filename=pdf_filename)
        msg.attach(attachment)
        
    # 删除临时文件
    os.remove(html_filename)
    
    # 发送邮件
    with smtplib.SMTP(smtp_server) as server:
        server.login(from_email, 'zdmpzrjrpqeqbgdc')
        server.sendmail(from_email, to_email, msg.as_string())
    
    

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

