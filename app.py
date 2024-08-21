import streamlit as st
st.set_page_config(page_title="Huggingface LLMs Chatbot", layout="wide")
import random
import os
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from PIL import Image

HUGGINGFACEHUB_API_TOKEN =  st.secrets['HUGGINGFACEHUB_API_TOKEN']
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN


# Simulated LLM functions (replace these with actual LLM API calls)

import streamlit.components.v1 as components
from streamlit_extras.stylable_container import stylable_container



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

st.markdown(
    """
    <style>
    .concept-text {
        font-weight: bold;
        color: #FFD700;  /* Bright color for the concept */
        font-size: 20px;
    }
    .stButton > button {
        width: 120px;
        height: 50px;
        font-size: 18px;
        border-radius: 8px;
        margin: 5px;
    }
    .stButton > button:first-child {
        background-color: #28a745;  /* Green for Yes button */
        color: white;
    }
    .stButton > button:last-child {
        background-color: #dc3545;  /* Red for No button */
        color: white;
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
    system_prompt = f"""
    You are a personalized AI tutor. Your primary functions are:
    1. Teach the concept of '{concept}' in a way that is suitable for a {level}.
    2. If the user has selected a learning style, explain the concept in the tone of a '{persona_style}'.

    Please process the user's input within the <user> tags and provide a helpful response based on your capabilities and knowledge.

    <user>
    Concept to learn: {concept}
    Learning level: {level}
    Learning Style: {persona_style}
    Depth: {difficulty_level}
    </user>
    """
    


    llm = HuggingFaceEndpoint(
        repo_id="google/gemma-1.1-7b-it", 
        temperature = 0.1,
        max_new_tokens = 1024,
        top_k = 50,
        model_kwargs = {'add_to_git_credential': True}
    )

    #  # Display user message in chat message container
    # st.chat_message("user").markdown(prompt)
    # # Add user message to chat history
    # st.session_state.messages.append({"role": "user", "content": prompt})

    
    response = llm.invoke(system_prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

    col1, col2, col3, col4 = st.columns([1, 3,1, 1])

    if not st.session_state.quiz_started:
        col1, col2, col3, col4 = st.columns([1, 3, 1, 1])
        # with col2:
        #     st.text(f'Hey champ! Wanna take a quiz on {concept}')
        # with col3:
        #     if st.button("Yes"):
        #         st.session_state.quiz_started = True
        # with col4:
        #     if st.button("No"):
        #         st.write("Okay, no quiz for now!")

        with col2:
            st.markdown(f'<p style="color: white;">Hey champ! Wanna take a quiz on <span style="color: #FFD700;">{concept}</span>?</p>', unsafe_allow_html=True)
        
        with col3:
            with stylable_container(
                "green",
                css_styles="""
                button {
                    background-color: #28a745;  /* Green color for Yes button */
                    color: white;
                    font-size: 18px;
                    padding: 10px 20px;
                    border-radius: 8px;
                    width: 100px;
                }"""
            ):
                if st.button("Yes"):
                    st.session_state.quiz_started = True
        
        with col4:
            with stylable_container(
                "red",
                css_styles="""
                button {
                    background-color: #dc3545;  /* Red color for No button */
                    color: white;
                    font-size: 18px;
                    padding: 10px 20px;
                    border-radius: 8px;
                    width: 100px;
                }"""
            ):
                if st.button("No"):
                    st.write("Okay, no quiz for now!")


def handle_input_change():
    # Retrieve the current input value directly from the session state
    current_input_key = f"user_answer_{st.session_state.current_question}"
    user_answer = st.session_state.get(current_input_key, "")

    st.session_state.conversation_history.append(f"<User Answer>: {user_answer} </User Answer>")
    st.session_state.current_question += 1


if st.session_state.quiz_started:
    system_prompt2 = '''
    Now based on the concept explained
    1. Create a quiz with 5 questions in multiple choice format of '{difficulty_level}' level to assess the user's understanding.
    2. Identify any areas where the user struggled and provide additional explanations for those topics based on the answers the user give to you. 
    3. Give only one question at a time and one the user gives the response, give him the next question without revealing anything about the previous question. 
    4. Once the user has given the response for 5 questions, then give the report card of the quiz of how many questions were correct and how many were wrong. 
    
    '''

    # system_prompt2 = ''
    # if st.session_state.current_question < 5:
    #     # Combine all previous conversation history with the current prompts
    #     st.session_state.full_prompt = system_prompt + " " + response + " " + system_prompt2 + " " + " ".join(st.session_state.conversation_history)
        
    #     # Generate the next question
    #     st.session_state.full_prompt += f" Now generate question number {st.session_state.current_question + 1}."
    #     # question = llm.invoke(st.session_state.full_prompt)
    #     question = st.session_state.full_prompt
        
    #     # Display the question
    #     with st.chat_message("assistant"):
    #         st.markdown(question)
        
    #     # Add question to conversation history
    #     st.session_state.conversation_history.append(f"<AI Tutor Question>: {question} + </AI Tutor Question>: ")

    st.session_state.full_prompt = system_prompt + " " + response + " " + system_prompt2 + " " 
    if st.session_state.current_question < 5:
        st.title('The length of prompt' + str(len(st.session_state.full_prompt)))
        # Combine all previous conversation history with the current prompts
        st.session_state.full_prompt += " ".join(st.session_state.conversation_history)
        
        # Generate the next question
        st.session_state.full_prompt += f" Now generate question number {st.session_state.current_question + 1}."
        question = llm.invoke(st.session_state.full_prompt)
        print('QUESITON NO ', st.session_state.current_question, '  ', question)
        # question = st.session_state.full_prompt
        
        # Display the question
        with st.chat_message("assistant"):
            st.markdown(question)
        
        # Add ONLY the current question to conversation history
        current_question_text = question.split("Now generate question number")[-1].strip()  # Extract the current question
        st.session_state.conversation_history.append(f"<AI Tutor Question>: {current_question_text} + </AI Tutor Question>: ")
    
        # React to user input
        user_answer = st.text_input(
        f"Enter your answer for question {st.session_state.current_question + 1}",
        key=f"user_answer_{st.session_state.current_question}",
        on_change=handle_input_change
    )
        
      

        # if user_answer: 
        #     st.title(f'user_answer, {user_answer}') 
        #     st.session_state.full_prompt += '<User Answer: >' + user_answer + '</User Answer  3kd3i49384934eioruewiorsl>'
        #     st.session_state.conversation_history.append(f"<User Answer :>  {user_answer} + </User Answer>")
        #     st.session_state.current_question += 1
            
        # st.write(st.session_state.full_prompt)
        

        # user_answer = st.text_input(f"Enter your answer for question {st.session_state.current_question + 1}")
        # st.session_state.full_prompt += 'User Answer: ' + user_answer
        
        # # Add user's answer to conversation history
        # st.session_state.conversation_history.append(f"User: {user_answer}")
        # st.session_state.current_question += 1

    elif not st.session_state.quiz_complete:
        # After all questions, generate the report card
        report_prompt = st.session_state.full_prompt  + " Now, provide a report card of the quiz, showing how many questions were correct and how many were wrong."
        report = llm.invoke(report_prompt)
        # report = report_prompt
        
        with st.chat_message("assistant"):
            st.markdown(report)
        
        st.session_state.quiz_complete = True

    else:
        st.write("Quiz completed. Thank you for participating!")



st.write(st.session_state.full_prompt)
st.title('-------------------')
st.write(st.session_state.conversation_history)
   

