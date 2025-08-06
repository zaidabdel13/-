# باقي الكود نفسه ...

# خلفية بلون أزرق ملكي شفاف + لون خط أبيض
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
        label {
            color: white;
        }
        body, div, p, span {
            color: white !important;
        }
        .stTextInput > div > div > input,
        .stTextArea > div > textarea,
        .stDateInput > div,
        .stSelectbox > div {
            background-color: white;
            color: black;
        }
        .stButton > button {
            background-color: #FDC82F;
            color: #00205B;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)
