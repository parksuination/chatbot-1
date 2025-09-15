import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("🤪 맛춘뻡 파괘 쳇봍")
st.write(
    "이 챗봇은 올바른 맞춤법의 문장을 일부러 틀린 맞춤법으로 바꿔주는 재미있는 앱입니다. "
    "OpenAI API 키가 필요하며, [여기서](https://platform.openai.com/account/api-keys) 얻을 수 있습니다."
)

# Ask user for their OpenAI API key via `st.text_input`.
openai_api_key = st.text_input("OpenAI API Key", type="password")

if not openai_api_key:
    st.info("계속하려면 OpenAI API 키를 입력해주세요.", icon="🗝️")
else:
    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)
    
    # Create a session state variable to store the chat messages.
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Create a chat input field
    if prompt := st.chat_input("올바른 맞춤법의 문장을 입력하세요..."):
        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Create system message for spelling destruction
        system_message = {
            "role": "system", 
            "content": """당신은 맞춤법을 일부러 틀리게 만드는 전문가입니다. 
            사용자가 입력한 올바른 한국어 문장을 받아서 다음과 같은 방식으로 맞춤법을 틀리게 만들어주세요:

            1. 받침 생략하기 (예: "있다" → "잇다", "좋다" → "조타")
            2. 된소리/거센소리 바꾸기 (예: "빠르다" → "파르다", "크다" → "그다")
            3. 모음 바꾸기 (예: "어서" → "어써", "그래서" → "그레서")
            4. 띄어쓰기 틀리기 (예: "할 수 있다" → "할수잇다")
            5. 비슷한 소리의 글자로 바꾸기 (예: "의" → "에", "를" → "을")
            
            자연스럽게 틀린 맞춤법처럼 보이도록 만들어주세요. 너무 과하지 않게 적당히 틀려야 합니다.
            오직 맞춤법만 틀리게 하고, 문장의 의미는 유지해주세요."""
        }
        
        # Prepare messages for API call
        api_messages = [system_message] + [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]
        
        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=api_messages,
            stream=True,
        )
        
        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
