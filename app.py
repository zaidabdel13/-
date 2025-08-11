import streamlit as st
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

# إعداد الصفحة
st.set_page_config(page_title="إرسال دعوات المقابلات تلقائياً - شركة تموين الشرق", layout="centered")

# خلفية برتقالي فاتح + دخان أزرق ملكي
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(
                135deg,
                rgba(255, 183, 77, 0.9) 0%,    /* برتقالي فاتح للعين */
                rgba(255, 204, 128, 0.9) 30%,  /* برتقالي أفتح */
                rgba(26, 35, 126, 0.6) 100%    /* أزرق ملكي شفاف مثل الدخان */
            );
            background-attachment: fixed;
            background-size: cover;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📩 إرسال دعوات المقابلات تلقائياً - شركة تموين الشرق")

st.markdown("### ✳️ إرسال جماعي من ملف Excel")
excel_file = st.file_uploader("📤 ارفع ملف Excel", type="xlsx")
st.markdown("**يجب أن يحتوي الملف على الأعمدة التالية:** `Email`, `التاريخ`, `الوقت`")

# إعدادات الإيميل
st.markdown("### ⚙️ إعدادات البريد الإلكتروني")
sender_email = st.text_input("✉️ الإيميل المرسل", value="zaid.hr.optc@gmail.com")
app_password = st.text_input("🔑 كلمة مرور التطبيق", type="password")

# زر إرسال (مثال)
if st.button("🚀 إرسال الدعوات"):
    if excel_file is not None and sender_email and app_password:
        df = pd.read_excel(excel_file)
        st.success(f"📤 تم تجهيز {len(df)} دعوة للإرسال!")
    else:
        st.error("⚠️ الرجاء إدخال جميع البيانات المطلوبة وتحميل ملف Excel.")
