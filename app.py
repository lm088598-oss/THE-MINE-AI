import streamlit as st
import google.generativeai as genai

# 1. API Key එක (මෙය එහෙම්ම තියෙන්න හරින්න)
API_KEY = "AIzaSyDfSVvaqBMJjvJyYtrdAf0ozBn_IsOVAN0"
genai.configure(api_key=API_KEY)

# Page Settings
st.set_page_config(page_title="The Mine AI", page_icon="💎")
st.title("💎 The Mine AI")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("මොනවාද දැනගන්න ඕනේ?")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- අයිතිකරු ගැන අහන කොටස (මෙතන කිසිම Error එකක් එන්නේ නැහැ) ---
    owner_keywords = ["owner", "අයිතිකරු", "කවුද හැදුවේ", "lahiru", "ළහිරු", "aitikaru", "kawda"]
    
    if any(word in prompt.lower() for word in owner_keywords):
        with st.chat_message("assistant"):
            st.success("මගේ අයිතිකරු තමයි Lahiru M. Liyanarachchi!")
            try:
                st.image("IMG-20250323-WA0011.jpg")
            except:
                st.info("Photo එක තාම Upload කරලා නැහැ වගේ.")
            st.session_state.messages.append({"role": "assistant", "content": "Lahiru M. Liyanarachchi"})

    # --- වෙනත් ප්‍රශ්න වලට AI පිළිතුරු (Error එකක් ආවොත් පෙන්වන්නේ නැත) ---
    else:
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            with st.chat_message("assistant"):
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except:
            with st.chat_message("assistant"):
                st.write("සමාවෙන්න, මට දැන් පිළිතුරක් දෙන්න බැහැ. පසුව උත්සාහ කරන්න.")
