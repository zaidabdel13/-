import streamlit as st
import pandas as pd
import smtplib
from email.message import EmailMessage
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(
    page_title="نظام دعوات المقابلة - تموين الشرق",
    layout="centered"
)

# تنسيقات CSS
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(
                135deg,
                rgba(0, 32, 91, 0.85),
                rgba(44, 62, 117, 0.85)
            );
            background-attachment: fixed;
        }
        h1, h2, h3 {
            color: #FDC82F;
            text-align: center;
        }
        label, body, div, p, span {
            color: white !important;
        }
        .stTextInput > div > div > input,
        .stTextArea > div > textarea,
        .stDateInput > div,
        .stSelectbox > div,
        .stFileUploader > div,
        .stFileUploader {
            background-color: #FDC82F !important;
            color: black !important;
            border-radius: 10px !important;
            padding: 10px !important;
        }
        .stButton > button {
            background-color: #FDC82F;
            color: #00205B;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("## 📨 نظام إرسال دعوات المقابلات - تموين الشرق")

# إدخال بيانات البريد
st.subheader("📧 بيانات البريد المرسل")
sender_email = st.text_input("الإيميل المرسل (Gmail)")
app_password = st.text_input("كلمة مرور التطبيق", type="password")

# رفع ملف Excel
st.subheader("📂 إرسال جماعي من ملف Excel")
excel_file = st.file_uploader("ارفع ملف Excel يحتوي على الأعمدة: email, date, time", type=["xlsx"])

if st.button("📨 إرسال جماعي"):
    if not excel_file:
        st.warning("⚠️ الرجاء رفع ملف Excel أولاً.")
    else:
        df = pd.read_excel(excel_file)
        success, failed = 0, 0

        for _, row in df.iterrows():
            try:
                msg = EmailMessage()
                msg['Subject'] = "دعوة لحضور مقابلة عمل"
                msg['From'] = sender_email
                msg['To'] = row['email']

                msg.set_content(f"""\
السلام عليكم ورحمة الله وبركاته،

نشكر لك اهتمامك بالتقدم على وظيفة في شركة تموين الشرق للتجارة.
يسرنا دعوتك لإجراء مقابلة عمل لمناقشة مؤهلاتك بشكل أوسع والتعرف عليك بشكل أفضل.

تفاصيل المقابلة:
📅 التاريخ: {row['date']}
⏰ الوقت: {row['time']}
📍الموقع: https://maps.app.goo.gl/meqgz4UdRxXAvc7T8

نأمل منكم الالتزام بالزي الرسمي السعودي واحضار نسخة من السيرة الذاتية.

نتطلع للقائك ونتمنى لك التوفيق....
""")

                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(sender_email, app_password)
                    smtp.send_message(msg)

                success += 1
            except Exception as e:
                failed += 1
                st.error(f"فشل الإرسال إلى {row['email']}: {e}")

        st.success(f"✅ تم إرسال {success} دعوة بنجاح.")
        if failed > 0:
            st.warning(f"❌ فشل إرسال {failed} دعوة.")

# إرسال يدوي لمرشح واحد
st.subheader("👤 إرسال يدوي لمرشح واحد")

with st.form("manual_form"):
    m_email = st.text_input("إيميل المرشح")
    m_date = st.date_input("تاريخ المقابلة")
    m_time = st.time_input("وقت المقابلة")
    m_resume = st.file_uploader("ارفع السيرة الذاتية", type=["pdf", "docx", "doc"], key="manual_resume")
    send_btn = st.form_submit_button("📤 إرسال الدعوة")

if send_btn:
    try:
        msg = EmailMessage()
        msg['Subject'] = "دعوة لحضور مقابلة عمل"
        msg['From'] = sender_email
        msg['To'] = m_email

        msg.set_content(f"""\
السلام عليكم ورحمة الله وبركاته،

نشكر لك اهتمامك بالتقدم على وظيفة في شركة تموين الشرق للتجارة.
يسرنا دعوتك لإجراء مقابلة عمل لمناقشة مؤهلاتك بشكل أوسع والتعرف عليك بشكل أفضل.

تفاصيل المقابلة:
📅 التاريخ: {m_date}
⏰ الوقت: {m_time}
📍الموقع: https://maps.app.goo.gl/meqgz4UdRxXAvc7T8

نأمل منكم الالتزام بالزي الرسمي السعودي واحضار نسخة من السيرة الذاتية.

نتطلع للقائك ونتمنى لك التوفيق....
""")

        if m_resume is not None:
            resume_data = m_resume.read()
            msg.add_attachment(resume_data, maintype="application", subtype="octet-stream", filename=m_resume.name)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, app_password)
            smtp.send_message(msg)

        st.success("✅ تم إرسال الدعوة بنجاح.")
    except Exception as e:
        st.error(f"❌ فشل الإرسال: {e}")

# تذييل
st.markdown("---")
st.caption("تم التطوير بواسطة زايد العبدلي ❤️")
