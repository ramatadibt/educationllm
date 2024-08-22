import streamlit as st
st.set_page_config(page_title="Huggingface LLMs Chatbot", layout="wide")
import random
import os
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from PIL import Image

# HUGGINGFACEHUB_API_TOKEN =  st.secrets['HUGGINGFACEHUB_API_TOKEN']
# os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN

st.markdown("""
        <style>
               .block-container {
                    padding-top: 1.5rem;
                    padding-left: 3rem;
                    padding-right: 3rem;
                    padding-bottom: -1rem;
                }
        </style>
        """, unsafe_allow_html=True)


st.markdown("""
<style>
.stButton > button {
  background-color: #4CAF50; /* Green */
  border: solid;
  color: black;
  padding: 11px 15px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 32px;
  border-radius: 12px;
  transition-duration: 0.4s;
}

.stButton > button:hover {
  background-color: black; /* Change to black on hover */
  box-shadow: 0 12px 16px 0 rgba(0,0,0,0.24), 0 17px 50px 0 rgba(0,0,0,0.19);
  color: red; /* Change the font color to red on hover */
  font-weight: bold; /* Make the font bold on hover */
}
</style>
""", unsafe_allow_html=True)


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
if  'quiz_rejection' not in st.session_state:
    st.session_state.quiz_rejection = False


def reset_conversation():
    st.session_state.yes_clicked = False
    st.session_state.no_clicked = False
    st.session_state.current_question = 0
    st.session_state.quiz_complete = False
    st.session_state.conversation_history = []
    st.session_state.quiz_started = False
    st.session_state.full_prompt = ''
    st.session_state.user_answer = ""
    st.session_state.system_prompt = ""
    st.session_state.response = ''
    st.session_state.system_prompt2 = ""
    st.session_state.question = ''
    st.session_state.concept = ''

  

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

col3.markdown(
    '<h1 style="font-family: \'Montserrat\', sans-serif; font-size: 2em;">AI Tutor: Personalized Learning Experience</h1>', 
    unsafe_allow_html=True
)

# All inputs in one line
col1, col2, col3, col4,col5 = st.columns([2,3,3,4,1])


with col1: 
    difficulty_level = st.selectbox("**Depth**", ["Basic", "Intermediate", "Advanced"], key="depth")

with col4:
    concept = st.text_input("**Enter the Concept Name to learn:**", key="concept")

with col2:
    level = st.selectbox("**Learning level:**", ["College graduate", "10 years old", "PhD level"], key="level")

with col3:
    persona_style = st.selectbox(
        "**Learning Style:**", 
        ["None", "Gamer", "Comic Fan", "Sci-Fi Enthusiast", "Sports Fan", "Music Lover", "Movie Buff"], 
        key="persona_style"
    )
with col5:
    st.button('Reset', on_click = reset_conversation)


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
    


    llm = HuggingFaceEndpoint(
        repo_id="google/gemma-1.1-7b-it", 
        temperature = 0.1,
        max_new_tokens = 1024,
        top_k = 50,
        model_kwargs = {'add_to_git_credential': True}
    )
    
    st.session_state.response = llm.invoke(st.session_state.system_prompt)
    # Display assistant response in chat message container
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
            if st.button("YES 😃"):
                st.session_state.quiz_started = True
                st.session_state.quiz_rejection = False
        with col3:
            if st.button("NO 😴"):
                st.session_state.quiz_rejection = True
                

if st.session_state.quiz_rejection:
    st.title('OK, Now quiz for now!')
    
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
    You are an AI-powered quiz generator. Your task is to create a multiple-choice quiz based on the concept previously explained. Follow these instructions carefully:
    1. Generate only one question at a time.
    2. Wait for the user's answer before generating the next question.
    3. Do not provide any commentary or explanations between questions.
    4. Do not generate the report card until explicitly instructed to do so.
    5. Maintain a count of the questions generated and answered.
    6. Format each question as follows:

    Question [number]: [Question text]
    A) [Option A]
    B) [Option B]
    C) [Option C]
    D) [Option D]

    7. After receiving the user's answer, immediately proceed to generate the next question without any additional response.
    8. If you receive the instruction "GENERATE_REPORT_CARD", provide a summary of the user's performance.

    Remember: Generate only one question at a time, and do not proceed to the next question or the report card without explicit instruction.
        """

    # st.session_state.system_prompt2 = 'QUIZ PROMPT'
    st.session_state.full_prompt = st.session_state.system_prompt + " " + \
     '<start_of_turn> model' + st.session_state.response +  '<end_of_turn>'  + \
    " " +  st.session_state.system_prompt2 
    
else:
    if st.session_state.current_question < 5:
        
        # Generate the next question and append it to the full_prompt
        # st.session_state.question = f" Generate the next question. <end_of_turn> <start_of_turn>model "
        st.session_state.question = f"   <end_of_turn> <start_of_turn>model "
        st.session_state.full_prompt += st.session_state.question
        question = llm.invoke(st.session_state.full_prompt)
        print('QUESITON NO ', st.session_state.current_question, '  ', question)
        
        # Display the question
        with st.chat_message("assistant"):
            st.markdown(question)

        
        # Add ONLY the current question to conversation history
        conversation_history.append(f"<start_of_turn>model {question}  ")
    
        # React to user input
        user_answer = st.text_input(
        f"Enter your answer for question {st.session_state.current_question + 1}", key=f"user_answer_{st.session_state.current_question}", max_chars = 5,
        on_change=handle_input_change)   
        
    if st.session_state.current_question == 5:
        st.title('REPORT GENERATED')
        st.session_state.full_prompt  += "<start_of_turn>user GENERATE REPORT CARD <end_of_turn><start_of_turn> model"
        with st.chat_message("assistant"):
            report = llm.invoke(st.session_state.full_prompt)
            st.session_state.full_prompt += report
            print('LLM REPORT ', len(report) , report)
            st.markdown(report)




