import streamlit as st
import pandas as pd
import smtplib
import base64
from email.message import EmailMessage
from datetime import datetime

# شعار الشركة
st.image("24A1BA1E-0E3F-4F87-A866-2691E01CE1D5.jpeg", width=150)
st.markdown("<h2 style='text-align: center;'>إرسال دعوات المقابلات تلقائيًا</h2>", unsafe_allow_html=True)

st.header("📤 إرسال جماعي من ملف Excel")

excel_file = st.file_uploader("ارفع ملف Excel يحتوي على Email، التاريخ، الوقت", type=["xlsx"])
st.divider()

st.header("📧 إعدادات البريد الإلكتروني")
sender_email = st.text_input("الإيميل المرسل", value="", key="sender_email")
app_password = st.text_input("كلمة مرور التطبيق", type="password", key="app_password")

st.divider()
st.header("👤 إدخال يدوي لمرشح")

manual_email = st.text_input("البريد الإلكتروني للمرشح")
manual_date = st.date_input("تاريخ المقابلة", format="YYYY-MM-DD")
manual_time = st.time_input("وقت المقابلة")
manual_files = st.file_uploader("رفع السيرة الذاتية (PDF أو Word)", type=["pdf", "docx"], accept_multiple_files=True)

# محتوى الإيميل
def compose_email_body(date, time):
    return f"""\
السلام عليكم ورحمة الله وبركاته،

نشكر لك اهتمامك بالتقدم على وظيفة في شركة تموين الشرق للتجارة .
يسرنا دعوتك لإجراء مقابلة عمل لمناقشة مؤهلاتك بشكل أوسع والتعرف عليك بشكل أفضل.

تفاصيل المقابلة:
📅 التاريخ: {date}
⏰ الوقت: {time}
📍الموقع: [https://maps.app.goo.gl/meqgz4UdRxXAvc7T8]

نأمل منكم الالتزام بالزي الرسمي السعودي واحضار نسخة من السيرة الذاتية.

نتطلع للقائك ونتمنى لك التوفيق...
"""

def send_email(receiver, subject, body, sender_email, app_password, attachments=[]):
    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = receiver
        msg.set_content(body)
        msg.set_charset('utf-8')

        for file in attachments:
            file_data = file.read()
            file_name = file.name
            msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, app_password)
            smtp.send_message(msg)
        return True
    except Exception as e:
        st.warning(f"فشل الإرسال إلى {receiver}: {e}")
        return False

# إرسال يدوي
if st.button("📨 إرسال الدعوة اليدوية"):
    if manual_email and manual_date and manual_time:
        formatted_date = manual_date.strftime("%Y-%m-%d")
        formatted_time = manual_time.strftime("%I:%M %p")
        body = compose_email_body(formatted_date, formatted_time)
        result = send_email(
            receiver=manual_email,
            subject="دعوة لمقابلة وظيفية",
            body=body,
            sender_email=sender_email,
            app_password=app_password,
            attachments=manual_files
        )
        if result:
            st.success("تم إرسال الدعوة بنجاح.")
    else:
        st.warning("يرجى تعبئة جميع الحقول.")

# إرسال جماعي
if st.button("📤 إرسال الدعوات من ملف Excel"):
    if excel_file is not None:
        df = pd.read_excel(excel_file)

        required_cols = ["Email", "التاريخ", "الوقت"]
        if not all(col in df.columns for col in required_cols):
            st.error("❌ تأكد أن الأعمدة في الملف هي: Email ، التاريخ ، الوقت")
        else:
            success_count = 0
            for _, row in df.iterrows():
                email = row["Email"]
                date = str(row["التاريخ"])
                time = str(row["الوقت"])
                body = compose_email_body(date, time)
                if send_email(
                    receiver=email,
                    subject="دعوة لمقابلة وظيفية",
                    body=body,
                    sender_email=sender_email,
                    app_password=app_password
                ):
                    success_count += 1

            st.success(f"✅ تم إرسال الدعوات إلى {success_count} مرشح بنجاح.")
    else:
        st.warning("يرجى رفع ملف Excel أولاً.")
