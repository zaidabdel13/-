import streamlit as st
import pandas as pd
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import fitz  # PyMuPDF
import docx2txt
from datetime import datetime

# إعداد البريد المرسل
SENDER_EMAIL = "zaid.hr.optc@gmail.com"
APP_PASSWORD = "ضع_كلمة_مرور_التطبيق_هنا"

st.set_page_config(page_title="نظام إرسال دعوات المقابلات", layout="centered")

st.title("📨 إرسال دعوات المقابلات للمرشحين")

# الدوال المساعدة
def extract_text_from_pdf(file):
    text = ""
    pdf = fitz.open(stream=file.read(), filetype="pdf")
    for page in pdf:
        text += page.get_text()
    return text

def extract_text_from_docx(file):
    return docx2txt.process(file)

def extract_info(text):
    phones = re.findall(r"(05\d{8})", text)
    emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    return phones, emails

def send_email(to_email, date_str, time_str):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = to_email
    msg['Subject'] = Header("دعوة لمقابلة عمل", 'utf-8')

    body = f"""\
السلام عليكم ورحمة الله وبركاته،

نشكر لك اهتمامك بالتقدم على وظيفة في شركة تموين الشرق للتجارة.
يسرنا دعوتك لإجراء مقابلة عمل لمناقشة مؤهلاتك بشكل أوسع والتعرف عليك بشكل أفضل.

تفاصيل المقابلة:
📅 التاريخ: {date_str}
⏰ الوقت: {time_str}
📍الموقع: https://maps.app.goo.gl/meqgz4UdRxXAvc7T8

نأمل منكم الالتزام بالزي الرسمي السعودي واحضار نسخة من السيرة الذاتية.

نتطلع للقائك ونتمنى لك التوفيق.
"""
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)

# واجهتين: جماعي وفردي
tab1, tab2 = st.tabs(["📋 إرسال جماعي (Excel)", "✉️ إرسال يدوي (مرشح واحد)"])

# tab1: جماعي من ملف Excel
with tab1:
    st.subheader("📎 ارفع ملف Excel فيه الأعمدة: Email، التاريخ، الوقت")
    excel_file = st.file_uploader("اختر ملف Excel", type="xlsx")

    if excel_file:
        try:
            df = pd.read_excel(excel_file)
            if not all(col in df.columns for col in ["Email", "التاريخ", "الوقت"]):
                st.error("❌ تأكد أن الأعمدة في الملف هي: Email، التاريخ، الوقت")
            else:
                if st.button("🚀 إرسال الدعوات"):
                    successes = 0
                    failures = 0
                    for _, row in df.iterrows():
                        email = row["Email"]
                        date = str(row["التاريخ"])
                        time = str(row["الوقت"])
                        try:
                            send_email(email, date, time)
                            st.success(f"✅ تم الإرسال إلى {email}")
                            successes += 1
                        except Exception as e:
                            st.warning(f"⚠️ فشل الإرسال إلى {email}: {e}")
                            failures += 1
                    st.info(f"📬 تمت العملية: {successes} نجاح / {failures} فشل")
        except Exception as e:
            st.error(f"❌ خطأ في قراءة الملف: {e}")

# tab2: إرسال يدوي لمرشح واحد
with tab2:
    st.subheader("📎 ارفع سيرة ذاتية واحدة (PDF أو Word)")
    file = st.file_uploader("السيرة الذاتية", type=["pdf", "docx"])

    if file:
        if file.name.endswith(".pdf"):
            text = extract_text_from_pdf(file)
        else:
            text = extract_text_from_docx(file)

        phones, emails = extract_info(text)

        st.write("📧 الإيميلات المستخرجة:", emails)
        st.write("📱 أرقام الجوال المستخرجة:", phones)

        email_input = st.text_input("📨 بريد المرشح", value=emails[0] if emails else "")
        interview_date = st.date_input("📅 تاريخ المقابلة", value=datetime.today())
        interview_time = st.text_input("⏰ وقت المقابلة", placeholder="مثال: 10:00 صباحًا")

        if st.button("✉️ إرسال الدعوة لهذا المرشح"):
            if email_input and interview_time:
                try:
                    send_email(email_input.strip(), interview_date.strftime("%Y-%m-%d"), interview_time)
                    st.success("✅ تم إرسال الدعوة بنجاح.")
                except Exception as e:
                    st.error(f"❌ فشل الإرسال: {e}")
            else:
                st.warning("يرجى إدخال البريد والوقت.")
