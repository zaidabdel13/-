import streamlit as st
import pandas as pd
import smtplib
from email.message import EmailMessage

# شعار الشركة (مضمن Base64)
logo_base64 = """
data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/...أكمل باقي الكود اللي عطيتني...
"""

# عرض الشعار والعنوان
st.markdown(
    f"<div style='text-align: center;'><img src='{logo_base64}' width='120'></div>",
    unsafe_allow_html=True
)
st.markdown("<h2 style='text-align: center;'>📩 نظام إرسال دعوات المقابلات - تموين الشرق</h2>", unsafe_allow_html=True)

# إعدادات البريد
st.subheader("📧 إعدادات البريد الإلكتروني (Gmail)")
sender_email = st.text_input("الإيميل المرسل")
app_password = st.text_input("كلمة مرور التطبيق", type="password")

# إرسال جماعي من Excel
st.subheader("📂 إرسال جماعي من ملف Excel")
excel_file = st.file_uploader("Upload Excel", type=["xlsx"])
if excel_file:
    df = pd.read_excel(excel_file)
    if all(col in df.columns for col in ["email", "date", "time"]):
        if st.button("إرسال الدعوات"):
            successes, failures = 0, 0
            for _, row in df.iterrows():
                try:
                    msg = EmailMessage()
                    msg['Subject'] = "دعوة لحضور المقابلة الشخصية"
                    msg['From'] = sender_email
                    msg['To'] = row["email"]
                    msg.set_content(
                        f"مرحبًا،\n\nنأمل حضوركم للمقابلة بتاريخ {row['date']} في تمام الساعة {row['time']}.\n\nمع تحيات قسم الموارد البشرية - تموين الشرق."
                    )

                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                        smtp.login(sender_email, app_password)
                        smtp.send_message(msg)
                    successes += 1
                except Exception as e:
                    failures += 1
                    st.warning(f"فشل الإرسال إلى {row['email']}: {e}")
            st.success(f"✅ تم إرسال {successes} دعوة، وفشل {failures}.")

    else:
        st.error("⚠️ الملف يجب أن يحتوي على الأعمدة: email, date, time")
