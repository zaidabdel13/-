import streamlit as st
import PyPDF2
import pytesseract
from PIL import Image
from pdf2image import convert_from_bytes
import re
from docx import Document
import io

st.set_page_config(page_title="CV Extractor with OCR", layout="centered")
st.title("📄 مستخرج السير الذاتية الذكي (يدعم PDF المصور)")
st.write("ارفع السيرة الذاتية (PDF أو Word)، وسنستخرج لك رقم الجوال والبريد الإلكتروني حتى لو الملف مصور.")

uploaded_file = st.file_uploader("ارفع السيرة الذاتية هنا", type=["pdf", "docx"])

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ''
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

def extract_text_from_docx(file):
    doc = Document(file)
    return '\n'.join([para.text for para in doc.paragraphs])

def extract_text_with_ocr(file_bytes):
    images = convert_from_bytes(file_bytes)
    text = ''
    for img in images:
        text += pytesseract.image_to_string(img, lang='eng+ara')
    return text

def extract_phone_numbers(text):
    pattern = r'(?:\+?966|0)?5\d{8}'
    return re.findall(pattern, text)

def extract_emails(text):
    pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
    return re.findall(pattern, text)

if uploaded_file:
    file_bytes = uploaded_file.read()
    file_type = uploaded_file.name.lower()

    if file_type.endswith(".pdf"):
        # نحاول استخراج النص أولاً بشكل طبيعي
        text = extract_text_from_pdf(io.BytesIO(file_bytes))
        if not text.strip():
            # لو ما فيه نص، نستخدم OCR
            st.warning("يبدو أن الملف عبارة عن صورة، نستخدم OCR لاستخراج النص...")
            text = extract_text_with_ocr(file_bytes)
    elif file_type.endswith(".docx"):
        text = extract_text_from_docx(io.BytesIO(file_bytes))
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
