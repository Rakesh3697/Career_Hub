
# AI-Powered Job Seeker Tools

**Description:**
This Streamlit application provides a suite of AI-powered tools for job seekers. It leverages Google’s **Gemini API** to analyze resumes for ATS compatibility, generate professional cold emails, and track job applications. Users can also manage and store their resumes directly in the app.

The app is designed for candidates looking to improve their chances of landing interviews by providing actionable insights and automating routine job application tasks.

---

## Features

1. **ATS Resume Analyzer**
    - Upload your resume (PDF) and paste a job description.
    - Get an AI-generated evaluation of your resume including:
        - **Match percentage** with the job description
        - **Missing key skills**
        - Strengths and weaknesses
        - Tips for improving your resume for ATS
2. **Cold Email Generator**
    - Upload your resume and provide details about the role and company.
    - Generate a concise, persuasive, and professional cold email tailored to your target role
3. **Job Tracker**
    - Track your job applications in one place
    - Add new applications with status updates (**Applied, Interview, Offer, Rejected**)
    - View all job applications in a table format
4. **Resume Folder Management**
    - Upload and store multiple resume PDFs
    - Download previously stored resumes for easy access

---

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd <repo-folder>
````

2.  Install dependencies:

<!-- end list -->

```bash
pip install -r requirements.txt
```

3.  Create a `.env` file in the root directory and add your Google API key:

<!-- end list -->

```
GOOGLE_API_KEY=your_google_api_key_here
```

4.  Run the app:

<!-- end list -->

```bash
streamlit run app.py
```

### Folder Structure

```
.
├── app.py                  # Main Streamlit app
├── resumes/                # Folder to store uploaded resumes
├── job_tracker.csv         # CSV file to track job applications
├── .env                    # Environment file with API keys
├── requirements.txt        # Python dependencies
└── README.md
```

### Dependencies

  * Python 3.10+
  * Streamlit
  * PyPDF2
  * Pandas
  * python-dotenv
  * Google Generative AI SDK

## How to Use

1.  Launch the app using Streamlit.
2.  Select a tool from the sidebar:
      * **ATS Resume Analyzer**
      * **Cold Email Generator**
      * **Job Tracker**
      * **Resume Folder**
3.  Follow the on-screen instructions for each tool.
4.  For ATS analysis and cold email generation, upload a PDF resume.
5.  Track all your applications in the **Job Tracker** section.

-----

## Future Enhancements

  * Add skill gap visualization for resumes
  * Integrate LinkedIn scraping to automatically fetch job postings
  * Add email sending functionality for generated cold emails
  * Support multiple resume formats (DOCX, TXT)

## Author

**Rakesh T** – Undergraduate in B.Tech (AI & Data Science)

**Email:** rakeshthangaraj89@gmail.com

-----

## Short Project Description (for Portfolio/GitHub)

An AI-powered Streamlit app for job seekers that analyzes resumes for **ATS compatibility**, generates professional cold emails, and tracks job applications. Built using **Python**, **Google Gemini API**, and **Streamlit** for a smooth candidate experience.

-----

## 🔥 Recruiter/LinkedIn Short Sell

**AI Job Seeker Suite (Python/Gemini API/Streamlit):** Developed an end-to-end application that drives interview-rate improvement by offering three key tools: a **Gemini-powered ATS Resume Analyzer**, a professional **Cold Email Generator**, and a centralized **Job Tracker**. Showcases expertise in **LLM integration**, data management (CSV/PDF), and front-end deployment with Streamlit.

```
```
