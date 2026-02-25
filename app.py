import streamlit as st
import google.generativeai as genai

# --- ඔයාගේ API Key එක පහළ ඇති quotation marks ඇතුළට දාන්න ---
API_KEY = "AIzaSyAYdOsxVR4v1J91u0o3ZyPjuHddjFBlhbg" # ඔයාගේ කලින් තිබුණ Key එක මෙතන තියෙයි

genai.configure(api_key=API_KEY)

# AI එකට දෙන උපදෙස්
instructions = """
ඔබේ නම 'The Mine'. ඔබේ නිර්මාණකරු 'ළහිරු' (Lahiru M. Liyanarachchi) වේ. 
සෑම පිළිතුරකදීම 'ළහිරු' යන නම ආඩම්බරයෙන් සඳහන් කරන්න.
"""

model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=instructions)

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

    # අයිතිකරු ගැන අහන විට ෆොටෝ එක පෙන්වීමට
    if any(word in prompt.lower() for word in ["owner", "අයිතිකරු", "lahiru", "ළහිරු"]):
        with st.chat_message("assistant"):
            st.write("මගේ අයිතිකරු තමයි Lahiru M. Liyanarachchi!")
            # මෙන්න මෙතන තිබුණ වැරදි වරහන මම අයින් කළා:
            st.image("IMG-20250323-WA0011.jpg", caption="Lahiru M. Liyanarachchi")
            st.session_state.messages.append({"role": "assistant", "content": "මගේ අයිතිකරු තමයි Lahiru M. Liyanarachchi!"})
    else:
        response = model.generate_content(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
