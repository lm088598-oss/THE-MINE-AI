import streamlit as st
import google.generativeai as genai

# API Key එක (මෙය නිවැරදිව තැබිය යුතුය)
API_KEY = "AIzaSyDfSVvaqBMJjvJyYtrdAf0ozBn_IsOVAN0" 

genai.configure(api_key=API_KEY)

# AI උපදෙස්
instructions = "ඔබේ නම 'The Mine'. ඔබේ නිර්මාණකරු 'ළහිරු' වේ. සෑම පිළිතුරකදීම 'ළහිරු' යන නම සඳහන් කරන්න."

# මෙන්න මෙතන තමයි වැරැද්ද තිබුණේ - අපි මාදිලිය නිවැරදිව හඳුන්වමු
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

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
            msg = "මගේ අයිතිකරු තමයි Lahiru M. Liyanarachchi!"
            st.write(msg)
            try:
                st.image("IMG-20250323-WA0011.jpg")
            except:
                pass
            st.session_state.messages.append({"role": "assistant", "content": msg})
    else:
        try:
            # AI එකෙන් පිළිතුරක් ඉල්ලීම (System instruction එක මෙතනට දාමු)
            full_prompt = f"{instructions}\n\nUser: {prompt}"
            response = model.generate_content(full_prompt)
            
            with st.chat_message("assistant"):
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"ප්‍රශ්නයක් වුණා: {e}")
