import streamlit as st
import google.generativeai as genai
import os

# 1. API Key එක (මෙය ක්‍රියාත්මක විය යුතුමයි)
API_KEY = "AIzaSyDfSVvaqBMJjvJyYtrdAf0ozBn_IsOVAN0"
genai.configure(api_key=API_KEY)

# 2. Model එක Configure කිරීම (අලුත්ම ක්‍රමය)
# මෙතැනදී අපි 'models/gemini-1.5-flash' යන සම්පූර්ණ නම භාවිතා කරනවා
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

st.set_page_config(page_title="The Mine AI", page_icon="💎")
st.title("💎 The Mine AI")

# Chat history එක පවත්වාගෙන යාම
if "messages" not in st.session_state:
    st.session_state.messages = []

# පරණ මැසේජ් පෙන්වීම
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("මොනවාද දැනගන්න ඕනේ?")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # අයිතිකරු ගැන අහනවා නම් (Direct Response)
    if any(word in prompt.lower() for word in ["owner", "අයිතිකරු", "ළහිරු", "lahiru"]):
        with st.chat_message("assistant"):
            st.write("මගේ අයිතිකරු තමයි Lahiru M. Liyanarachchi!")
            try:
                st.image("IMG-20250323-WA0011.jpg")
            except:
                pass
    
    # වෙනත් ඕනෑම ප්‍රශ්නයකට AI එකෙන් පිළිතුරු ලබා ගැනීම
    else:
        with st.chat_message("assistant"):
            try:
                # AI එකට උපදෙස් ලබා දීම
                chat_session = model.start_chat(history=[])
                response = chat_session.send_message(prompt)
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                # මෙතනදී එන error එක නිවැරදිව හඳුනා ගැනීමට
                st.error("AI පද්ධතියට සම්බන්ධ වීමට නොහැකි විය.")
                if "404" in str(e):
                    st.warning("ඔබේ API Key එක තවමත් සක්‍රීය වී නැත. කරුණාකර විනාඩි 5ක් ඉන්න.")
                else:
                    st.info(f"දෝෂය: {e}")
