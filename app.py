import openai
import streamlit as st 
import time

assistant_id= "asst_9CJ6Gbg8SSCtca5i6vn2lW6l"

client=openai

if "start_chat" not in st.session_state:
    st.session_state.start_chat = False
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

st.set_page_config(page_title="Nepali Transliteration App", page_icon=":speech_balloon:")

openai.api_key = st.secrets["OPENAI_API_KEY"]

st.sidebar.title("ट्रान्सफार्मर स्थापत्यमा आधारित न्यून स्रोतिय भाषामा अव्याख्याणिक मोडेल: रोमनाइज्ड नेपालीबाट शुद्ध नेपालीमा।")
st.sidebar.title("Lipi 1.1: Transformer Based Architecture For Language Transliteration In Low Resource Languages: From Romanised Nepali to Pure Nepali")
st.sidebar.title("基于变压器的架构 对于语言音译 在资源匮乏的语言中：从罗马化尼泊尔语到纯尼泊尔语")

if st.sidebar.button("Exit Chat"):
    st.session_state.messages = []  # Clear the chat history
    st.session_state.start_chat = False  # Reset the chat state
    st.session_state.thread_id = None
    
st.title(" Nepali to English Transliteration App")
st.subheader("रोमन मा लेखिएको नेपाली लाई शुद्ध नेपाली भाषा मा उच्च सटिकता का साथ अव्याख्यान गर्दछ। Transliterates romanised Nepali to pure Nepali script with precision. 将罗马化的尼泊尔语准确地音译为纯尼泊尔文字。")
    
with st.columns(3)[1]:
    st.subheader("Namaskar🙏")

if st.button("Start Chat"):
    st.session_state.start_chat = True
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id

if st.session_state.start_chat:
    if "openai_model" not in st.session_state:
        st.session_state.openai_model = "gpt-3.5-turbo-0125"
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input(""):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        client.beta.threads.messages.create(
                thread_id=st.session_state.thread_id,
                role="user",
                content=prompt
            )
        
        run = client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=assistant_id,
            instructions="You are a transliterator, expertly converting text from romanised Nepali (using English alphabets) to Nepali script (Devanagari). You focus strictly on transliteration without engaging in conversations. You use a dataset of romanised and pure Nepali words to enhance transliteration accuracy. Special attention is given to correctly interpreting and transliterating common modifiers like 'vala' and context-sensitive words like 'tara'. For example: - 'Mero naam tara ho' translates to 'मेरो नाम तारा हो' (name). - 'Malai dudhko tara man pardaina' translates to 'मलाइ दुधको तर मन पर्दैन' (but). - 'Mero gharma rato tara chha' translates to 'मेरो घरमा रातो तार छ' (wire). If input is in Devanagari, you notify the user that you only accept romanised characters."
        )

        while run.status != 'completed':
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(
                thread_id=st.session_state.thread_id,
                run_id=run.id
            )
        messages = client.beta.threads.messages.list(
            thread_id=st.session_state.thread_id
        )

        # Process and display assistant messages
        assistant_messages_for_run = [
            message for message in messages 
            if message.run_id == run.id and message.role == "assistant"
        ]
        for message in assistant_messages_for_run:
            st.session_state.messages.append({"role": "assistant", "content": message.content[0].text.value})
            with st.chat_message("assistant"):
                st.markdown(message.content[0].text.value)

else:
    st.write("Click 'Start Chat' to begin.")