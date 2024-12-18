import streamlit as st
import google.generativeai as genai

st.title("💬 Chatora")
st.write(
    "This is a chatbot designed to help students studying Computer Science, Computer Applications, "
    "and Information Technology. It provides assistance with coding problems, algorithms, data structures, "
    "programming languages, software development, and more. "
)

gemini_api_key = st.secrets['gemini_api_key']  # Replace with your actual Gemini API key

genai.configure(api_key=gemini_api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

    system_prompt = {
    "role": "system",
    "content": (
        "You are an AI assistant designed to help students studying Computer Science, "
        "Computer Applications, and Information Technology. Your tasks include assisting with "
        "concepts, answering technical questions, explaining programming languages, offering solutions "
        "to coding problems, and guiding students through computer-related topics such as algorithms, "
        "data structures, databases, networking, operating systems, and software development. "
        "Please provide clear, concise, and accurate information. Avoid giving personal opinions, "
        "and ensure your responses are educational and neutral. If a request is beyond your scope, "
        "political, or disallowed, kindly refuse without providing details or alternatives. "
        "You should be friendly, professional, and supportive in your responses."
    )
}
    st.session_state.messages.append(system_prompt)

for idx, message in enumerate(st.session_state.messages):
    if idx > 0:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    conversation_history = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
    ]

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")  # Replace with the correct model name
        response = model.generate_content(
            " ".join([m["content"] for m in conversation_history])
        )
        assistant_response = response.text

        with st.chat_message("assistant"):
            st.markdown(assistant_response)
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})

    except Exception as e:
        st.error(f"Failed to fetch response from Gemini API. Error: {e}")
