import streamlit as st
import google.generativeai as genai

# ඔයා අන්තිමට ගත්ත අලුත් API Key එක
API_KEY = "AIzaSyAcuJQjVzZGazuXxaW9VSQAiPv2-CKphKw"

# මෙන්න මෙතනයි වැදගත්ම වෙනස! 
# අපි Google එකට කියනවා v1beta පාවිච්චි කරන්න එපා කියලා.
genai.configure(api_key=API_KEY, transport="rest")

# Model එක හඳුන්වා දීම
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

st.set_page_config(page_title="The Mine AI", page_icon="💎")
st.title("💎 The Mine AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("මොනවාද දැනගන්න ඕනේ?")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # අයිතිකරු ගැන අහනවා නම්
    owner_q = ["owner", "අයිතිකරු", "කවුද හැදුවේ", "lahiru", "ළහිරු"]
    if any(word in prompt.lower() for word in owner_q):
        with st.chat_message("assistant"):
            st.success("මගේ අයිතිකරු තමයි Lahiru M. Liyanarachchi!")
            try: st.image("IMG-20250323-WA0011.jpg")
            except: pass
    
    # AI පිළිතුරු ලබා ගැනීම (Stable version එකෙන්)
    else:
        with st.chat_message("assistant"):
            try:
                # කෙලින්ම පිළිතුර ගමු
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                # මොකක් හරි වුණොත් හරියටම පෙන්වන්න
                st.error("AI තාක්ෂණික දෝෂයක්.")
                st.info(f"Technical Log: {e}")
