import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.set_page_config(page_title="إرسال دعوات المقابلات", layout="centered")

st.title("📧 إرسال دعوات المقابلات تلقائيًا")
st.markdown("ارفع ملف Excel يحتوي على الأعمدة: `Email`, `التاريخ`, `الوقت`")

uploaded_file = st.file_uploader("📄 رفع ملف Excel", type=["xlsx"])

# بيانات البريد (غيّرها بما يناسبك)
sender_email = "zaid.hr.optc@gmail.com"
sender_password = "اكتب_كلمة_مرور_التطبيق_هنا"

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)

        if "Email" not in df.columns or "التاريخ" not in df.columns or "الوقت" not in df.columns:
            st.error("❌ تأكد أن الأعمدة في الملف هي: Email، التاريخ، الوقت")
        else:
            st.success(f"✅ تم تحميل {len(df)} مرشح، جاهز للإرسال!")

            if st.button("🚀 إرسال الدعوات"):
                success_count = 0
                fail_count = 0

                for _, row in df.iterrows():
                    to_email = str(row["Email"]).strip()
                    interview_date = str(row["التاريخ"])
                    interview_time = str(row["الوقت"])

                    message = f"""\
السلام عليكم ورحمة الله وبركاته،

نشكر لك اهتمامك بالتقدم على وظيفة في شركة تموين الشرق للتجارة.
يسرنا دعوتك لإجراء مقابلة عمل لمناقشة مؤهلاتك بشكل أوسع والتعرف عليك بشكل أفضل.

تفاصيل المقابلة:
📅 التاريخ: {interview_date}
⏰ الوقت: {interview_time}
📍الموقع: https://maps.app.goo.gl/meqgz4UdRxXAvc7T8

نأمل منكم الالتزام بالزي الرسمي السعودي واحضار نسخة من السيرة الذاتية.

نتطلع للقائك ونتمنى لك التوفيق.
"""

                    msg = MIMEMultipart()
                    msg["From"] = sender_email
                    msg["To"] = to_email
                    msg["Subject"] = "دعوة لحضور مقابلة وظيفية"
                    msg.attach(MIMEText(message, "plain"))

                    try:
                        with smtplib.SMTP("smtp.gmail.com", 587) as server:
                            server.starttls()
                            server.login(sender_email, sender_password)
                            server.sendmail(sender_email, to_email, msg.as_string())
                        success_count += 1
                    except Exception as e:
                        fail_count += 1
                        st.error(f"⚠️ فشل إرسال إلى {to_email}: {e}")

                st.success(f"✅ تم إرسال الدعوة إلى {success_count} مرشح بنجاح.")
                if fail_count > 0:
                    st.warning(f"⚠️ تعذر إرسال الدعوة إلى {fail_count} مرشح.")

    except Exception as e:
        st.error(f"❌ حصل خطأ أثناء قراءة الملف: {e}")
