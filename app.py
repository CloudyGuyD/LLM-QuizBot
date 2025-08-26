import streamlit as st
import time
import json



#set the page layout to be centered
st.set_page_config(layout='centered', page_title="AI Quiz Generator")

#defaults to main page
if 'page' not in st.session_state:
    st.session_state.page = 'main' 


def dummy_quiz():
    #returns a dummy quiz for development purposes
    quiz = """
    {
        "quiz": [
            {
            "question": "What is the capital of Japan?",
            "options": [
                "Beijing",
                "Seoul",
                "Tokyo",
                "Bangkok"
            ],
            "answers": ["Tokyo"]
            },
            {
            "question": "What is the chemical symbol for water?",
            "options": [
                "H2O",
                "CO2",
                "O2",
                "NaCl"
            ],
            "answers": ["H2O"]
            },
            {
            "question": "Who was the first President of the United States?",
            "options": [
                "Thomas Jefferson",
                "Abraham Lincoln",
                "John Adams",
                "George Washington"
            ],
            "answers": ["George Washington"]
            }
        ]
    }
    """
    json_quiz = json.loads(quiz)
    return json_quiz


def load_question(question, num):
    #takes in a question (dict) and changes onscreen options to match the question
    st.subheader(f"Question {num}: {question['question']}")

    user_selections = []
    options = question['options']
    answers = question['answers']
    #columns for answer choices
    if len(answers) == 1:
        # single-choice answer
        user_choice = st.radio(
            "Select one answer:",
            options = options,
            key = f"q_{num}_radio",
            index=None
        )
        if user_choice:
            user_selections = [user_choice]    
    else: 
        #Multichoice answers, use checkbox
        st.write("Select all that apply:")
        for option in options:
            if st.checkbox(option, key=f"q_{num}_{option}"):
                user_selections.append(option)
    
    return user_selections

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

    #quiz creation
    if 'quiz_data' not in st.session_state:
        #text input for a topic
        topic = st.text_input("Enter the topic for your quiz (e.g., 'Photosynthesis')")

        if st.button("Generate Quiz!"):
            if topic: 
                #show a loading message
                with st.spinner(f"Generating a quiz about {topic}"):
                    time.sleep(3) #simulate LLM inference
                    st.success("Quiz generated successfully!")
                    #Initialize quiz
                    st.session_state.quiz_data = dummy_quiz()
                    st.session_state.q_index = 0
                    st.session_state.score = 0
                    st.session_state.q_answered = False
                st.rerun() # switch to quiz taking state
            else: 
                st.warning("Please enter a topic.")

    #quiz taking mode
    if 'quiz_data' in st.session_state:
        quiz_data = st.session_state.quiz_data

        if st.session_state.q_index >= len(quiz_data['quiz']):
            st.success(f"Quiz Complete! Your final score is {st.session_state.score} out of {len(quiz_data['quiz'])}.")
            if st.button("Generate another Quiz!"):
                for key in ['quiz_data', 'q_index', 'score', 'q_answered']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
            return

        q_index = st.session_state.q_index
        question = quiz_data['quiz'][q_index]
        user_answers = load_question(question, q_index+1)
        
        if not st.session_state.q_answered:
            if st.button("Check Answer"):
                st.session_state.q_answered = True
                correct_answers = set(question['answers'])
                if set(user_answers) == correct_answers:
                    st.session_state.score += 1
                    st.success("Correct!")
                else:
                    st.error(f"Incorrect, the correct answer(s) are {", ".join(correct_answers)}")
                st.rerun()
        
        if st.session_state.q_answered:
            if set(user_answers) == set(question['answers']):
                st.success("Correct!")
            else:
                st.error(f"Incorrect, the correct answer(s) are {", ".join(correct_answers)}")
            
            #navigate to next question
            if st.button("Next Question"):
                st.session_state.q_index += 1
                st.session_state.q_answered = False
                st.rerun()

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

