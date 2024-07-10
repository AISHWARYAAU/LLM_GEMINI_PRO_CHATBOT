[10:06, 10/07/2024] ᴬⁱˢʰʷᵃʳʸᵃ: # Imports
import os
from datetime import datetime
import io
from PyPDF2 import PdfReader
from docxtpl import DocxTemplate
from pdf2image import convert_from_bytes
from PIL import Image
import streamlit as st
import google.generativeai as genai

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Function to convert PDF to text
def pdf_to_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = ''
    for page in reader.pages:
        text += str(page.extract_text())
    return text

# Function to construct skills prompt for Gemini AI
def construct_skills_prompt(resume, job_description):
    skill_prompt = f'''Act as a HR Manager with 20 years of experience.
    Compare the resume provided below with the job description given below…
[10:09, 10/07/2024] ᴬⁱˢʰʷᵃʳʸᵃ: # Imports
import os
from datetime import datetime
import io
from PyPDF2 import PdfReader
from docxtpl import DocxTemplate
import streamlit as st
import google.generativeai as genai

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Function to convert PDF to text
def pdf_to_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = ''
    for page in reader.pages:
        text += str(page.extract_text())
    return text

# Function to construct skills prompt for Gemini AI
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

# Function to construct resume score prompt for Gemini AI
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

# Function to get result from Gemini AI
def get_result(input):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

# Function to build resume using provided details
def build_resume(first_name, last_name, aspiring_role, email, mob_prefix, mobile,
                 city, country, linkedin, about_me, skill_1, skill_2, skill_3, skill_4, skill_5, 
                 company_name, job_role, job_details, lang_1, lang_2, lang_3,
                 ed_12_perc, ed_12_school, pre_degree, pre_degree_cpi, pre_degree_uni,
                 post_degree, post_degree_cpi, post_degree_uni, temp_option):

    # Load the template based on selected option
    doc = DocxTemplate(f'templates/{temp_option}.docx')

    # Define the context with dynamic values
    context = {
        'first_name': first_name,
        'last_name': last_name, 
        'aspiring_role': aspiring_role,
        'email': email,
        'mob_prefix': mob_prefix,
        'mobile': mobile,
        'city': city,
        'country': country,
        'linkedin': linkedin,
        'about_me': about_me,
        'skill_1': skill_1,
        'skill_2': skill_2,
        'skill_3': skill_3,
        'skill_4': skill_4,
        'skill_5': skill_5,
        'company_name': company_name,
        'job_role': job_role,
        'job_details': job_details,
        'lang_1': lang_1,
        'lang_2': lang_2,
        'lang_3': lang_3,
        'ed_12_perc': ed_12_perc,
        'ed_12_school': ed_12_school,
        'pre_degree': pre_degree,
        'pre_degree_cpi': pre_degree_cpi,
        'pre_degree_uni': pre_degree_uni,
        'post_degree': post_degree,
        'post_degree_cpi': post_degree_cpi,
        'post_degree_uni': post_degree_uni
    }

    # Render the document with the dynamic content
    doc.render(context)

    # Save the document to a buffer
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    # Provide download button for the generated resume
    st.download_button(
        label="Download Resume",
        key="download_resume",
        data=buffer.read(),
        file_name=f"generated_doc_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )

# Main function to run the Streamlit app
def main():
    st.set_page_config(page_title="Resume Builder and AI Tools", page_icon="📄", layout="wide")

    st.title("Resume Builder and AI Tools")

    # Sidebar for selecting AI functionalities
    with st.sidebar:
        selected = st.selectbox(
            'Select AI-Powered Tool',
            ['Build Resume', 'Resume Score Checker', 'Skill Checker'],
        )

    if selected == 'Build Resume':
        # Resume Builder Section
        st.title("Build Your Resume")

        first_name = st.text_input('Enter First Name')
        last_name = st.text_input('Enter Last Name')
        aspiring_role = st.text_input('Enter Aspiring Role')
        email = st.text_input('Enter Email')
        mob_prefix = st.selectbox('Select Mobile Prefix', ['+91', '+1', '+44', '+81'])
        mobile = st.text_input('Enter Mobile Number')
        city = st.text_input('Enter City')
        country = st.text_input('Enter Country')
        linkedin = st.text_input('Enter LinkedIn Link')
        about_me = st.text_area('About Me')
        
        st.subheader('Skills (Enter any 5 relevant skills)')
        skill_1 = st.text_input('Skill 1')
        skill_2 = st.text_input('Skill 2')
        skill_3 = st.text_input('Skill 3')
        skill_4 = st.text_input('Skill 4')
        skill_5 = st.text_input('Skill 5')
        
        st.subheader('Work Experience')
        company_name = st.text_input('Company Name')
        job_role = st.text_input('Job Role')
        job_details = st.text_input('Job Details')
        
        st.subheader('Languages')
        lang_1 = st.text_input('Language 1')
        lang_2 = st.text_input('Language 2')
        lang_3 = st.text_input('Language 3')
        
        st.subheader('Education')
        ed_12_perc = st.text_input('12th Percentage')
        ed_12_school = st.text_input('12th School')
        pre_degree = st.text_input('Pre Degree')
        pre_degree_cpi = st.text_input('Pre Degree CPI')
        pre_degree_uni = st.text_input('Pre Degree University')
        post_degree = st.text_input('Post Degree')
        post_degree_cpi = st.text_input('Post Degree CPI')
        post_degree_uni = st.text_input('Post Degree University')
        
        st.subheader('Select Template')
        temp_option = st.selectbox(
            'Choose Template',
            ['blue_d1', 'blue_d2', 'orange_d1', 'green_d3']
        )
        
        if st.button("Build Resume"):
            build_resume(first_name, last_name, aspiring_role, email, mob_prefix, mobile,
                         city, country, linkedin, about_me, skill_1, skill_2, skill_3, skill_4, skill_5,
                         company_name, job_role, job_details, lang_1, lang_2, lang_3,
                         ed_12_perc, ed_12_school, pre_degree, pre_degree_cpi, pre_degree_uni,
                         post_degree, post_degree_cpi, post_degree_uni, temp_option)
    
    elif selected == 'Resume Score Checker':
        # Resume Score Checker Section
        st.title("Resume Score Checker")
        
        job_description = st.text_area('Enter Job Description')
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
                    
                    # Extract the score from the response
                    final_result = result.split(":")[1].strip()

                    # Display the score to the user
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

    elif selected == 'Skill Checker':

    # Skill Checker Section
    st.title("Skill Checker")
    
    job_description = st.text_area('Enter Job Description')
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
                result = get_result(skill_prompt)
                
                # Display the missing skills to the user
                st.write('Your Resume misses the following keywords:')
                st.markdown(result, unsafe_allow_html=True)
            except Exception as e:
                st.error(f'Error: {e}')
