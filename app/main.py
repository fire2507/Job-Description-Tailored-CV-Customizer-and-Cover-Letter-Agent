from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from app.tools import parse_uploaded_pdf
from app.agent import run_tailoring_pipeline

app = FastAPI(title="JD-Tailored Resume Agent")

@app.post("/api/customize")
async def customize_resume(
    resume_file: UploadFile = File(...),
    jd_input: str = Form(...)
):
    if not resume_file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF resume files are supported.")

    try:
        resume_text = parse_uploaded_pdf(resume_file.file)
        if not resume_text:
            raise HTTPException(status_code=400, detail="Could not read text from the uploaded PDF.")

        result = run_tailoring_pipeline(
            user_resume_text=resume_text,
            jd_input=jd_input
        )
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/download-pdf")
def download_pdf():
    pdf_path = "./outputs/Tailored_Application.pdf"
    return FileResponse(pdf_path, media_type="application/pdf", filename="Tailored_Resume.pdf")