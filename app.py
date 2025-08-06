import streamlit as st
import pandas as pd
import smtplib
from email.message import EmailMessage
from datetime import datetime

# شعار "تموين الشرق" بصيغة base64
st.image("data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBwgHBgkI...<اختصرنا هنا عشان ما يطول الرد>...", width=150)

# عنوان الصفحة
st.markdown("<h2 style='text-align: center;'>📩 نظام إرسال دعوات المقابلات - تموين الشرق</h2>", unsafe_allow_html=True)

st.divider()

# إعدادات البريد
st.subheader("📧 إعدادات البريد الإلكتروني (Gmail)")
sender_email = st.text_input("الإيميل المرسل")
app_password = st.text_input("كلمة مرور التطبيق", type="password")

st.divider()

# إرسال جماعي من Excel
st.subheader("📂 إرسال جماعي من ملف Excel")
excel_file = st.file_uploader("ارفع ملف Excel (يحتوي على الأعمدة: Email، التاريخ، الوقت)", type=["xlsx"])

if st.button("📨 إرسال جماعي"):
    if excel_file and sender_email and app_password:
        df = pd.read_excel(excel_file)
        required_columns = {"Email", "التاريخ", "الوقت"}
        if not required_columns.issubset(df.columns):
            st.error("❌ تأكد أن ملف Excel يحتوي على الأعمدة: Email، التاريخ، الوقت")
        else:
            success = 0
            for _, row in df.iterrows():
                email = row["Email"]
                date = str(row["التاريخ"])
                time = str(row["الوقت"])
                msg = EmailMessage()
                msg["Subject"] = "دعوة لمقابلة وظيفية"
                msg["From"] = sender_email
                msg["To"] = email
                msg.set_content(f"""\
السلام عليكم ورحمة الله وبركاته،

نشكر لك اهتمامك بالتقدم على وظيفة في شركة تموين الشرق للتجارة .
يسرنا دعوتك لإجراء مقابلة عمل لمناقشة مؤهلاتك بشكل أوسع والتعرف عليك بشكل أفضل.

تفاصيل المقابلة:
📅 التاريخ: {date}
⏰ الوقت: {time}
📍الموقع: https://maps.app.goo.gl/meqgz4UdRxXAvc7T8

نأمل منكم الالتزام بالزي الرسمي السعودي واحضار نسخة من السيرة الذاتية.

نتطلع للقائك ونتمنى لك التوفيق...
""", charset="utf-8")

                try:
                    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                        smtp.login(sender_email, app_password)
                        smtp.send_message(msg)
                    success += 1
                except Exception as e:
                    st.warning(f"⚠️ فشل الإرسال إلى {email} - {e}")

            st.success(f"✅ تم إرسال الدعوات إلى {success} مرشح بنجاح.")
    else:
        st.warning("الرجاء تعبئة كل الحقول المطلوبة.")

st.divider()

# إدخال يدوي
st.subheader("✍️ إرسال يدوي")

manual_email = st.text_input("إيميل المرشح")
manual_date = st.date_input("📅 تاريخ المقابلة")
manual_time = st.time_input("⏰ وقت المقابلة")
uploaded_files = st.file_uploader("📎 رفع السيرة الذاتية (يمكن اختيار أكثر من ملف)", type=["pdf", "docx"], accept_multiple_files=True)

if st.button("📨 إرسال يدوي"):
    if manual_email and manual_date and manual_time:
        formatted_date = manual_date.strftime("%Y-%m-%d")
        formatted_time = manual_time.strftime("%I:%M %p")
        msg = EmailMessage()
        msg["Subject"] = "دعوة لمقابلة وظيفية"
        msg["From"] = sender_email
        msg["To"] = manual_email
        msg.set_content(f"""\
السلام عليكم ورحمة الله وبركاته،

نشكر لك اهتمامك بالتقدم على وظيفة في شركة تموين الشرق للتجارة .
يسرنا دعوتك لإجراء مقابلة عمل لمناقشة مؤهلاتك بشكل أوسع والتعرف عليك بشكل أفضل.

تفاصيل المقابلة:
📅 التاريخ: {formatted_date}
⏰ الوقت: {formatted_time}
📍الموقع: https://maps.app.goo.gl/meqgz4UdRxXAvc7T8

نأمل منكم الالتزام بالزي الرسمي السعودي واحضار نسخة من السيرة الذاتية.

نتطلع للقائك ونتمنى لك التوفيق...
""", charset="utf-8")

        for file in uploaded_files:
            msg.add_attachment(file.read(), maintype="application", subtype="octet-stream", filename=file.name)

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(sender_email, app_password)
                smtp.send_message(msg)
            st.success("✅ تم إرسال الدعوة بنجاح.")
        except Exception as e:
            st.error(f"⚠️ فشل الإرسال: {e}")
    else:
        st.warning("الرجاء تعبئة جميع الحقول.")
import streamlit as st

st.markdown(
    """
    <style>
    /* الخلفية */
    .stApp {
        background-color: #f4f4f4;
    }

    /* العنوان */
    h1, h2, h3 {
        color: #00205B;
    }

    /* الأزرار */
    div.stButton > button {
        background-color: #FDC82F;
        color: #00205B;
        border: none;
        padding: 0.6em 1.2em;
        border-radius: 6px;
        font-weight: bold;
    }
    div.stButton > button:hover {
        background-color: #e0b122;
        color: white;
    }

    /* مربعات الإدخال */
    .stTextInput > div > div > input,
    .stTextArea > div > textarea,
    .stDateInput > div,
    .stSelectbox > div {
        background-color: white;
        border: 2px solid #8C6239;
        border-radius: 4px;
        color: #00205B;
    }

    /* تسميات الحقول */
    label {
        font-weight: 600;
        color: #00205B;
    }
    </style>
    """,
    unsafe_allow_html=True
)
