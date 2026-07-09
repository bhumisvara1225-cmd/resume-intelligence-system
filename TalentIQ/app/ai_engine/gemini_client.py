import os
import json
import google.generativeai as genai

def configure_gemini():
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key and api_key != "your_gemini_api_key_here":
        genai.configure(api_key=api_key)
    else:
        print("Warning: Valid GEMINI_API_KEY is not set.")

def extract_resume_info(text: str) -> dict:
    """
    Uses Gemini to extract structured info and analyze the candidate.
    """
    configure_gemini()
    prompt = f"""
    You are an expert HR AI Assistant. Given the following resume text, extract and analyze the information.
    Return ONLY a valid JSON object matching this schema exactly. Do not add markdown blocks like ```json ... ```. Just the JSON object.

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
        "suitability_scores": "string (JSON string of scores)",
        "strengths": "string (Comma-separated key strengths)"
      }}
    }}

    Resume Text:
    {text}
    """
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        
        result = response.text.strip()
        if result.startswith("```json"):
            result = result[7:]
        if result.startswith("```"):
            result = result[3:]
        if result.endswith("```"):
            result = result[:-3]
            
        data = json.loads(result.strip())
        return data
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return {}
