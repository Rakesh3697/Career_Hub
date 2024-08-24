import streamlit as st
import google.generativeai as genai
import os
import docx2txt
import PyPDF2 as pdf
from dotenv import load_dotenv
import spacy

# Load environment variables from a .env file
load_dotenv()

# Configure the generative AI model with the Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set up the model configuration for text generation
generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

# Define safety settings for content generation
safety_settings = [
    {"category": f"HARM_CATEGORY_{category}", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
    for category in ["HARASSMENT", "HATE_SPEECH", "SEXUALLY_EXPLICIT", "DANGEROUS_CONTENT"]
]

# Load NLP model
nlp = spacy.load("en_core_web_sm")

def generate_response_from_gemini(input_text):
    llm = genai.GenerativeModel(
        model_name="gemini-pro",
        generation_config=generation_config,
        safety_settings=safety_settings,
    )
    output = llm.generate_content(input_text)
    return output.text

def extract_text_from_pdf_file(uploaded_file):
    pdf_reader = pdf.PdfReader(uploaded_file)
    text_content = ""
    for page in pdf_reader.pages:
        text_content += str(page.extract_text())
    return text_content

def extract_text_from_docx_file(uploaded_file):
    return docx2txt.process(uploaded_file)

def extract_skills_and_experience(text):
    doc = nlp(text)
    skills = []
    experiences = []

    for ent in doc.ents:
        if ent.label_ in ["SKILL", "EXPERIENCE"]:
            if ent.label_ == "SKILL":
                skills.append(ent.text)
            elif ent.label_ == "EXPERIENCE":
                experiences.append(ent.text)

    return skills, experiences

# Prompt Template
input_prompt_template = """
As an experienced Applicant Tracking System (ATS) analyst,
with profound knowledge in technology, software engineering, data science, 
and big data engineering, your role involves evaluating resumes against job descriptions.
Recognizing the competitive job market, provide top-notch assistance for resume improvement.
Your goal is to analyze the resume against the given job description, 
assign a percentage match based on key criteria, and pinpoint missing keywords accurately.
resume:{text}
description:{job_description}
I want the response in one single string having the structure
{{"Job Description Match":"%","Missing Keywords":"","Candidate Summary":"","Experience":""}}
"""

# Streamlit app
st.title("Intelligent ATS - Enhance Your Resume ATS")
st.markdown('<style>h1{color: orange; text-align: center;}</style>', unsafe_allow_html=True)
job_description = st.text_area("Paste the Job Description", height=300)
uploaded_file = st.file_uploader("Upload Your Resume", type=["pdf", "docx"], help="Please upload a PDF or DOCX file")

submit_button = st.button("Submit")

if submit_button:
    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            resume_text = extract_text_from_pdf_file(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            resume_text = extract_text_from_docx_file(uploaded_file)

        # Extract skills and experience
        skills, experiences = extract_skills_and_experience(resume_text)
        


        # Generate response from the Gemini model
        response_text = generate_response_from_gemini(input_prompt_template.format(text=resume_text, job_description=job_description))

        # Extract Job Description Match percentage from the response
        match_percentage_str = response_text.split('"Job Description Match":"')[1].split('"')[0]

        # Remove percentage symbol and convert to float
        match_percentage = float(match_percentage_str.rstrip('%'))

        st.subheader("ATS Evaluation Result:")
        st.write(response_text)

        # Display message based on Job Description Match percentage
        if match_percentage >= 60:
            st.text("Candidate is a good match for the position.")
            if experiences:
                st.text(f"Highlighted Experience: {experiences_str}")
        else:
            st.text("Candidate is not a match.")

# Footer with your name and email
footer = """
    <div style="
        position: fixed;
        bottom: 0;
        right: 0;
        width: 100%;
        background-color: transparent;
        text-align: right;
        padding: 20px;
        font-size: 14px;
        color: grey;
    ">
        <p>Made by <b style="font-size:24px;">Rakesh T          </b>
        <br>Email: <a href="mailto:rakeshthangaraj89@gmail.com">rakeshthangaraj89@gmail.com</a></p>
    </div>
"""

st.markdown(footer, unsafe_allow_html=True)
