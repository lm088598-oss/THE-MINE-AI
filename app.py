import streamlit as st
import google.generativeai as genai

# API Key එක (මෙය කාටවත් පෙනෙන්නට තැබීමෙන් වළකින්න)
API_KEY = "AIzaSyDfSVvaqBMJjvJyYtrdAf0ozBn_IsOVAN0"
genai.configure(api_key=API_KEY)

# AI එකට දෙන උපදෙස්
instructions = "ඔබේ නම 'The Mine'. ඔබේ නිර්මාණකරු 'ළහිරු' (Lahiru M. Liyanarachchi) වේ."

# Model එක හඳුන්වා දීම (Error එක වැළැක්වීමට 'gemini-1.5-flash' වෙනුවට අලුත්ම version එක භාවිතා කර ඇත)
try:
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception:
    model = genai.GenerativeModel("models/gemini-1.5-flash")

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
    # User ගේ message එක chat එකට එකතු කිරීම
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # අයිතිකරු ගැන අහනවා නම් කෙලින්ම පිළිතුරු දීම
    owner_keywords = ["owner", "අයිතිකරු", "lahiru", "ළහිරු", "කවුද හැදුවේ"]
    if any(word in prompt.lower() for word in owner_keywords):
        with st.chat_message("assistant"):
            response_text = "මගේ අයිතිකරු තමයි Lahiru M. Liyanarachchi!"
            st.write(response_text)
            try:
                st.image("IMG-20250323-WA0011.jpg")
            except:
                st.warning("අයිතිකරුගේ පින්තූරය සොයාගත නොහැකි විය.")
            
            st.session_state.messages.append({"role": "assistant", "content": response_text})
    
    # වෙනත් ප්‍රශ්න වලට AI හරහා පිළිතුරු ලබා ගැනීම
    else:
        try:
            full_prompt = f"{instructions}\n\nපරිශීලකයාගේ ප්‍රශ්නය: {prompt}"
            response = model.generate_content(full_prompt)
            
            with st.chat_message("assistant"):
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # Model error එකක් ආවොත් පෙන්වන message එක
            st.error("කණගාටුයි, AI සම්බන්ධතාවයේ දෝෂයක් පවතී. කරුණාකර මොහොතකින් නැවත උත්සාහ කරන්න.")
            st.info(f"Technical Error: {e}")
