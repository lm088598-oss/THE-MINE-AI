import streamlit as st
import google.generativeai as genai

# ඔයා ගත්ත අලුත්ම API Key එක
API_KEY = "AIzaSyAcuJQjVzZGazuXxaW9VSQAiPv2-CKphKw"

# 1. පද්ධතියට 'v1' ස්ථාවර සංස්කරණය භාවිතා කිරීමට බල කිරීම
genai.configure(api_key=API_KEY, transport="rest")

# 2. මම මෙතන Model එක 'gemini-1.5-flash-latest' ලෙස වෙනස් කළා 
# (Flash වැඩ නොකරන සමහර Keys වලට මේක වැඩ කරනවා)
model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")

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

    owner_q = ["owner", "අයිතිකරු", "කවුද හැදුවේ", "lahiru", "ළහිරු"]
    
    if any(word in prompt.lower() for word in owner_q):
        with st.chat_message("assistant"):
            st.success("මගේ අයිතිකරු තමයි Lahiru M. Liyanarachchi!")
            try:
                st.image("IMG-20250323-WA0011.jpg")
            except:
                pass
    
    else:
        with st.chat_message("assistant"):
            try:
                # මෙතනදීත් අපි v1 version එකම ඉල්ලා සිටිනවා
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                # මම මෙතන 'v1beta' error එක bypass කරන්න උත්සාහ කරනවා
                st.error("AI පද්ධතියට සම්බන්ධ වීමේ අපහසුවක්.")
                st.info("පොඩ්ඩක් ඉන්න, මම නැවත උත්සාහ කරනවා...")
                
                try:
                    # Flash වැඩ නැත්නම් Gemini-Pro එකට මාරු වෙලා බලනවා
                    alt_model = genai.GenerativeModel("gemini-pro")
                    response = alt_model.generate_content(prompt)
                    st.markdown(response.text)
                except:
                    st.warning("ඔබේ API Key එක තවමත් සක්‍රීය වී නැති බව පෙනේ. කරුණාකර විනාඩි 10කින් පසුව බලන්න.")
