import streamlit as st
import google.generativeai as genai

# API Key එක
API_KEY = "AIzaSyDfSVvaqBMJjvJyYtrdAf0ozBn_IsOVAN0"

# API එක Configure කරන කොට පරණ v1beta වෙනුවට v1 පාවිච්චි කරන්න බල කිරීම
genai.configure(api_key=API_KEY, transport="rest") 

# Model එක හඳුන්වා දීම
model = genai.GenerativeModel('gemini-1.5-flash')

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
    if any(word in prompt.lower() for word in ["owner", "අයිතිකරු", "ළහිරු", "lahiru"]):
        with st.chat_message("assistant"):
            st.success("මගේ අයිතිකරු තමයි Lahiru M. Liyanarachchi!")
            try:
                st.image("IMG-20250323-WA0011.jpg")
            except:
                st.info("පින්තූරය සොයාගත නොහැක.")
    
    # AI පිළිතුරු ලබා ගැනීම
    else:
        with st.chat_message("assistant"):
            try:
                # මෙතැනදී instructions එකතු කරලා උත්තරය ගමු
                full_prompt = f"ඔබේ නම The Mine. ඔබේ නිර්මාණකරු ළහිරු. ප්‍රශ්නය: {prompt}"
                response = model.generate_content(full_prompt)
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                # ඇත්තටම වෙන ප්‍රශ්නය මොකක්ද කියලා බලාගන්න
                st.error("AI පද්ධතියේ දෝෂයකි.")
                st.caption(f"Error details: {e}")
