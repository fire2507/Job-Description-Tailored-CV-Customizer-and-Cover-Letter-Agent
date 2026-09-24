import os
import streamlit as st
from app.tools import parse_uploaded_pdf
from app.agent import run_tailoring_pipeline

st.set_page_config(page_title="JD-Tailored Resume Agent", page_icon="📄", layout="centered")

st.title("📄 JD-Tailored Resume & Cover Letter Generator")
st.write("Upload your PDF resume, paste the target Job Description, and download an ATS-tailored resume and cover letter!")

st.markdown("---")

# 1. File Upload Section
uploaded_file = st.file_uploader("1. Upload your Resume (PDF)", type=["pdf"])

# 2. JD Input Section
jd_input = st.text_area("2. Paste Job Description (or Job Link)", height=200, placeholder="Paste job description text or link here...")

# 3. Process Button
if st.button("✨ Customize My Application", type="primary"):
    if not uploaded_file:
        st.error("Please upload a PDF resume first.")
    elif not jd_input.strip():
        st.error("Please paste a Job Description or link.")
    else:
        with st.spinner("Analyzing JD, aligning experience with Gemini, and compiling PDF..."):
            try:
                # Extract text from uploaded PDF
                resume_text = parse_uploaded_pdf(uploaded_file)
                
                # Run tailoring pipeline
                result = run_tailoring_pipeline(
                    user_resume_text=resume_text,
                    jd_input=jd_input
                )
                
                pdf_path = result["pdf_path"]
                
                st.success("🎉 Your tailored application is ready!")
                
                # Download Button
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        label="📥 Download Tailored PDF Resume & Cover Letter",
                        data=pdf_file,
                        file_name="Tailored_Application.pdf",
                        mime="application/pdf"
                    )
                
                # Preview Text
                with st.expander("Preview Tailored Application Content"):
                    st.markdown(result["markdown_content"])

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")