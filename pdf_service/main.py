from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse
import pdfplumber
import os
from task_extractor import TaskExtractor

app = FastAPI(title="PDF Task Extractor - Cahier des Charges")

# ============================================
# 🔑 CONFIGURATION API KEY
# ============================================
# Option 1: Variable d'environnement (recommandé)
# Option 2: Mettre ta clé directement ici (pour les tests)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_API_KEY_HERE")


@app.get("/", response_class=HTMLResponse)
async def home():
    """Page d'accueil avec formulaire"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>📋 Extracteur de Tâches - Cahier des Charges</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 900px; margin: 50px auto; padding: 20px; background: #f5f5f5; }
            .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; text-align: center; }
            .upload-form { text-align: center; margin: 30px 0; }
            input[type="file"] { margin: 20px 0; padding: 10px; }
            button { background: #3498db; color: white; padding: 15px 30px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
            button:hover { background: #2980b9; }
            .info { background: #e8f4f8; padding: 15px; border-radius: 5px; margin: 20px 0; }
            .result { background: #f9f9f9; padding: 20px; border-radius: 5px; margin-top: 20px; white-space: pre-wrap; overflow-x: auto; }
            .loading { display: none; text-align: center; margin: 20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📋 Extracteur de Tâches</h1>
            <p style="text-align:center;">Transformez votre cahier des charges en liste de tâches structurées</p>
            
            <div class="info">
                <strong>📌 Comment ça marche :</strong><br>
                1. Uploadez votre cahier des charges (PDF)<br>
                2. L'IA analyse le document<br>
                3. Vous obtenez une liste de tâches avec complexité et durée estimée
            </div>
            
            <form class="upload-form" action="/analyze-pdf" method="post" enctype="multipart/form-data" onsubmit="showLoading()">
                <input type="file" name="file" accept=".pdf" required><br>
                <button type="submit">🚀 Analyser le Cahier des Charges</button>
            </form>
            
            <div class="loading" id="loading">
                <p>⏳ Analyse en cours... Cela peut prendre 30-60 secondes</p>
            </div>
        </div>
        <script>
            function showLoading() {
                document.getElementById('loading').style.display = 'block';
            }
        </script>
    </body>
    </html>
    """


@app.post("/extract-pdf")
async def extract_pdf(file: UploadFile = File(...)):
    """Extrait le texte d'un PDF (endpoint original)"""
    text = ""
    with pdfplumber.open(file.file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return {"text": text}


@app.post("/analyze-pdf")
async def analyze_pdf(file: UploadFile = File(...)):
    """
    🎯 ENDPOINT PRINCIPAL
    Analyse un PDF de cahier des charges et retourne les tâches structurées
    """
    # Vérifier la clé API
    if GEMINI_API_KEY == "YOUR_API_KEY_HERE":
        raise HTTPException(
            status_code=500, 
            detail="❌ Clé API non configurée! Configure GEMINI_API_KEY"
        )
    
    # Extraire le texte du PDF
    text = ""
    try:
        with pdfplumber.open(file.file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lecture PDF: {str(e)}")
    
    if not text.strip():
        raise HTTPException(status_code=400, detail="Le PDF semble vide ou illisible")
    
    # Analyser avec Gemini
    extractor = TaskExtractor(GEMINI_API_KEY)
    result = extractor.extract_tasks(text)
    
    if result["success"]:
        return {
            "status": "success",
            "message": "Analyse terminée avec succès!",
            "tasks": result["data"]
        }
    else:
        return {
            "status": "error",
            "message": result["error"],
            "raw_response": result.get("raw_response")
        }


@app.post("/analyze-text")
async def analyze_text(text: str = Form(...)):
    """
    Analyse du texte directement (sans PDF)
    Utile pour les tests
    """
    if GEMINI_API_KEY == "YOUR_API_KEY_HERE":
        raise HTTPException(
            status_code=500, 
            detail="❌ Clé API non configurée! Configure GEMINI_API_KEY"
        )
    
    extractor = TaskExtractor(GEMINI_API_KEY)
    result = extractor.extract_tasks(text)
    
    return result
