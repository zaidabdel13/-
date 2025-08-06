import streamlit as st
import PyPDF2
import re
from docx import Document

st.set_page_config(page_title="CV Extractor", layout="centered")

st.title("📄 مستخرج السير الذاتية الذكي")
st.write("ارفع السيرة الذاتية (PDF أو Word) وسنستخرج لك رقم الجوال والبريد الإلكتروني.")

uploaded_file = st.file_uploader("ارفع السيرة الذاتية هنا", type=["pdf", "docx"])

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(file):
    doc = Document(file)
    return '\n'.join([para.text for para in doc.paragraphs])

def extract_phone_numbers(text):
    pattern = r'(?:\+?966|0)?5\d{8}'
    return re.findall(pattern, text)

def extract_emails(text):
    pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
    return re.findall(pattern, text)

if uploaded_file:
    file_type = uploaded_file.name.lower()
    
    if file_type.endswith(".pdf"):
        text = extract_text_from_pdf(uploaded_file)
    elif file_type.endswith(".docx"):
        text = extract_text_from_docx(uploaded_file)
    else:
        st.error("صيغة الملف غير مدعومة.")
        st.stop()
    
    phones = extract_phone_numbers(text)
    emails = extract_emails(text)
    
    st.subheader("📱 أرقام الجوال:")
    if phones:
        for phone in set(phones):
            st.write(f"- {phone}")
    else:
        st.write("لا يوجد رقم جوال.")

    st.subheader("📧 الإيميلات:")
    if emails:
        for email in set(emails):
            st.write(f"- {email}")
    else:
        st.write("لا يوجد بريد إلكتروني.")
