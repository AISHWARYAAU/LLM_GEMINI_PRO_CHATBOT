import os
from dotenv import load_dotenv

from PIL import Image
import streamlit as st
from streamlit_option_menu import option_menu

from PyPDF2 import PdfReader
import google.generativeai as genai
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

from gemini_utility import (
    load_gemini_pro_model,
    gemini_pro_response,
    gemini_pro_vision_response,
    embeddings_model_response
)

load_dotenv()  # load all our environment variables

def get_gemini_pro():
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    return genai.GenerativeModel('gemini-pro')

def pdf_to_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = ''
    for page in reader.pages:
        text += str(page.extract_text())
    return text

def construct_skills_prompt(resume, job_description):
    skill_prompt = f'''Act as a HR Manager with 20 years of experience.
    Compare the resume provided below with the job description given below.
    Check for key skills in the resume that are related to the job description.
    List the missing key skillset from the resume.
    I just need the extracted missing skillset.
    Here is the Resume text: {resume}
    Here is the Job Description: {job_description}
    I want the response as a list of missing skill words.'''
    return skill_prompt

def construct_resume_score_prompt(resume, job_description):
    resume_score_prompt = f'''Act as a HR Manager with 20 years of experience.
    Compare the resume provided below with the job description given below.
    Check for key skills in the resume that are related to the job description.
    Rate the resume out of 100 based on the matching skill set.
    Assess the score with high accuracy.
    Here is the Resume text: {resume}
    Here is the Job Description: {job_description}
    I want the response as a single string in the following structure: score:%'''
    return resume_score_prompt

def construct_resume_improvement_prompt(resume, job_description):
    improvement_prompt = f'''Act as a HR Manager with 20 years of experience.
    Compare the resume provided below with the job description given below.
    Check for key skills in the resume that are related to the job description.
    Provide detailed suggestions to improve the resume based on the job description.
    Here is the Resume text: {resume}
    Here is the Job Description: {job_description}
    I want the response in a structured list of suggestions.'''
    return improvement_prompt

def get_result(input):
    model = get_gemini_pro()
    response = model.generate_content(input)
    return response.text

st.set_page_config(
    page_title="Gemini AI",
    page_icon="🧠",
    layout="centered",
)

# Load authentication configuration
def load_auth_config():
    with open('config.yaml') as file:
        return yaml.load(file, Loader=SafeLoader)

config = load_auth_config()

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('Login', 'main')

# Function to update the config file
def save_auth_config(updated_config):
    with open('config.yaml', 'w') as file:
        yaml.dump(updated_config, file)

# Sign-up page
if st.sidebar.button('Sign Up'):
    st.title("🔑 Sign Up")

    new_username = st.text_input('Username')
    new_name = st.text_input('Name')
    new_email = st.text_input('Email')
    new_password = st.text_input('Password', type='password')

    if st.button('Register'):
        if new_username and new_name and new_email and new_password:
            hashed_password = stauth.Hasher([new_password]).generate()[0]
            if new_username not in config['credentials']['usernames']:
                config['credentials']['usernames'][new_username] = {
                    'name': new_name,
                    'email': new_email,
                    'password': hashed_password
                }
                save_auth_config(config)
                st.success('User registered successfully! You can now log in.')
            else:
                st.error('Username already exists.')
        else:
            st.error('Please fill in all fields.')

