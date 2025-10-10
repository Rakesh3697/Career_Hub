import os
import streamlit as st
import pandas as pd
import google.generativeai as genai
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from datetime import datetime

# Load API key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Create folders if not exist
RESUME_FOLDER = "resumes"
os.makedirs(RESUME_FOLDER, exist_ok=True)
JOB_TRACKER_FILE = "job_tracker.csv"

# Load Job Tracker CSV
def load_jobs():
    if os.path.exists(JOB_TRACKER_FILE):
        return pd.read_csv(JOB_TRACKER_FILE)
    else:
        return pd.DataFrame(columns=["Company", "Role", "Application Date", "Status"])

# Save Job Tracker CSV
def save_jobs(df):
    df.to_csv(JOB_TRACKER_FILE, index=False)

# Extract text from PDF
def extract_pdf_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Candidate-Facing ATS Analyzer prompt
def construct_candidate_resume_prompt(resume, jd):
    return f"""
    Act as a career coach and ATS assistant. Evaluate the candidate's resume against the job description.
    Provide:
    1. Match percentage (0-100) with the job description.
    2. Key skills that the candidate is missing.
    3. Candidate's strengths and weaknesses based on the resume.
    4. Tips to improve the resume for better ATS compatibility.

    Candidate Resume:
    {resume}

    Job Description:
    {jd}
    """

# Cold Email Generator prompt
def construct_email_prompt(resume_text, role, company=None, purpose=None, jd=None):
    company_text = f"Company: {company}" if company else ""
    purpose_text = f"Purpose: {purpose}" if purpose else ""
    jd_text = f"Job Description: {jd}" if jd else ""
    return f"""
    Act as a professional copywriter. Generate a concise and persuasive cold email applying for a role.
    Use the information from the candidate's resume below to highlight relevant skills, experience, and achievements.
    The email should be polite, professional, and tailored to the {role} role.
    {company_text}
    {purpose_text}
    {jd_text}

    Candidate Resume:
    {resume_text}
    """

# Call Gemini API
def get_gemini_response(prompt):
    model = genai.GenerativeModel("models/gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text

# Streamlit UI
def main():
    st.title("AI-Powered Job Seeker Tools")
    
    # Sidebar menu
    menu = ["ATS Resume Analyzer", "Cold Email Generator", "Job Tracker", "Resume Folder"]
    choice = st.sidebar.selectbox("Choose a tool", menu)
    
    if choice == "ATS Resume Analyzer":
        st.header("ATS Resume Analyzer (Candidate Self-Check)")
        job_desc = st.text_area("Paste Job Description")
        uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type=["pdf"])
        
        if st.button("Check Resume"):
            if not job_desc or not uploaded_file:
                st.error("Please provide both job description and resume.")
                return

            resume_text = extract_pdf_text(uploaded_file)
            prompt = construct_candidate_resume_prompt(resume_text, job_desc)
            response = get_gemini_response(prompt)

            st.subheader("ATS Analysis Results")
            st.write(response)
    
    elif choice == "Cold Email Generator":
        st.header("Cold Email Generator")
        uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
        company = st.text_input("Company Name")
        role = st.text_input("Role / Position")
        purpose = st.text_area("Purpose / Message")
        jd = st.text_area("Paste Job Description (optional)")

        if st.button("Generate Cold Email"):
            if not uploaded_file or not role:
                st.error("Please upload your resume and specify the role.")
                return
            
            resume_text = extract_pdf_text(uploaded_file)
            prompt = construct_email_prompt(resume_text, role, company, purpose, jd)
            response = get_gemini_response(prompt)

            st.subheader("Generated Cold Email")
            st.write(response)
    
    elif choice == "Job Tracker":
        st.header("Job Tracker")
        df = load_jobs()
        
        with st.form("add_job_form"):
            st.subheader("Add New Job Application")
            new_company = st.text_input("Company Name")
            new_role = st.text_input("Role / Position")
            new_status = st.selectbox("Status", ["Applied", "Interview", "Offer", "Rejected"])
            submitted = st.form_submit_button("Add Job")
            
            if submitted:
                new_entry = {
                    "Company": new_company,
                    "Role": new_role,
                    "Application Date": datetime.today().strftime("%Y-%m-%d"),
                    "Status": new_status
                }
                df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
                save_jobs(df)
                st.success("Job added successfully!")

        st.subheader("Your Job Applications")
        st.dataframe(df)
    
    elif choice == "Resume Folder":
        st.header("Resume Folder")
        st.subheader("Upload New Resume")
        uploaded_file = st.file_uploader("Upload Resume PDF", type=["pdf"])
        
        if st.button("Save Resume"):
            if uploaded_file is not None:
                save_path = os.path.join(RESUME_FOLDER, uploaded_file.name)
                with open(save_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.success(f"Resume saved: {uploaded_file.name}")
            else:
                st.error("Please upload a PDF file.")
        
        st.subheader("Stored Resumes")
        resumes = os.listdir(RESUME_FOLDER)
        if resumes:
            for r in resumes:
                st.write(r)
                if st.button(f"Download {r}"):
                    with open(os.path.join(RESUME_FOLDER, r), "rb") as f:
                        st.download_button(label=f"Download {r}", data=f, file_name=r)
        else:
            st.info("No resumes stored yet.")

if __name__ == "__main__":
    main()
