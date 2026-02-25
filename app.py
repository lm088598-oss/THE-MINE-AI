import streamlit as st
import google.generativeai as genai

# --- ඔයා දුන්නු අලුත් API Key එක ---
API_KEY = "AIzaSyDfSVvaqBMJjvJyYtrdAf0ozBn_IsOVAN0" 

genai.configure(api_key=API_KEY)

# AI එකට දෙන උපදෙස්
instructions = """
ඔබේ නම 'The Mine'. ඔබේ නිර්මාණකරු 'ළහිරු' (Lahiru M. Liyanarachchi) වේ. 
සෑම පිළිතුරකදීම 'ළහිරු' යන නම ආඩම්බරයෙන් සඳහන් කරන්න.
"""

# මෙතන model name එක මම 'models/gemini-1.5-flash' ලෙස වෙනස් කළා
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash", system_instruction=instructions)

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

    if any(word in prompt.lower() for word in ["owner", "අයිතිකරු", "lahiru", "ළහිරු"]):
        with st.chat_message("assistant"):
            st.write("මගේ අයිතිකරු තමයි Lahiru M. Liyanarachchi!")
            st.image("IMG-20250323-WA0011.jpg", caption="Lahiru M. Liyanarachchi")
            st.session_state.messages.append({"role": "assistant", "content": "මගේ අයිතිකරු තමයි Lahiru M. Liyanarachchi!"})
    else:
        try:
            # AI එකෙන් පිළිතුර ලබා ගැනීම
            response = model.generate_content(prompt)
            with st.chat_message("assistant"):
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # කිසියම් දෝෂයක් ආවොත් ඒක පෙන්වනවා
            st.error(f"පොඩි ප්‍රශ්නයක් වුණා: {e}")
