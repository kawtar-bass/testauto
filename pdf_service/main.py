from fastapi import FastAPI, UploadFile, File
import pdfplumber

app = FastAPI()

@app.post("/extract-pdf")
async def extract_pdf(file: UploadFile = File(...)):
    text = ""
    with pdfplumber.open(file.file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return {"text": text}
