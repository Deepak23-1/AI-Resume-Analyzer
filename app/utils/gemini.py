import google.generativeai as genai
import json
import os
from dotenv import load_dotenv


load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")



def analyze_resume(resume_text: str):
    prompt = f"""
    You are an ATS Resume Analyzer.

    Analyze the following resume.

    Resume: {resume_text}

    Return Oly valid JSON in the following format.


    {{
    "ats_score": 0,
    "technical_skills": [],
    "missing skills": [],
    "strengths": [],
    "weaknesses": [],
    "suggestions": []
    }}

    Do not include markdown.
    Do not use triple backticks.
    Return only JSON.
    """


    response = model.generate_content(prompt)

    result = response.text.strip()

    result = result.replace("```json", "")
    result = result.replace("```", "")

    analysis = json.loads(result)

    return analysis



def compare_resume_job(resume_text: str, job_description: str):

    prompt = f"""
You are an ATS Resume Analyzer.

Compare the following resume with the job description.

Resume:
{resume_text}

Job Description:
{job_description}

Return only valid JSON.

{{
    "match_score": 0,
    "matching_skills": [],
    "missing_skills": [],
    "strengths": [],
    "suggestions": []
}}

Do not use markdown.
Return only JSON.
"""

    response = model.generate_content(prompt)

    result = response.text.strip()

    result = result.replace("```json", "")
    result = result.replace("```", "")

    return json.loads(result)