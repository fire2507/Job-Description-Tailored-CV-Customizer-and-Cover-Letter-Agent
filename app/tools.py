import os
import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader
import markdown
from xhtml2pdf import pisa

def parse_uploaded_pdf(file_bytes) -> str:
    """Extracts raw text content from an uploaded PDF resume file."""
    reader = PdfReader(file_bytes)
    extracted_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            extracted_text += text + "\n"
    return extracted_text.strip()

def extract_jd_text(jd_input: str) -> str:
    """Scrapes URL if input is a web link; otherwise returns plain text as-is."""
    if jd_input.startswith("http://") or jd_input.startswith("https://"):
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        res = requests.get(jd_input, headers=headers)
        soup = BeautifulSoup(res.content, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:4000]
    return jd_input

def render_markdown_to_pdf(md_content: str, output_path: str = "./outputs/Tailored_Resume.pdf") -> str:
    """Converts tailored Markdown text into a clean ATS-formatted PDF using xhtml2pdf."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    html_content = markdown.markdown(md_content, extensions=['tables'])
    
    css = """
    <style>
        @page { size: letter; margin: 0.6in; }
        body { font-family: Helvetica, Arial, sans-serif; font-size: 10pt; line-height: 1.4; color: #111; }
        h1 { font-size: 16pt; margin-bottom: 2px; text-transform: uppercase; color: #000; }
        h2 { font-size: 11pt; border-bottom: 1px solid #222; padding-bottom: 2px; margin-top: 10px; margin-bottom: 4px; text-transform: uppercase; }
        p { margin: 2px 0; }
        ul { margin-top: 2px; margin-bottom: 6px; padding-left: 16px; }
        li { margin-bottom: 3px; }
        strong { color: #000; }
    </style>
    """
    full_html = f"<html><head>{css}</head><body>{html_content}</body></html>"
    
    with open(output_path, "wb") as pdf_file:
        pisa.CreatePDF(full_html, dest=pdf_file)
        
    return output_path