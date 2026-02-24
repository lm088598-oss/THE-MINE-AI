import streamlit as st
import google.generativeai as genai

# --- මෙතනට ඔයාගේ API Key එක දාන්න ---
API_KEY = "AIzaSyBmlbUS2TmfPKYhNVPJekL1RhoaXE70X7c" # ඔයාගේ Key එක මෙතන තියෙනවා නේද?

genai.configure(api_key=API_KEY)

# AI එකට දෙන උපදෙස්
instructions = """
ඔබේ නම 'The Mine'. ඔබේ නිර්මාණකරු ළහිරු එම් ලියනආරච්චි  (Lahiru m liyanaarachchi) ය. 
සෑම පිළිතුරකදීම 'ළහිරු' යන නම ආමන්ත්‍රණය කරමින් ඉතා සුහදව කතා කරන්න.
"""

model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=instructions)

st.set_page_config(page_title="The Mine AI", page_icon="💎")

# පින්තූරය සහ නම පෙන්වීම
st.title("💎 The Mine AI")
st.image("IMG-20250323-WA0011.jpg" caption="The Mine නිර්මාණකරු: ළහිරු", width=150)
st.write(f"ආයුබෝවන් ළහිරු! මම 'The Mine'. මම ඔයාට උදව් කරන්න සූදානම්.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("මොකක්ද වෙන්න ඕනේ?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
