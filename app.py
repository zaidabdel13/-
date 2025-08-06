import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

# عنوان التطبيق
st.title("📧 إرسال دعوات المقابلات تلقائيًا")

# شرح بسيط
st.write("ارفع ملف Excel يحتوي على الأعمدة التالية: Email، التاريخ، الوقت")

# رفع ملف الإكسل
uploaded_file = st.file_uploader("📂 رفع ملف Excel", type="xlsx")

# إدخال البريد الإلكتروني وكلمة مرور التطبيق
sender_email = st.text_input("📨 بريدك الإلكتروني (Gmail فقط)", placeholder="example@gmail.com")
app_password = st.text_input("🔑 كلمة مرور التطبيق (App Password)", type="password")

# بعد رفع الملف
if uploaded_file:
    try:
        # قراءة الملف
        df = pd.read_excel(uploaded_file)

        # التحقق من الأعمدة
        if not all(col in df.columns for col in ["Email", "التاريخ", "الوقت"]):
            st.error("❌ تأكد أن الأعمدة في الملف هي: Email، التاريخ، الوقت")
        else:
            st.success("✅ تم قراءة الملف بنجاح")

            # زر الإرسال
            if st.button("📤 إرسال الدعوات"):
                success_count = 0
                fail_count = 0

                # تكرار على كل مرشح
                for index, row in df.iterrows():
                    receiver_email = row["Email"]
                    date = row["التاريخ"]
                    time = row["الوقت"]

                    try:
                        # نص الرسالة
                        message = f"""\
السلام عليكم ورحمة الله وبركاته،

نشكر لك اهتمامك بالتقدم على وظيفة في شركة تموين الشرق للتجارة.
يسرنا دعوتك لإجراء مقابلة عمل لمناقشة مؤهلاتك بشكل أوسع والتعرف عليك بشكل أفضل.

📅 التاريخ: {date}
⏰ الوقت: {time}
📍الموقع: https://maps.app.goo.gl/meqgz4UdRxXAvc7T8

نأمل منكم الالتزام بالزي الرسمي السعودي واحضار نسخة من السيرة الذاتية.

نتطلع للقائك ونتمنى لك التوفيق."""

                        # بناء الرسالة
                        msg = MIMEMultipart()
                        msg['From'] = sender_email
                        msg['To'] = receiver_email
                        msg['Subject'] = Header("دعوة لمقابلة عمل", 'utf-8')
                        msg.attach(MIMEText(message, 'plain', 'utf-8'))

                        # الإرسال
                        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                            server.login(sender_email, app_password)
                            server.send_message(msg)

                        st.success(f"✅ تم إرسال الدعوة إلى: {receiver_email}")
                        success_count += 1

                    except Exception as e:
                        st.warning(f"⚠️ فشل إرسال إلى {receiver_email}: {e}")
                        fail_count += 1

                # ملخص
                st.info(f"📬 تم إرسال الدعوات إلى {success_count} مرشح بنجاح.")
                st.info(f"⚠️ تعذر إرسال الدعوات إلى {fail_count} مرشح.")

    except Exception as e:
        st.error(f"❌ حدث خطأ أثناء قراءة الملف: {e}")
