import streamlit as st
import google.generativeai as genai

# API Key එක
API_KEY = "AIzaSyDfSVvaqBMJjvJyYtrdAf0ozBn_IsOVAN0"
genai.configure(api_key=API_KEY)

# AI එකට දෙන උපදෙස්
instructions = "ඔබේ නම 'The Mine'. ඔබේ නිර්මාණකරු 'ළහිරු' (Lahiru M. Liyanarachchi) වේ."

# Model එක නිවැරදි නම සහිතව හඳුන්වා දීම (Error එක මඟහරවා ගැනීමට)
try:
    # මෙතන 'gemini-1.5-flash-latest' ලෙස වෙනස් කර ඇත
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
except Exception:
    model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="The Mine AI", page_icon="💎")
st.title("💎 The Mine AI")

# Chat history එක පවත්වාගෙන යාම
if "messages" not in st.session_state:
    st.session_state.messages = []

# කලින් කතා කරපු දේවල් පෙන්වීම
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("මොනවාද දැනගන්න ඕනේ?")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # අයිතිකරු ගැන විමසන විට
    if any(word in prompt.lower() for word in ["owner", "අයිතිකරු", "lahiru", "ළහිරු"]):
        with st.chat_message("assistant"):
            response_text = "මගේ අයිතිකරු තමයි Lahiru M. Liyanarachchi!"
            st.write(response_text)
            try:
                st.image("IMG-20250323-WA0011.jpg")
            except:
                pass
            st.session_state.messages.append({"role": "assistant", "content": response_text})
            
    else:
        try:
            # AI එකෙන් පිළිතුර ලබා ගැනීම
            full_prompt = f"{instructions}\n\nUser Question: {prompt}"
            response = model.generate_content(full_prompt)
            
            with st.chat_message("assistant"):
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # තවමත් error එකක් එනවා නම් එය පෙන්වීමට
            st.error(f"ප්‍රශ්නයක් වුණා: {e}")
