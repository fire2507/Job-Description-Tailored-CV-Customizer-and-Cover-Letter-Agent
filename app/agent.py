import os
import time
from google import genai
from dotenv import load_dotenv
from app.tools import extract_jd_text, render_markdown_to_pdf

load_dotenv()

def run_tailoring_pipeline(user_resume_text: str, jd_input: str) -> dict:
    """Analyzes candidate resume and target JD using Gemini with automatic model fallback."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing from your .env file.")

    client = genai.Client(api_key=api_key)
    jd_text = extract_jd_text(jd_input)
    
    prompt = f"""
You are an expert ATS Resume Coach and Career Strategist.

TARGET JOB DESCRIPTION:
{jd_text[:3000]}

CANDIDATE MASTER RESUME:
{user_resume_text[:4000]}

TASK:
1. Extract top technical keywords and core responsibilities from the Target Job Description.
2. Align the Candidate's Master Resume with these requirements.
3. Rewrite bullet points using the structure: [Action Verb] + [Context/Technologies Used] + [Quantifiable Impact or Outcome].
4. Maintain strict factual accuracy based on the candidate's actual background—do NOT invent non-existent job titles or metrics.
5. Generate a professional 3-paragraph Cover Letter addressed to the hiring team.

FORMAT OUTPUT IN CLEAN MARKDOWN:
# CANDIDATE RESUME
## Professional Summary
[2-3 sentence overview aligned with the target role]

## Technical & Core Competencies
- **Skills**: [Extracted skills matching JD]

## Professional & Project Experience
### [Job Title / Project Name]
- [Action Verb + Context + Result bullet point 1]
- [Action Verb + Context + Result bullet point 2]
- [Action Verb + Context + Result bullet point 3]

---

# COVER LETTER

Dear Hiring Manager,

[Paragraph 1: Passion for the role and high-level fit]

[Paragraph 2: Specific evidence from candidate experience solving key JD challenges]

[Paragraph 3: Confident call to action and closing]

Sincerely,
Candidate
"""

    # List of candidate models to route through if 503 high demand hits
    candidate_models = ["gemini-3.6-flash", "gemini-2.5-pro", "gemini-1.5-flash"]
    response = None
    last_exception = None

    for model_name in candidate_models:
        # Try each model up to 2 times before falling back to the next
        for attempt in range(2):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                )
                if response and response.text:
                    break
            except Exception as e:
                last_exception = e
                time.sleep(1.5)
        
        if response and response.text:
            break  # Successfully generated content, exit loop

    if not response or not response.text:
        raise RuntimeError(f"All model endpoints busy or unavailable. Last error: {str(last_exception)}")

    final_md = response.text
    pdf_filename = "./outputs/Tailored_Application.pdf"
    render_markdown_to_pdf(final_md, pdf_filename)
    
    return {
        "status": "success",
        "pdf_path": pdf_filename,
        "markdown_content": final_md
    }