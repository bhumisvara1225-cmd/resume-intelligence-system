import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# NOTE: This file was originally gemini_client.py but has been switched to
# use Groq (Llama 3.3 70B) as the AI backend to avoid Gemini's strict daily
# free-tier quota of 20 requests/day.  All public function signatures remain
# identical so the rest of the codebase requires zero changes.
# ---------------------------------------------------------------------------

def get_groq_client() -> Groq:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not set in .env file. "
            "Get a free key at https://console.groq.com"
        )
    return Groq(api_key=api_key)


def extract_resume_info(text: str) -> dict:
    """
    Uses Groq (Llama 3.3 70B) to extract structured info and analyze a candidate.
    Returns a dict that matches the CandidateCreate schema exactly.
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
    "candidate_summary": "string (A detailed 2-3 sentence summary of the candidate)",
    "recommended_roles": "string (Comma-separated list of suitable roles e.g. 'Python Developer: 92%, Data Analyst: 76%')",
    "suitability_scores": "string (JSON string of role scores)",
    "strengths": "string (Comma-separated key strengths)",
    "ats_score": 0
  }}
}}

IMPORTANT: ats_score must be an INTEGER between 0 and 100 representing the overall resume quality, formatting and content density for an ATS system. Higher = better formatted and more complete resume.

Resume Text:
{text}"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert HR AI assistant that extracts resume data "
                        "and returns only valid JSON. Never wrap the JSON in markdown code blocks."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
            max_tokens=4096,
        )

        result = response.choices[0].message.content.strip()

        # Strip markdown code blocks if the model adds them anyway
        if result.startswith("```json"):
            result = result[7:]
        if result.startswith("```"):
            result = result[3:]
        if result.endswith("```"):
            result = result[:-3]

        data = json.loads(result.strip())

        # Ensure ats_score is an int (model sometimes returns a string)
        if "ai_analysis" in data and isinstance(data["ai_analysis"], dict):
            raw = data["ai_analysis"].get("ats_score", 0)
            try:
                data["ai_analysis"]["ats_score"] = int(raw)
            except (ValueError, TypeError):
                data["ai_analysis"]["ats_score"] = 0

        return data

    except json.JSONDecodeError as e:
        print(f"Groq JSON Parse Error: {e}")
        return {}
    except Exception as e:
        print(f"Groq API Error: {e}")
        return {}


def calculate_role_score(resume_text: str, role: str) -> dict:
    """
    Evaluates how well a candidate matches a specific job role.
    Returns {"ats_score": int, "matching_keywords": [str, ...]}.
    """
    client = get_groq_client()

    prompt = f"""You are an expert HR AI Assistant. Evaluate the candidate's suitability for the role of "{role}" based on the resume text below.
Return ONLY a valid JSON object matching this schema exactly. No markdown code blocks.

{{
  "ats_score": 0,
  "matching_keywords": ["string", "string"]
}}

IMPORTANT:
- ats_score must be an INTEGER between 0 and 100 scoring how well the candidate matches the role.
- matching_keywords must be exact words or short phrases from the resume that are highly relevant to the role.

Resume Text:
{resume_text}"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert HR AI assistant. Return only valid JSON. "
                        "Never wrap it in markdown code blocks."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
            max_tokens=1024,
        )

        result = response.choices[0].message.content.strip()

        if result.startswith("```json"):
            result = result[7:]
        if result.startswith("```"):
            result = result[3:]
        if result.endswith("```"):
            result = result[:-3]

        data = json.loads(result.strip())

        # Ensure ats_score is an int
        try:
            data["ats_score"] = int(data.get("ats_score", 0))
        except (ValueError, TypeError):
            data["ats_score"] = 0

        return data

    except json.JSONDecodeError as e:
        print(f"Groq JSON Parse Error: {e}")
        return {"ats_score": 0, "matching_keywords": []}
    except Exception as e:
        print(f"Groq API Error: {e}")
        return {"ats_score": 0, "matching_keywords": []}
