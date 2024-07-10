import os
import io
from datetime import datetime
from PIL import Image
from PyPDF2 import PdfReader
from pdf2image import convert_from_bytes
from docxtpl import DocxTemplate
from dotenv import load_dotenv
import streamlit as st
from streamlit_option_menu import option_menu
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Initialize Gemini AI
def get_gemini_pro():
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    return genai.GenerativeModel('gemini-pro')

# Function to extract text from PDF
def pdf_to_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = ''
    for page in reader.pages:
        text += str(page.extract_text())
    return text

# Construct prompt for skills comparison
def construct_skills_prompt(resume, job_description):
    skill_prompt = f'''Act as a HR Manager with 20 years of experience.
    Compare the resume provided below with the job description given below.
    Check for key skills in the resume that are related to the job description.
    List the missing key skillset from the resume.
    Here is the Resume text: {resume}
    Here is the Job Description: {job_description}
    I want the response as a list of missing skill words.'''
    return skill_prompt

# Construct prompt for resume score calculation
def construct_resume_score_prompt(resume, job_description):
    resume_score_prompt = f'''Act as a HR Manager with 20 years of experience.
    Compare the resume provided below with the job description given below.
    Check for key skills in the resume that are related to the job description.
    Rate the resume out of 100 based on the matching skill set.
    Assess the score with high accuracy.
    Here is the Resume text: {resume}
    Here is the Job Description: {job_description}
    I want the response as a single string in the following structure score:%'''
    return resume_score_prompt

# Function to build the resume
def build_resume(first_name, last_name, aspiring_role, email, mob_prefix, mobile,
                 city, country, linkedin, about_me, skill_1, skill_2, skill_3, skill_4, skill_5,
                 company_name, job_role, job_details, lang_1, lang_2, lang_3,
                 ed_12_perc, ed_12_school, pre_degree, pre_degree_cpi, pre_degree_uni,
                 post_degree, post_degree_cpi, post_degree_uni, temp_option):

    # Load the template
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

# Function to read PDF page and extract text
def read_pdf_page(file, page_number):
    pdfReader = PdfReader(file)
    page = pdfReader.pages[page_number]
    return page.extract_text()

# Event handler for text area change
def on_text_area_change():
    st.session_state.page_text = st.session_state.my_text_area

# Main function for Streamlit application
def main():
    st.set_page_config(page_title="Resume Screening System",
                       layout="wide",
                       page_icon="🧑‍⚕️")

    # Sidebar for navigation
    with st.sidebar:
        selected = option_menu('Resume Screening System',
                               ['Build Resume',
                                'Resume Highlights',
                                'Score Checker',
                                'Skill Checker'],
                               menu_icon='hospital-fill',
                               icons=['activity', 'heart', 'person', 'gender-female'],
                               default_index=0)

    # Page selection based on sidebar
    if selected == 'Build Resume':
        st.title('Resume Builder')

        # UI elements for resume building
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

        st.header('Select Template')

        col1, col2 = st.columns(2)
        with col1:
            image = Image.open('images/blue_d1.png')
            st.image(image, caption='Template blue_d1', width=200)
        with col2:
            image = Image.open('images/orange_d1.png')
            st.image(image, caption='Template orange_d1', width=200)

        col3, col4 = st.columns(2)
        with col3:
            image = Image.open('images/green_d3.png')
            st.image(image, caption='Template green_d3', width=200)
        with col4:
            image = Image.open('images/blue_d2.png')
            st.image(image, caption='Template blue_d2', width=200)

        temp_option = st.selectbox('Choose Template', ('blue_d1', 'blue_d2', 'orange_d1', 'green_d3'))

        if st.button("Build Resume"):
            build_resume(first_name, last_name, aspiring_role, email, mob_prefix, mobile,
                         city, country, linkedin, about_me, skill_1, skill_2, skill_3, skill_4, skill_5,
                         company_name, job_role, job_details, lang_1, lang_2, lang_3,
                         ed_12_perc, ed_12_school, pre_degree, pre_degree_cpi, pre_degree_uni,
                         post_degree, post_degree_cpi, post_degree_uni, temp_option)

    elif selected == 'Resume Highlights':
        st.title('Resume Highlights')

        # Resume Highlighter functionality
        pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

        if pdf_file:
            # Create a selectbox to choose the page number
            pdfReader = PdfReader(pdf_file)
            page_numbers = list(range(1, len(pdfReader.pages)+1))
            selected_page = st.selectbox("Select a page", page_numbers)
            selected_page -= 1

            # Convert the selected page to an image
            images = convert_from_bytes(pdf_file.getvalue())
            image = images[selected_page]

            # Display the image and extracted text
            col1, col2 = st.columns([1, 1])
            col1.image(image, caption=f"Page {selected_page + 1}")

            col2.text_area("Extracted Text", height=400, value=read_pdf_page(pdf_file, selected_page),
                           key="my_text_area", on_change=on_text_area_change)

    elif selected == 'Score Checker':
        st.title('Score Checker')

        # Score Checker functionality
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
                    final_result = result.split(":")[1].strip()
                    if '%' not in final_result:
                        final_result = final_result + '%'
                    st.markdown(f"Your Resume matches **{final_result}** with the Job Description", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f'Error: {e}')

    elif selected == 'Skill Checker':
        st.title('Skill Checker')

        # Skill Checker functionality
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
                    st.write('Your Resume misses the following keywords:')
                    st.markdown(result, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f'Error: {e}')

if __name__ == '__main__':
    main()
