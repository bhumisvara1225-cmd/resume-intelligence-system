import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not set in .env file. Get a free key at https://console.groq.com")
    return Groq(api_key=api_key)


def extract_resume_info(text: str) -> dict:
    """
    Uses Groq (Llama 3.3 70B) to extract structured info and analyze the candidate.
    """
    client = get_groq_client()

    prompt = f"""You are an expert HR AI Assistant. Given the following resume text, extract and analyze the information.
Return ONLY a valid JSON object matching this schema exactly. Do not add markdown blocks like ```json ... ```. Just the raw JSON object.

{{
  "full_name": "string",
  "email": "string",
  "phone": "string",
  "linkedin": "string",
  "github": "string",
  "portfolio": "string",
  "address": "string",
  "education": [
    {{"degree": "string", "institution": "string", "year": "string", "cgpa": "string"}}
  ],
  "experience": [
    {{"company_name": "string", "role": "string", "duration": "string", "description": "string"}}
  ],
  "skills": [
    {{"skill_name": "string", "skill_type": "Technical|Soft|Language"}}
  ],
  "ai_analysis": {{
    "candidate_summary": "string (A detailed summary of the candidate)",
    "recommended_roles": "string (Comma-separated list of suitable roles e.g. 'Python Developer: 92%, Data Analyst: 76%')",
    "suitability_scores": "string (JSON string of role scores)",
    "strengths": "string (Comma-separated key strengths)"
  }}
}}

Resume Text:
{text}"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert HR AI assistant that extracts resume data and returns only valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1,
            max_tokens=4096,
        )

        result = response.choices[0].message.content.strip()

        # Strip markdown code blocks if present
        if result.startswith("```json"):
            result = result[7:]
        if result.startswith("```"):
            result = result[3:]
        if result.endswith("```"):
            result = result[:-3]

        data = json.loads(result.strip())
        return data

    except json.JSONDecodeError as e:
        print(f"JSON Parse Error: {e}")
        return {}
    except Exception as e:
        print(f"Groq API Error: {e}")
        return {}
