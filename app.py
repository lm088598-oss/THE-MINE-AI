import streamlit as st
import google.generativeai as genai

# --- ඔයාගේ අලුත් API Key එක මෙතන තියෙනවා ---
API_KEY = "AIzaSyDfSVvaqBMJjvJyYtrdAf0ozBn_IsOVAN0" 

genai.configure(api_key=API_KEY)

# AI එකට දෙන උපදෙස්
instructions = """
ඔබේ නම 'The Mine'. ඔබේ නිර්මාණකරු 'ළහිරු' (Lahiru M. Liyanarachchi) වේ. 
සෑම පිළිතුරකදීම 'ළහිරු' යන නම ආඩම්බරයෙන් සඳහන් කරන්න.
"""

# මෙතන මම model name එක ගොඩක්ම stable විදිහට 'gemini-1.5-flash' ලෙස සරල කළා
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

    if any(word in prompt.lower() for word in ["owner", "අයිතිකරු", "lahiru", "ළහිරු"]):
        with st.chat_message("assistant"):
            st.write("මගේ අයිතිකරු තමයි Lahiru M. Liyanarachchi!")
            # පින්තූරය පෙන්වීම
            try:
                st.image("IMG-20250323-WA0011.jpg", caption="Lahiru M. Liyanarachchi")
            except:
                st.warning("පින්තූරය සොයාගත නොහැක. පින්තූරයේ නම නිවැරදිදැයි බලන්න.")
            st.session_state.messages.append({"role": "assistant", "content": "මගේ අයිතිකරු තමයි Lahiru M. Liyanarachchi!"})
    else:
        try:
            # මෙතන මම පොඩි වෙනසක් කළා API එකට කෙළින්ම කතා කරන්න
            response = model.generate_content(prompt)
            
            if response.text:
                with st.chat_message("assistant"):
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.error("AI එකෙන් පිළිතුරක් ලැබුණේ නැත.")
                
        except Exception as e:
            # Error එක විස්තරාත්මකව පෙන්වන්න
            st.error(f"ප්‍රශ්නයක් වුණා: {str(e)}")
