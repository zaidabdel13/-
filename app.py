import streamlit as st
import PyPDF2
import re
from docx import Document
import io
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

st.set_page_config(page_title="CV Extractor + Email", layout="centered")
st.title("📄 مستخرج السير الذاتية الذكي + دعوة عبر الإيميل")
st.write("ارفع السيرة الذاتية، عدل البيانات، واختر وقت المقابلة ثم أرسل الدعوة.")

uploaded_file = st.file_uploader("ارفع السيرة الذاتية هنا", type=["pdf", "docx"])

date_input = st.date_input("📅 تاريخ المقابلة", format="YYYY-MM-DD")
time_input = st.time_input("⏰ وقت المقابلة")

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    return ''.join(page.extract_text() for page in reader.pages if page.extract_text())

def extract_text_from_docx(file):
    doc = Document(file)
    return '\n'.join(para.text for para in doc.paragraphs)

def extract_phone_numbers(text):
    return re.findall(r'(?:\+?966|0)?5\d{8}', text)

def extract_emails(text):
    return re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text)

def extract_name(text):
    for line in text.strip().split('\n'):
        line = line.strip()
        if len(line.split()) >= 2 and not any(char.isdigit() for char in line):
            return line
    return "غير معروف"

def send_email(to_email, date_str, time_str):
    sender_email = "zaid.hr.optc@gmail.com"
    sender_password = "pjxmoytkvtslfcvb"

    subject = "دعوة لمقابلة عمل"
    body = f"""السلام عليكم ورحمة الله وبركاته،

نشكر لك اهتمامك بالتقدم على وظيفة في شركة تموين الشرق للتجارة.
يسرنا دعوتك لإجراء مقابلة عمل لمناقشة مؤهلاتك بشكل أوسع والتعرف عليك بشكل أفضل.

تفاصيل المقابلة:
📅 التاريخ: {date_str}
⏰ الوقت: {time_str}
📍 الموقع: https://maps.app.goo.gl/meqgz4UdRxXAvc7T8

نأمل منكم الالتزام بالزي الرسمي السعودي واحضار نسخة من السيرة الذاتية.

نتطلع للقائك ونتمنى لك التوفيق...
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
        return True
    except Exception as e:
        return str(e)

if uploaded_file:
    file_bytes = uploaded_file.read()
    file_type = uploaded_file.name.lower()
    text = extract_text_from_pdf(io.BytesIO(file_bytes)) if file_type.endswith(".pdf") else extract_text_from_docx(io.BytesIO(file_bytes))
    name = extract_name(text)
    phones = extract_phone_numbers(text)
    emails = extract_emails(text)

    st.subheader("🧑‍💼 اسم المتقدم:")
    st.write(name)

    # Editable email and phone
    default_email = emails[0] if emails else ""
    default_phone = phones[0] if phones else ""

    email_input = st.text_input("📧 الإيميل (يمكنك التعديل):", value=default_email)
    phone_input = st.text_input("📱 رقم الجوال (يمكنك التعديل):", value=default_phone)

    if st.button("✉️ إرسال دعوة عبر الإيميل"):
        if email_input.strip() == "":
            st.error("🚫 الرجاء إدخال بريد إلكتروني.")
        else:
            date_str = date_input.strftime("%Y-%m-%d")
            time_str = time_input.strftime("%I:%M %p")
            result = send_email(email_input.strip(), date_str, time_str)
            st.success("📩 تم إرسال الدعوة.") if result is True else st.error(f"حدث خطأ أثناء الإرسال: {result}")
