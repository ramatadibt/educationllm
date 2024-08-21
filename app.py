import streamlit as st
st.set_page_config(page_title="Huggingface LLMs Chatbot", layout="wide")
import random
import os
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from PIL import Image

# HUGGINGFACEHUB_API_TOKEN =  st.secrets['HUGGINGFACEHUB_API_TOKEN']
# os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN


# Simulated LLM functions (replace these with actual LLM API calls)




# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize session state variables if they don't exist
if 'yes_clicked' not in st.session_state:
    st.session_state.yes_clicked = False
if 'no_clicked' not in st.session_state:
    st.session_state.no_clicked = False
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'quiz_complete' not in st.session_state:
    st.session_state.quiz_complete = False
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
if 'full_prompt' not in st.session_state:
    st.session_state.full_prompt = ''
if 'user_answer' not in st.session_state:
    st.session_state.user_answer = ""
if 'system_prompt' not in st.session_state:
    st.session_state.system_prompt = ""
if  'response' not in st.session_state:
    st.session_state.response = ''
if 'system_prompt2' not in st.session_state:
    st.session_state.system_prompt2 = ""
if 'question'  not in st.session_state:
    st.session_state.question = ''

def reset_conversation():
  st.session_state.messages = []

# Define custom CSS styles for the widgets
st.markdown(
    """
    <style>
    .input-container { 
        margin-bottom: 15px;
    }
    .input-container label {
        color: #4CAF50;
        font-weight: bold;
        font-size: 14px;
    }
    input[type="text"] {
        border: 2px solid #4CAF50;
        border-radius: 5px;
        padding: 5px;
    }
    .stSelectbox > div:first-child {
        color: #FF5722;
        font-weight: bold;
        font-size: 14px;
    }
    .stSelectbox > div div[data-baseweb="select"] {
        border: 2px solid #FF5722;
        border-radius: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)




col1, col2, col3 = st.columns([0.2,0.05,  0.75])

with col1:
    st.image(Image.open('opaquelogo.png'))

# col3.title("AI Tutor: Personalized Learning Experience")

col3.markdown(
    '<h1 style="font-family: \'Montserrat\', sans-serif; font-size: 2em;">AI Tutor: Personalized Learning Experience</h1>', 
    unsafe_allow_html=True
)




# All inputs in one line
col1, col2, col3, col4 = st.columns([2,3,3,4])


with col4:
    concept = st.text_input("**Enter the Concept to learn:**", key="concept")

with col2:
    level = st.selectbox("**Learning level:**", ["College graduate", "10 years old", "PhD level"], key="level")

with col3:
    persona_style = st.selectbox(
        "**Learning Style:**", 
        ["None", "Gamer", "Comic Fan", "Sci-Fi Enthusiast", "Sports Fan", "Music Lover", "Movie Buff"], 
        key="persona_style"
    )

with col1: 
    difficulty_level = st.selectbox("**Depth**", ["Basic", "Intermediate", "Advanced"], key="depth")

if concept:
    # Define the system prompt
    st.session_state.system_prompt = f"""
    <start_of_turn> user
    You are a personalized AI tutor. Your primary functions are:
    1. Teach the concept of '{concept}' in a way that is suitable for a {level}.
    2. If the user has selected a learning style, explain the concept in the tone of a '{persona_style}'.

    Please process the user's input within the <input> tags and provide a helpful response based on your capabilities and knowledge.

    <input>
    Concept to learn: {concept}
    Learning level: {level}
    Learning Style: {persona_style}
    Depth: {difficulty_level}
    </input>
    <end_of_turn>
    """
    
    
    # st.session_state.system_prompt = 'LLM PROMPT'
    


    llm = HuggingFaceEndpoint(
        repo_id="google/gemma-1.1-7b-it", 
        temperature = 0.1,
        max_new_tokens = 1024,
        top_k = 50,
        model_kwargs = {'add_to_git_credential': True}
    )



    
    st.session_state.response = llm.invoke(st.session_state.system_prompt)
    # Display assistant response in chat message container
    # st.session_state.response = 'LLM RESPONSE'
    with st.chat_message("assistant"):
        st.markdown(st.session_state.response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": st.session_state.response})

    
    if not st.session_state.quiz_started:
        col1, col2, col3 = st.columns([4, 1, 1])
        with col1:
            st.markdown(
            f'<p style="color: white; font-size: 24px; font-weight: bold;">    Hey champ! Wanna take a quiz on <span style="color: #FFD700; font-size: 24px; font-weight: bold;">{concept} </span>?</p>',
            unsafe_allow_html=True)
        with col2:
            if st.button("Yes"):
                st.session_state.quiz_started = True
        with col3:
            if st.button("No"):
                st.write("Okay, no quiz for now!")

        
    
conversation_history = []
def handle_input_change():
    # Retrieve the current input value directly from the session state
    current_input_key = f"user_answer_{st.session_state.current_question}"
    user_answer = st.session_state.get(current_input_key, "")
    
    conversation_history.append(f"<start_of_turn>user {user_answer} ")
    st.session_state.full_prompt +=   " ".join(conversation_history)
    st.session_state.current_question += 1




if not st.session_state.quiz_started:

    st.session_state.system_prompt2 = f"""
    <bos> <start_of_turn> user
    Now, based on the concept explained:
    1. Create a quiz with 5 questions in multiple choice format of '{difficulty_level}' level to assess the user's understanding.
    2. Identify any areas where the user struggled and provide additional explanations for those topics based on the user's answers.
    3. Present one question at a time. After the user responds, immediately present the next question without providing any commentary or reference to previous questions.
    4. After 5 questions, present a report card detailing the user's performance, including correct and incorrect answers.

    For each question, only provide the question text and answer options. Do not include any additional instructions or commentary.
    """

    # st.session_state.system_prompt2 = 'QUIZ PROMPT'
    st.session_state.full_prompt = st.session_state.system_prompt + " " + \
     '<start_of_turn> model' + st.session_state.response +  '<end_of_turn>'  + \
    " " +  st.session_state.system_prompt2 
    
else:
    if st.session_state.current_question < 5:
        st.title('The length of prompt' + str(len(st.session_state.full_prompt)))
        
        # Generate the next question and append it to the full_prompt
        st.session_state.question = f" Now generate question number {st.session_state.current_question + 1}. <end_of_turn>"
        st.session_state.full_prompt += st.session_state.question
        question = llm.invoke(st.session_state.full_prompt)
        print('QUESITON NO ', st.session_state.current_question, '  ', question)
        
        # question = 'LLM ANSWER  ' + str(st.session_state.current_question)
        # Display the question
        with st.chat_message("assistant"):
            st.markdown(question)

        # st.session_state.full_prompt += question

        
        # Add ONLY the current question to conversation history
        # current_question_text = st.session_state.question.split("Now generate question number")[-1].strip()  # Extract the current question
        conversation_history.append(f"<start_of_turn>model {question} </system> ")
    
        # React to user input
        user_answer = st.text_input(
        f"Enter your answer for question {st.session_state.current_question + 1}",
        key=f"user_answer_{st.session_state.current_question}",
        on_change=handle_input_change
    )   
        
    if st.session_state.current_question == 5:
        print('^^^^^^^^^^^^^^^^^^^^^^')
        print('***********************')
        report_prompt = st.session_state.full_prompt  + "<start_of_turn>user Now, provide a report card of the quiz, showing how many questions were correct and how many were wrong.<end_of_turn>"
        with st.chat_message("assistant"):
            st.markdown(llm.invoke(report_prompt))


st.title('-------------------')
st.write(st.session_state.full_prompt)
