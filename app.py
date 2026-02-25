import streamlit as st
import google.generativeai as genai

# ඔයාගේ API Key එක
API_KEY = "AIzaSyDfSVvaqBMJjvJyYtrdAf0ozBn_IsOVAN0"
genai.configure(api_key=API_KEY)

# AI එකට දෙන උපදෙස්
instructions = "ඔබේ නම 'The Mine'. ඔබේ නිර්මාණකරු 'ළහිරු' වේ. සෑම පිළිතුරකදීම 'ළහිරු' යන නම ආඩම්බරයෙන් සඳහන් කරන්න."

# --- මෙන්න මෙතන මම වෙනසක් කළා (Version Error එක නැති කරන්න) ---
try:
    model = genai.GenerativeModel("gemini-1.5-flash")
except:
    model = genai.GenerativeModel("models/gemini-1.5-flash")

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
            try:
                st.image("IMG-20250323-WA0011.jpg")
            except:
                pass
    else:
        try:
            # මෙතන full prompt එක කෙළින්ම යවනවා stable වෙන්න
            full_prompt = f"{instructions}\n\nUser Question: {prompt}"
            response = model.generate_content(full_prompt)
            
            with st.chat_message("assistant"):
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # මෙතනදී Error එකක් ආවොත්, ඒක මොකක්ද කියලා ලෙහෙසියෙන් බලාගමු
            st.error(f"පොඩි ප්‍රශ්නයක් වුණා: {str(e)}")
