import streamlit as st
import helper
import requests
 
# Set the title of the Streamlit page
st.title("YouChat")
api_host = "http://localhost:8000"
 
# Step 1: User inputs a YouTube link
youtube_url = st.text_input("Enter YouTube video URL")
 
 
if "messages" not in st.session_state:
    st.session_state.messages = []
if "transcript" not in st.session_state:
    st.session_state.transcript = None
 

 
# Function to simulate fetching transcript (dummy text in this example)
def fetch_transcript(url):
    # response = requests.post(f"{api_host}/transcribe", json={"youtube_url": youtube_url})
    response = helper.generateText(youtube_url)
    return response
   # return "Dummy transcript based on the video at " + url
 
# Only proceed with the chatbot interface if a YouTube URL has been entered
 
if youtube_url and st.session_state.transcript is None:
    st.session_state.transcript = fetch_transcript(youtube_url)
    st.session_state.messages = []
 
if st.session_state.transcript:
    # Display the fetched transcript (you might want to hide this in production)
    st.write("The chat bot is ready to answer your questions")
    # st.write(st.session_state.transcript)
 
    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
 
    # User input field for the chat
    prompt = st.chat_input("Type your question...")
 
    # Process the user input
    if prompt:
        # Add user message to chat history and display it
        user_message = {"role": "user", "content": prompt}
        st.session_state.messages.append(user_message)
        with st.chat_message("user"):
            st.markdown(prompt)
 
        # Send query to backend API
        # response = requests.post(f"{api_host}/query", json={"query": prompt, "transcript": st.session_state.transcript}).json()
        response = helper.query_transcript(st.session_state.transcript, prompt)
        # Display assistant response in chat message container
        assistant_message = {"role": "assistant", "content": response}
        with st.chat_message("assistant"):
            st.markdown(response)
 
        # Add assistant response to chat history
        st.session_state.messages.append(assistant_message)