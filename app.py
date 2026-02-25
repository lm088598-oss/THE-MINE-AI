import streamlit as st
import google.generativeai as genai

# 1. ඔයාගේ අලුත් API Key එක මෙතනට දැම්මා
API_KEY = "AIzaSyAcuJQjVzZGazuXxaW9VSQAiPv2-CKphKw"
genai.configure(api_key=API_KEY)

# 2. Model එක ස්ථාවරව හඳුන්වා දීම
# Gemini-1.5-flash කියන එක තමයි දැන් තියෙන වේගවත්ම එක
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="The Mine AI", page_icon="💎")
st.title("💎 The Mine AI")

# Chat history එක පවත්වාගෙන යාම
if "messages" not in st.session_state:
    st.session_state.messages = []

# කලින් කතා කරපු දේවල් screen එකේ පෙන්වීම
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User ගෙන් input එක ලබා ගැනීම
prompt = st.chat_input("මොනවාද දැනගන්න ඕනේ?")

if prompt:
    # User ගේ message එක එකතු කිරීම
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- අයිතිකරු ගැන ප්‍රශ්නයක් නම් (කෙලින්ම ක්‍රියාත්මක වේ) ---
    owner_keywords = ["owner", "අයිතිකරු", "කවුද හැදුවේ", "lahiru", "ළහිරු", "aitikaru"]
    
    if any(word in prompt.lower() for word in owner_keywords):
        with st.chat_message("assistant"):
            response_text = "මගේ අයිතිකරු තමයි Lahiru M. Liyanarachchi!"
            st.success(response_text)
            try:
                # ඔයාගේ photo එක මෙතනින් පෙන්වනවා
                st.image("IMG-20250323-WA0011.jpg", caption="Founder: Lahiru M. Liyanarachchi")
            except:
                st.info("පින්තූරය (IMG-20250323-WA0011.jpg) සොයාගත නොහැක.")
            
            st.session_state.messages.append({"role": "assistant", "content": response_text})

    # --- වෙනත් ඕනෑම ප්‍රශ්නයකට AI පිළිතුරු ලබා ගැනීම ---
    else:
        with st.chat_message("assistant"):
            try:
                # AI එකට උපදෙස් දී පිළිතුර ලබා ගැනීම
                full_prompt = f"ඔබේ නම 'The Mine'. ඔබේ නිර්මාණකරු 'ළහිරු'. ප්‍රශ්නය: {prompt}"
                response = model.generate_content(full_prompt)
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                # කිසියම් දෝෂයක් ආවොත් පමණක් මෙය පෙන්වයි
                st.error("කණගාටුයි, AI පද්ධතියට සම්බන්ධ වීමේදී දෝෂයක් ඇති විය.")
                st.caption(f"Technical Error: {e}")
