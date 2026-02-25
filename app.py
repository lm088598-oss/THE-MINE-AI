import streamlit as st
import google.generativeai as genai

# API Key එක
API_KEY = "AIzaSyDfSVvaqBMJjvJyYtrdAf0ozBn_IsOVAN0"
genai.configure(api_key=API_KEY)

# --- මෙන්න මෙතනයි වෙනස තියෙන්නේ ---
# පද්ධතිය විසින් පිළිගන්නා ඕනෑම නමක් සොයා ගැනීමට උත්සාහ කරයි
model_to_use = "gemini-1.5-flash" # Default නම

try:
    # Google විසින් ලබා දෙන models list එක පරීක්ෂා කිරීම
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    if 'models/gemini-1.5-flash' in available_models:
        model_to_use = 'models/gemini-1.5-flash'
    elif 'models/gemini-pro' in available_models:
        model_to_use = 'models/gemini-pro'
except:
    # List එක ගන්න බැරි වුණොත් වඩාත් ස්ථාවර නම පාවිච්චි කරයි
    model_to_use = "gemini-pro" 

model = genai.GenerativeModel(model_to_use)

# Page Setup
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

    # 1. අයිතිකරු ගැන අහනවා නම් (මෙය කෙලින්ම ක්‍රියා කරයි)
    owner_keywords = ["owner", "අයිතිකරු", "කවුද හැදුවේ", "lahiru", "ළහිරු", "aitikaru"]
    if any(word in prompt.lower() for word in owner_keywords):
        with st.chat_message("assistant"):
            res = "මගේ අයිතිකරු තමයි Lahiru M. Liyanarachchi!"
            st.markdown(f"**{res}**")
            try:
                st.image("IMG-20250323-WA0011.jpg")
            except:
                pass
            st.session_state.messages.append({"role": "assistant", "content": res})

    # 2. වෙනත් ප්‍රශ්න සඳහා
    else:
        try:
            # 'instructions' වෙනුවට කෙලින්ම prompt එක යවමු තහවුරු කරගන්න
            response = model.generate_content(f"ඔබේ නම 'The Mine'. නිර්මාණකරු 'ළහිරු'. ප්‍රශ්නය: {prompt}")
            with st.chat_message("assistant"):
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # තවමත් error එකක් එනවා නම් නම මාරු කරමු
            st.error("AI තාක්ෂණික දෝෂයක්. කරුණාකර 'gemini-pro' ලෙස මාරු වී නැවත උත්සාහ කරන්න.")
            st.info(f"Model used: {model_to_use} | Error: {e}")
