from dotenv import load_dotenv 
load_dotenv() 

import streamlit as st 
import os 
import io 
import base64
from PIL import Image 
import pdf2image 
import google.generativeai as genai 

genai.configure(api_key= os.getenv("GOOGLE_API_KEY")) 

def get_gemini_response(input , pdf_content , prompt):
    #model = genai.GenerativeModel('gemini-pro-vision')
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input , pdf_content[0] , prompt]) 
    return response.text 

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None : 

           ## convert pdf into image 
           images = pdf2image.convert_from_bytes(uploaded_file.read()) 
           first_page = images[0] 

           ## Convert to bytes 
           img_byte_arr = io.BytesIO() 
           first_page.save(img_byte_arr , format='JPEG')
           img_byte_arr = img_byte_arr.getvalue() 

           pdf_parts = [
                 {
                       "mime_type" : "image/jpeg" , 
                       "data" : base64.b64encode(img_byte_arr).decode()  ## encode to base64 
                 }
           ]

           return pdf_parts 
    else :
          raise FileNotFoundError("No File Uploaded")
    

### Streamlit App 
st.set_page_config(page_title="ATS Resume Expert") 
st.header("MY PERSONAL ATS ") 
input_text = st.text_area("Job Description : " , key = "input") 
uploaded_file = st.file_uploader("Upload your resume(PDF).." , type = ['pdf']) 


if uploaded_file is not None : 
     st.write("PDF Uploaded Successfully....") 

submit1 = st.button("Tell Me  About the Resume") 
submit2 = st.button("How can I improvise my Skills") 
# submit3 = st.button("What are the keywords That are Missing") 
submit3 = st.button("Percentage Match") 
submit4 = st.button("Personalized learning Path")

input_prompt1 = """
You are an experienced HR with Tech Experience in the field of any one job role from Data Science , Full Stack , Web Development , Big Data Engineering , DEVOPS , Data Analyst , Your task is to review the provided resume against the job description for these profiles . 
Please share your professional evaluation on whether the candidate's profile align with Highlight the strengths and weaknesses of the applicant in relation to the specified job role
"""

input_prompt3 = """
You are an skilled ATS(Applicant Tracking System) scanner with a deep understanding of Data Science , Full Stack , Web Development , Big Data Engineering , DEVOPS , Data Analyst and deep ATS functionality . Your task is to evaluate the resume against the provided job description . given me the percentage of match if the resume matches the job description . 
First the output should come as percentage then keywords missing and last final
"""

input_prompt_4 = """
You are an experienced learning coach and technical expert. Your task is to create a 6-month personalized study plan for an individual aiming to excel in [Job Role], focusing on the skills, topics, and tools specified in the provided job description. The plan should cover the fundamentals, intermediate concepts, and advanced applications, along with hands-on practice. Break down the study schedule month-by-month, ensuring that the individual progresses from beginner to advanced in each of the required skills.
Make sure the study plan includes:
A list of topics and tools to cover each month.
Suggested resources (books, online courses, documentation).
Recommended practical exercises or projects for hands-on experience.
Periodic assessments or milestones to track progress.
Tips for integrating these skills into real-world projects.
"""

if submit1 :
     if uploaded_file is not None : 
          pdf_content = input_pdf_setup(uploaded_file) 
          response = get_gemini_response(input_prompt1 , pdf_content , input_text) 
          st.subheader("The Response is ") 
          st.write(response) 
     else : 
          st.write("Please upload the resume")

elif submit3 :
     if uploaded_file is not None :
          pdf_content = input_pdf_setup(uploaded_file)
          response = get_gemini_response(input_prompt3 , pdf_content , input_text)
          st.subheader("The Response is")
          st.write(response) 
     else :
          st.write("Please upload the resume")

elif submit4 :
     if uploaded_file is not None :
          pdf_content = input_pdf_setup(uploaded_file)
          response = get_gemini_response(input_prompt_4 , pdf_content , input_text)
          st.subheader("The Response is")
          st.write(response) 
     else :
          st.write("Please upload the resume")
