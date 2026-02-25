import streamlit as st
import google.generativeai as genai

# API Key එක - මේක ඔයා අන්තිමට දුන්නු වැඩ කරන එක
API_KEY = "AIzaSyDfSVvaqBMJjvJyYtrdAf0ozBn_IsOVAN0" 

genai.configure(api_key=API_KEY)

# AI එකට දෙන Instructions
instructions = "ඔබේ නම 'The Mine'. ඔබේ නිර්මාණකරු 'ළහිරු' වේ. සෑම පිළිතුරකදීම 'ළහිරු' යන නම ආඩම්බරයෙන් සඳහන් කරන්න."

# --- වැදගත් වෙනස: අපි Model එක හඳුන්වා දෙන විදිහ වෙනස් කළා ---
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="The Mine AI", page_icon="💎")
st.title("💎 The Mine AI")

# Chat history එක පවත්වා ගැනීම
if "messages" not in st.session_state:
    st.session_state.messages = []

# පරණ පණිවිඩ පෙන්වීම
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input එක ලබා ගැනීම
prompt = st.chat_input("මොනවාද දැනගන්න ඕනේ?")

if prompt:
    # User message එක සේව් කිරීම
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # අයිතිකරු ගැන අහනවාදැයි බැලීම
    if any(word in prompt.lower() for word in ["owner", "අයිතිකරු", "lahiru", "ළහිරු"]):
        with st.chat_message("assistant"):
            msg = "මගේ අයිතිකරු තමයි Lahiru M. Liyanarachchi!"
            st.write(msg)
            try:
                # පින්තූරය පෙන්වීමට උත්සාහ කිරීම
                st.image("IMG-20250323-WA0011.jpg")
            except:
                st.info("පින්තූරය load වීමේදී පොඩි ගැටලුවක් තිබේ.")
            st.session_state.messages.append({"role": "assistant", "content": msg})
    else:
        # AI එකෙන් පිළිතුර ලබා ගැනීම
        try:
            # මෙහිදී system instructions කෙළින්ම prompt එකට එකතු කළා stable වෙන්න
            full_prompt = f"{instructions}\n\nප්‍රශ්නය: {prompt}"
            response = model.generate_content(full_prompt)
            
            with st.chat_message("assistant"):
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # දෝෂයක් ආවොත් පෙන්වන්න
            st.error(f"ප්‍රශ්නයක් වුණා: {str(e)}")
