import streamlit as st
import google.generativeai as genai

# --- මෙතනට ඔයාගේ API Key එක දාන්න ---
API_KEY = "AIzaSyBmlbUS2TmfPKYhNVF..." # ඔයාගේ කලින් තිබුණ Key එක මෙතන තියෙයි

genai.configure(api_key=API_KEY)

# AI එකට දෙන උපදෙස්
instructions = """
ඔබේ නම 'The Mine'. ඔබේ නිර්මාණකරු 'ළහිරු එම් ලියනආරච්චි' (Lahiru M. Liyanaarachchi) වේ. 
සෑම පිළිතුරකදීම 'ළහිරු' යන නම ආඩම්බරයෙන් සඳහන් කරන්න.
"""

model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=instructions)

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

    if "owner" in prompt.lower() or "අයිතිකරු" in prompt or "lahiru" in prompt.lower():
        with st.chat_message("assistant"):
            st.write("මගේ අයිතිකරු තමයි Lahiru M. Liyanaarachchi!")
            st.image("IMG-20250323-WA0011.jpg", caption="Lahiru M. Liyanarachchi")
    else:
        response = model.generate_content(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
