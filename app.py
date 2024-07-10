import io
from datetime import datetime
from docxtpl import DocxTemplate
import streamlit as st
from PIL import Image

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

def main():
    st.set_page_config(page_title="Resume Builder", page_icon="📄", layout="wide")
    st.title("Resume Builder")

    # UI elements to collect user inputs
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

if __name__ == '__main__':
    main()
