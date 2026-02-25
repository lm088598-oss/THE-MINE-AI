import streamlit as st
import google.generativeai as genai

# 1. API Key එක (මෙය එහෙම්ම තියෙන්න හරින්න)
API_KEY = "AIzaSyDfSVvaqBMJjvJyYtrdAf0ozBn_IsOVAN0"
genai.configure(api_key=API_KEY)

# 2. Model එක නිවැරදිව හඳුන්වා දීම
try:
    model = genai.GenerativeModel("gemini-1.5-flash")
except:
    model = genai.GenerativeModel("models/gemini-1.5-flash")

# Page එකේ සැකසුම්
st.set_page_config(page_title="The Mine AI", page_icon="💎")
st.title("💎 The Mine AI")

# AI එකට දෙන පොදු උපදෙස්
instructions = "ඔබේ නම 'The Mine'. ඔබේ නිර්මාණකරු 'ළහිරු' (Lahiru M. Liyanarachchi) වේ."

# Chat history එක මතක තබා ගැනීම
if "messages" not in st.session_state:
    st.session_state.messages = []

# කලින් කතා කරපු දේවල් පෙන්වීම
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User ගෙන් ප්‍රශ්නය ලබා ගැනීම
prompt = st.chat_input("මොනවාද දැනගන්න ඕනේ?")

if prompt:
    # User ගේ ප්‍රශ්නය Chat එකේ පෙන්වීම
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- අයිතිකරු ගැන අහනවා නම් (මෙය AI එකට යන්නේ නැතිව කෙළින්ම වැඩ කරයි) ---
    owner_keywords = ["owner", "අයිතිකරු", "කවුද හැදුවේ", "lahiru", "ළහිරු", "aitikaru", "kawda"]
    
    if any(word in prompt.lower() for word in owner_keywords):
        with st.chat_message("assistant"):
            response_text = "මගේ අයිතිකරු තමයි Lahiru M. Liyanarachchi!"
            st.markdown(f"**{response_text}**")
            try:
                # ඔයාගේ Photo එක මෙතනින් පෙන්වයි
                st.image("IMG-20250323-WA0011.jpg", caption="Lahiru M. Liyanarachchi")
            except:
                st.warning("පින්තූරය (IMG-20250323-WA0011.jpg) සොයාගත නොහැකි විය. එය එකම Folder එකේ තියෙනවාදැයි බලන්න.")
            
            st.session_state.messages.append({"role": "assistant", "content": response_text})

    # --- වෙනත් ප්‍රශ්න සඳහා AI භාවිතා කිරීම ---
    else:
        try:
            full_prompt = f"{instructions}\n\nපරිශීලකයාගේ ප්‍රශ්නය: {prompt}"
            response = model.generate_content(full_prompt)
            
            with st.chat_message("assistant"):
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("AI සම්බන්ධතාවයේ දෝෂයක් පවතී.")
            st.info(f"Technical Error: {e}")
