import streamlit as st
import time

#set the page layout to be centered:
st.set_page_config(layout='centered', page_title="AI Quiz Generator")

#defaults to main page
if 'page' not in st.session_state:
    st.session_state.page = 'main' 

#function for main page, displays two navigation buttons
def main_page():
    st.title("Welcome to the AI Quiz Generator!")
    st.write("Choose your quiz generation method below.")
    
    #two columns for the buttons to appear side by side
    col1, col2 = st.columns(2)

    with col1:
        #if clicked, change the page to topic_quiz
        if st.button("Generate Quiz from a Topic", use_container_width=True):
            st.session_state.page = "topic_quiz"
            st.rerun()
    
    with col2:
        #if clicked, change the page to file_quiz
        if st.button("Generate Quiz from a File", use_container_width=True):
            st.session_state.page = "file_quiz"
            st.rerun()
    
def topic_quiz_page():
    #displays ui for generating quiz from a topic
    st.title("Generate Quiz From Topic")

    #text input for a topic
    topic = st.text_input("Enter the topic for your quiz (e.g., 'Photosynthesis')")

    if st.button("Generate Quiz!"):
        if topic: 
            #show a loading message
            with st.spinner(f"Generating a quiz about {topic}"):
                time.sleep(3) #simulate LLM inference
            st.success("Quiz generated successfully!")
            #INSERT QUIZ LAYOUT AND QUESTIONS


        else: 
            st.warning("Please enter a topic.")
    
    #go back to main menu
    if st.button("← Back to Main Menu"):
        st.session_state.page = 'main'
        st.rerun()

def file_quiz_page():
    #displays the ui for file upload and quiz generation

    st.title("Generate Quiz from File")

    #file upload
    uploaded_file = st.file_uploader("Choose a file (.txt or .pdf)", type=['txt', 'pdf'])

    topic = st.text_input("Enter a topic from the file (e.g., 'Photosynthesis')")

    if st.button("Generate Quiz!"):
        if topic: 
            #show a loading message
            with st.spinner(f"Generating a quiz about {topic}"):
                time.sleep(3) #simulate LLM inference
            st.success("Quiz generated successfully!")
            #INSERT QUIZ LAYOUT AND QUESTIONS


        else: 
            st.warning("Please upload a file and enter a topic.")
    
    #go back to main menu
    if st.button("← Back to Main Menu"):
        st.session_state.page = 'main'
        st.rerun()

if st.session_state.page == 'main':
    main_page()
elif st.session_state.page == 'topic_quiz':
    topic_quiz_page()
elif st.session_state.page == 'file_quiz':
    file_quiz_page()
