from docxtpl import DocxTemplate
import streamlit as st
from datetime import datetime
from PIL import Image, ImageDraw
import io
import pyrebase
import os
from pathlib import Path


current_datetime = datetime.now()


filename = f"generated_doc_{current_datetime.strftime('%Y%m%d_%H%M%S')}.docx"


def build_resume(first_name, last_name, aspiring_role, email, mob_prefix, mobile,
                 city, country, linkedin, about_me, skill_1, skill_2, skill_3, skill_4, skill_5, company_name, job_role, job_details, lang_1, lang_2, lang_3,
                 ed_12_perc, ed_12_school, pre_degree, pre_degree_cpi, pre_degree_uni, post_degree, post_degree_cpi, post_degree_uni, temp_option):


    # Load the template
    doc = DocxTemplate(f'{temp_option}.docx')
 
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
        'skill_1' : skill_1,
        'skill_2' : skill_2,
        'skill_3' : skill_3,
        'skill_4' : skill_4,
        'skill_5' : skill_5,
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



    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    st.download_button(
            label="Download Resume",
            key="download_resume",
            data=buffer.read(),  # Read the content of the buffer
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )



if __name__=="__main__":


    st.title("Resume Builder")


    first_name = st.text_input('Enter first name')

    last_name = st.text_input('Enter last name')

    aspiring_role = st.text_input('Enter the job you want to do')

    email = st.text_input('Enter your email')

    mobile_prefix_options = ['+91', '+1', '+44', '+81']  # Add your desired prefixes

    col1, col2 = st.columns(2)

    with col1:
        mob_prefix = st.selectbox('Select Mobile Prefix', mobile_prefix_options)
    with col2:
        mobile = st.text_input('Enter your mobile number')

    col3, col4 = st.columns(2)

    with col3:
        city = st.text_input('Enter your city')
    with col4:
        country = st.text_input('Enter your country')

    linkedin = st.text_input('Enter your linkedin link')

    about_me = st.text_area('Enter something about you')

    with st.container():
        st.subheader('Enter any 5 relevant skills')
        skill_1 = st.text_input('Skill1')
        skill_2 = st.text_input('Skill2')
        skill_3 = st.text_input('Skill3')
        skill_4 = st.text_input('Skill4')
        skill_5 = st.text_input('Skill5')

    with st.container():
        st.subheader('Enter your most recent work experience or any other relevant experience')
        company_name = st.text_input('Company name')
        job_role = st.text_input('Job Role')
        job_details = st.text_input('Job Details')


    with st.container():
        st.subheader('Enter any 3 languages you have fluency on (Leave blank if less languages known)')
        lang_1 = st.text_input('Language 1')
        lang_2 = st.text_input('Laguage 2')
        lang_3 = st.text_input('Language 3')

    with st.container():
        st.subheader('Enter your education degrees')
        
        col5, col6 = st.columns(2)
        with col5:
            ed_12_perc = st.text_input('Enter your 12th percentage')
        with col6:
            ed_12_school = st.text_input('Enter the school of 12th education')



        col7, col8, col9 = st.columns(3)
        with col7:
            pre_degree = st.text_input('Enter your pre degree')
        with col8:
            pre_degree_cpi = st.text_input('Enter your university cpi')
        with col9:
            pre_degree_uni = st.text_input('Enter your university')

        col10, col11, col12 = st.columns(3)
        with col10:
            post_degree = st.text_input('Enter your post degree')
        with col11:
            post_degree_cpi = st.text_input('Enter your post degree university cpi')
        with col12:
            post_degree_uni = st.text_input('Enter your post degree university')

        st.header('View the template to have your resume in')

        col13, col14 = st.columns(2)

        with col13:
            image = Image.open('images/blue_d1.png')
 
            st.image(image, caption='Template blue_d1', width=200)
        with col14:
            image = Image.open('images/orange_d1.png')

            st.image(image, caption='Template orange_d1', width=200)

        col15, col16 = st.columns(2)

        with col15:
            image = Image.open('images/green_d3.png')

            st.image(image, caption='Template green_d3', width=200)
        with col16:
            image = Image.open('images/blue_d2.png')

            st.image(image, caption='Template blue_d2', width=200)


        temp_option = st.selectbox(
        'How would you like your resume to be?',
        ('blue_d1', 'blue_d2', 'orange_d1', 'green_d3'))







    



    if st.button("Build Resume"):

        build_resume(first_name, last_name, aspiring_role, email, mob_prefix, mobile,
                 city, country, linkedin, about_me, skill_1, skill_2, skill_3, skill_4, skill_5, company_name, job_role, job_details, lang_1, lang_2, lang_3,
                 ed_12_perc, ed_12_school, pre_degree, pre_degree_cpi, pre_degree_uni, post_degree, post_degree_cpi, post_degree_uni, temp_option)

