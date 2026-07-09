@echo off
:: ── Gemini API test script ──────────────────────────────────────────────
:: Set your GEMINI_API_KEY in .env before running this script.
:: Usage: set GEMINI_API_KEY=your_key_here && test_curl.bat

if "%GEMINI_API_KEY%"=="" (
    echo ERROR: GEMINI_API_KEY environment variable is not set.
    echo Please set it first: set GEMINI_API_KEY=your_key_here
    exit /b 1
)

curl.exe "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent" ^
  -H "Content-Type: application/json" ^
  -H "X-goog-api-key: %GEMINI_API_KEY%" ^
  -X POST ^
  -d "{\"contents\": [{\"parts\": [{\"text\": \"Explain how AI works in a few words\"}]}]}"
