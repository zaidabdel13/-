import streamlit as st
import PyPDF2
import re
from docx import Document
import io
import smtplib
from email.mime.text import MIMEText

st.set_page_config(page_title="CV Extractor + Email", layout="centered")
st.title("📄 مستخرج السير الذاتية الذكي + دعوة عبر الإيميل")
st.write("ارفع السيرة الذاتية (PDF أو Word)، واستخرج الاسم، رقم الجوال، الإيميل، ثم أرسل دعوة تلقائيًا.")

uploaded_file = st.file_uploader("ارفع السيرة الذاتية هنا", type=["pdf", "docx"])

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

def send_email(to_email, name):
    sender_email = "zaid.hr.optc@gmail.com"
    sender_password = "iytzknowcgmzkhbe"

    subject = "دعوة لمقابلة عمل"
    body = f"أهلًا {name},\n\nيسعدنا دعوتك لحضور مقابلة عمل يوم الأحد الساعة 10 صباحًا.\n\nتحياتنا،\nفريق الموارد البشرية"

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

    st.subheader("📱 أرقام الجوال:")
    st.write(phones if phones else "لا يوجد رقم جوال.")

    st.subheader("📧 الإيميلات:")
    st.write(emails if emails else "لا يوجد بريد إلكتروني.")

    if emails:
        if st.button("✉️ إرسال دعوة عبر الإيميل"):
            result = send_email(emails[0], name)
            st.success("📩 تم إرسال الدعوة.") if result is True else st.error(f"خطأ: {result}")
