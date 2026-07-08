import google.generativeai as genai
from dotenv import load_dotenv
import os
import json

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

def analyze_resume(resume_text, user_goal):
    prompt = f"""
you are a senior software engineer and hiring manager.

Evaluate the resume based on the user's goal.

User goal: "{user_goal}"

STRICT RULES:
- Extract only relevant skils for this goal
- REMOVE irrelevant tools [excel for backend, etc]
- Identify real gaps
- Generate roadmap only for missing fields
- Make output DIFFERENT based on goal

Return only JSON:
{{
"skills": [],
"missing_skills": [],
"roadmap" : [],
"interview_questions" : []

}}
Resume:
{resume_text}

"""
    try:
        response = model.generate_content(prompt)

        content = response.text.strip()

        start = content.find("{")
        end = content.rfind("}")+1

        return json.loads(content[start:end])
    
    except Exception as e:
        return {
            "skills": [],
            "missing_skills": [],
            "roadmap": [],
            "interview_questions": [],
            "error": str(e)
        }