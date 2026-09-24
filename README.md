#  JD-Tailored Resume & Cover Letter Customizer Agent

An intelligent, AI-powered career assistant that parses a candidate's master PDF resume and a target Job Description (JD) to generate an ATS-optimized, single-page tailored resume and a custom cover letter.

---

##  Problem Statement
Applying to modern jobs with a generic resume often leads to instant rejections by automated **Applicant Tracking Systems (ATS)**. Job seekers waste hours manually tailoring bullet points, matching skill keywords, and formatting custom cover letters for every role while struggling to maintain strict single-page limits.

##  Solution
This agent automates application tailoring in seconds:
- **ATS Skill & Keyword Extraction**: Analyzes JDs from raw text or job posting URLs.
- **Impact-Driven Bullet Rewriting**: Aligns experience using the **Action Verb + Context + Result** framework.
- **Single-Page ATS PDF Rendering**: Compiles tailored Markdown into a clean, ATS-compliant PDF.
- **Targeted Cover Letter**: Drafts a concise, role-specific 3-paragraph cover letter for hiring teams.

---

##  Tech Stack

| Domain | Technology / Library | Role |
| :--- | :--- | :--- |
| **Frontend UI** | [Streamlit](https://streamlit.io/) | Drag-and-drop web dashboard for PDF uploads and live interaction |
| **LLM Engine** | [Google Gemini API](https://ai.google.dev/) (`google-genai` SDK) | AI reasoning, keyword extraction, and experience alignment |
| **PDF Parser** | [PyPDF](https://pypdf.readthedocs.io/) | In-memory text extraction from uploaded PDF resumes |
| **Web Scraper** | `requests` + `BeautifulSoup4` | Fetches and cleans job descriptions from web links |
| **PDF Renderer** | `xhtml2pdf` + `markdown` | Converts tailored Markdown into downloadable ATS-friendly PDFs |
| **Configuration** | `python-dotenv` | Secure environment variable management |

---

##  Repository Structure

```text
Job-Description-Tailored-CV-Customizer-and-Cover-Letter-Agent/
│
├── .env                          # API keys and secrets (Git ignored)
├── .gitignore                    # Prevents sensitive/temp files from upload
├── requirements.txt              # Project dependencies
├── README.md                     # Project documentation
├── streamlit_app.py              # Main Streamlit web frontend
│
├── app/
│   ├── __init__.py               # Python package identifier
│   ├── agent.py                  # Core Gemini pipeline and prompt logic
│   ├── main.py                   # FastAPI server endpoints
│   └── tools.py                  # PDF parsing, web scraping, and PDF generation
│
└── outputs/                      # Generated tailored PDFs
