# TalentIQ Resume Intelligence Engine

An AI-powered backend system capable of parsing bulk resumes, extracting structured candidate information, and using AI-based analysis to determine suitable job roles and compatibility scores.

## Setup Instructions

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure Environment Variables:
   Open the `.env` file and replace `your_gemini_api_key_here` with your actual Google Gemini API Key.

4. Run the Server:
   ```bash
   uvicorn app.main:app --reload
   ```

5. Access the API Documentation:
   Navigate to `http://127.0.0.1:8000/docs` in your browser to test the API endpoints using the Swagger UI.