if authentication_status:
    with st.sidebar:
        selected = option_menu(
            'AI-Powered Resume Screening and Assistance Tool',
            ['Overview', '🧑‍💻Score Checker', '🕵Skill Checker', 'ChatBot', 'Image Captioning', 'Embed text', 'Ask me anything'],
            menu_icon='robot',
            icons=['info-circle', 'chat-dots-fill', 'image-fill', 'textarea-t', 'patch-question-fill', 'bi-clipboard2-data', 'hash'],
            default_index=0
        )

    # Overview page
    if selected == 'Overview':
        st.title("🔍 Overview")
        st.markdown("""
        ### Welcome to the AI-Powered Resume Screening and Assistance Tool!
        
        Here is a brief explanation of the functionalities offered by this tool:

        - **🧑‍💻 Score Checker**: Upload your resume and provide a job description to get an ATS (Applicant Tracking System) score, which indicates how well your resume matches the job description.
        - **🕵 Skill Checker**: Identify the skills missing from your resume based on the provided job description. This feature helps you understand which key skills you need to add.
        - **ChatBot**: Interact with an AI-powered chatbot that can help you add the missing skills to your resume and provide other assistance.
        - **Image Captioning**: Upload an image (such as an image in your resume) to get a caption. This feature can help you ensure that the images in your resume are appropriately described.
        - **Embed Text**: Enter text to get its embeddings, useful for encryption and other advanced text processing.
        - **Ask me anything**: Ask any type of question and get a response from the AI. This feature is designed to help you with a wide range of queries.

        We hope you find this tool helpful in enhancing your resume and preparing for job applications. 
        """)

    # Function to translate roles between Gemini-Pro and Streamlit terminology
    def translate_role_for_streamlit(user_role):
        if user_role == "model":
            return "assistant"
        else:
            return user_role

    # ChatBot page
    if selected == 'ChatBot':
        model = load_gemini_pro_model()

        # Initialize chat session in Streamlit if not already present
        if "chat_session" not in st.session_state:
            st.session_state.chat_session = model.start_chat(history=[])

        # Display the chatbot's title on the page
        st.title("🤖 ChatBot")

        # Display the chat history
        for message in st.session_state.chat_session.history:
            with st.chat_message(translate_role_for_streamlit(message.role)):
                st.markdown(message.parts[0].text)

        # Input field for user's message
        user_prompt = st.chat_input("Ask Gemini-Pro...")
        if user_prompt:
            # Add user's message to chat and display it
            st.chat_message("user").markdown(user_prompt)

            # Send user's message to Gemini-Pro and get the response
            gemini_response = st.session_state.chat_session.send_message(user_prompt)

            # Display Gemini-Pro's response
            with st.chat_message("assistant"):
                st.markdown(gemini_response.text)

    # Image captioning page
    if selected == "Image Captioning":
        st.title("📷 Snap Narrate")

        uploaded_image = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

        if st.button("Generate Caption"):
            image = Image.open(uploaded_image)

            col1, col2 = st.columns(2)

            with col1:
                resized_img = image.resize((800, 500))
                st.image(resized_img)

            default_prompt = "write a short caption for this image"  # change this prompt as per your requirement

            # get the caption of the image from the gemini-pro-vision LLM
            caption = gemini_pro_vision_response(default_prompt, image)

            with col2:
                st.info(caption)

    # Embed text page
    if selected == "Embed text":
        st.title("🔡 Embed Text")

        # text box to enter prompt
        user_prompt = st.text_area(label='', placeholder="Enter the text to get embeddings")

        if st.button("Get Response"):
            response = embeddings_model_response(user_prompt)
            st.markdown(response)

    # Ask me anything page
    if selected == "Ask me anything":
        st.title("❓ Ask me a question")

        # text box to enter prompt
        user_prompt = st.text_area(label='', placeholder="Ask me anything...")

        if st.button("Get Response"):
            response = gemini_pro_response(user_prompt)
            st.markdown(response)

    # Resume Score Checker page
    if selected == '🧑‍💻Score Checker':
        st.title("🧑‍💻 Resume Score Checker")

        job_description = st.text_area('Enter the Job Description')
        uploaded_file = st.file_uploader('Upload Your Resume', type=['pdf'])

        if st.button('Get Score'):
            if job_description == '':
                st.error('Enter Job Description')
            elif uploaded_file is None:
                st.error('Upload your Resume')
            else:
                try:
                    resume = pdf_to_text(uploaded_file)
                    score_prompt = construct_resume_score_prompt(resume, job_description)
                    result = get_result(score_prompt)
                    final_result = result.split(":")[1]
                    if '%' not in final_result:
                        final_result = final_result + '%'
                    result_str = f"""
                    <style>
                    p.a {{
                      font: bold 25px Arial;
                    }}
                    </style>
                    <p class="a">Your Resume matches {final_result} with the Job Description</p>
                    """
                    st.markdown(result_str, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f'Error: {e}')

    # Skill Checker page
    if selected == '🕵Skill Checker':
        st.title("🕵 Skill Checker")

        job_description = st.text_area('Enter the Job Description')
        uploaded_file = st.file_uploader('Upload Your Resume', type=['pdf'])

        if st.button('Get Missing Skills'):
            if job_description == '':
                st.error('Enter Job Description')
            elif uploaded_file is None:
                st.error('Upload your Resume')
            else:
                try:
                    resume = pdf_to_text(uploaded_file)
                    skill_prompt = construct_skills_prompt(resume, job_description)
                    improvement_prompt = construct_resume_improvement_prompt(resume, job_description)
                    result = get_result(skill_prompt)
                    improvement_suggestions = get_result(improvement_prompt)

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.write('Your Resume misses the following keywords:')
                        st.markdown(result, unsafe_allow_html=True)

                    with col2:
                        st.write('Here are some suggestions to improve your resume:')
                        st.markdown(improvement_suggestions, unsafe_allow_html=True)

                    with col3:
                        st.write('Summary:')
                        st.markdown("""
                        - **ATS Score Checker**: Check how well your resume matches the job description.
                        - **Skill Checker**: Find out which skills are missing in your resume.
                        - **Improvement Suggestions**: Get suggestions to improve your resume.
                        """, unsafe_allow_html=True)

                except Exception as e:
                    st.error(f'Error: {e}')

elif authentication_status == False:
    st.error('Username/password is incorrect')

elif authentication_status == None:
    st.warning('Please enter your username and password')
