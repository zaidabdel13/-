import streamlit as st
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

# إعداد الصفحة
st.set_page_config(page_title="إرسال دعوات المقابلات تلقائياً - شركة تموين الشرق", layout="centered")

# خلفية برتقالي فاتح + دخان أزرق ملكي (استبدال الخلفية فقط)
st.markdown("""
    <style>
        .stApp {
            background:
                radial-gradient(at 20% 30%, rgba(26, 35, 126, 0.18) 0%, rgba(26, 35, 126, 0) 40%),
                radial-gradient(at 80% 70%, rgba(26, 35, 126, 0.15) 0%, rgba(26, 35, 126, 0) 45%),
                linear-gradient(135deg,
                    rgba(255, 183, 77, 0.95) 0%,
                    rgba(255, 204, 128, 0.95) 40%,
                    rgba(26, 35, 126, 0.45) 100%
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
company_name = st.text_input("🏢 اسم الشركة", value="شركة تموين الشرق للتجارة")
location_link = st.text_input("📍رابط الموقع", value="https://maps.app.goo.gl/meqgz4UdRxXAvc7T8")

# إرسال جماعي من Excel
if excel_file:
    try:
        df = pd.read_excel(excel_file)

        if not {'Email', 'التاريخ', 'الوقت'}.issubset(df.columns):
            st.error("❌ تأكد أن الأعمدة في الملف هي: Email، التاريخ، الوقت.")
        else:
            if st.button("📨 إرسال الدعوات"):
                success, fail = 0, 0
                for _, row in df.iterrows():
                    to = row['Email']
                    date = str(row['التاريخ']).split(' ')[0]
                    time = row['الوقت']
                    body = f"""\
السلام عليكم ورحمة الله وبركاته،

نشكر لك اهتمامك بالتقدم على وظيفة في {company_name}.
يسرنا دعوتك لإجراء مقابلة عمل لمناقشة مؤهلاتك بشكل أوسع والتعرف عليك بشكل أفضل.

تفاصيل المقابلة:
📅 التاريخ: {date}
⏰ الوقت: {time}
📍الموقع: {location_link}

نأمل منكم الالتزام بالزي الرسمي السعودي وإحضار نسخة من السيرة الذاتية.

نتطلع للقائك ونتمنى لك التوفيق.
"""

                    msg = MIMEMultipart()
                    msg['From'] = sender_email
                    msg['To'] = to
                    msg['Subject'] = "دعوة لحضور مقابلة شخصية"
                    msg.attach(MIMEText(body, 'plain', _charset='utf-8'))

                    try:
                        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                            server.login(sender_email, app_password)
                            server.sendmail(sender_email, to, msg.as_string())
                        st.success(f"✅ تم إرسال الدعوة إلى {to}")
                        success += 1
                    except Exception as e:
                        st.warning(f"⚠️ فشل الإرسال إلى {to}: {e}")
                        fail += 1

                st.info(f"✅ تم الإرسال إلى {success} مرشح / ❌ فشل الإرسال إلى {fail}")
    except Exception as e:
        st.error(f"حدث خطأ أثناء قراءة الملف: {e}")

# إدخال يدوي
st.markdown("---")
st.markdown("### ✳️ إرسال يدوي لمرشح واحد")
manual_email = st.text_input("📧 بريد المرشح")
manual_date = st.date_input("📅 تاريخ المقابلة")
manual_time = st.time_input("⏰ وقت المقابلة")

if st.button("📨 إرسال الدعوة يدويًا"):
    body = f"""\
السلام عليكم ورحمة الله وبركاته،

نشكر لك اهتمامك بالتقدم على وظيفة في {company_name}.
يسرنا دعوتك لإجراء مقابلة عمل لمناقشة مؤهلاتك بشكل أوسع والتعرف عليك بشكل أفضل.

تفاصيل المقابلة:
📅 التاريخ: {manual_date}
⏰ الوقت: {manual_time.strftime('%H:%M')}
📍الموقع: {location_link}

نأمل منكم الالتزام بالزي الرسمي السعودي وإحضار نسخة من السيرة الذاتية.

نتطلع للقائك ونتمنى لك التوفيق.
"""
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = manual_email
    msg['Subject'] = "دعوة لحضور مقابلة شخصية"
    msg.attach(MIMEText(body, 'plain', _charset='utf-8'))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, manual_email, msg.as_string())
        st.success("✅ تم إرسال الدعوة بنجاح.")
    except Exception as e:
        st.error(f"❌ فشل الإرسال: {e}")
