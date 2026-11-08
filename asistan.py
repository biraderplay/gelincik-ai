from google import genai
from openai import OpenAI
import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(page_title="Birader AI - Çoklu Beyin", page_icon="🧠")
st.title("🧠 Birader AI (Çoklu Beyin Merkezi)")
st.write("Google Gemini ve OpenAI güçlerini tek bir çatı altında birleştirdik!")

# Kenar Çubuğu (Model Seçimi İçin)
st.sidebar.header("Kontrol Paneli")
secilen_model = st.sidebar.selectbox(
    "Hangi Yapay Zekayı Kullanmak İstersin?",
    ("Google Gemini (Hızlı & Güncel)", "OpenAI ChatGPT (Mantıksal & Kod)")
)

# API Anahtarları
GEMINI_KEY = "AQ.Ab8RN6J3jWYhfktmuHttVd0hhZLtDxcETir-ff12IzDFiguCXg"
OPENAI_KEY = "AQ.Ab8RN6J3jWYhfktmuHttVd0hhZLtDxcETir-ff12IzDFiguCXg"

# İstemcileri Hazırlıyoruz
gemini_client = genai.Client(api_key=GEMINI_KEY)
openai_client = OpenAI(api_key=OPENAI_KEY)

# Sohbet Geçmişi
if "messages" not in st.session_state:
    st.session_state.messages = []

# Eski mesajları ekrana yazdır
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcı mesaj yazdığında
if prompt := st.chat_input("Bir şeyler sorun..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    cevap = ""

    with st.chat_message("assistant"):
        try:
            # Hangi modeli seçtiyse ona göre istek atıyoruz
            if "Gemini" in secilen_model:
                response = gemini_client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt,
                )
                cevap = response.text
            else:
                response = openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}]
                )
                cevap = response.choices[0].message.content

            st.markdown(cevap)
            st.session_state.messages.append({"role": "assistant", "content": cevap})

        except Exception as e:
            hata_mesaji = f"Bir hata oluştu: {e}"
            st.markdown(hata_mesaji)
            st.session_state.messages.append({"role": "assistant", "content": hata_mesaji})
