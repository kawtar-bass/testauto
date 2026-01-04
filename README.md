# 📋 Extracteur de Tâches - Cahier des Charges

Transforme automatiquement un cahier des charges PDF en liste de tâches structurées avec estimation de complexité et durée.

## 🚀 Installation

```bash
pip install fastapi uvicorn pdfplumber google-generativeai
```

## 🔑 Obtenir une Clé API Gemini (GRATUIT)

1. Va sur : https://aistudio.google.com/app/apikey
2. Connecte-toi avec ton compte Google
3. Clique sur **"Create API Key"**
4. Copie la clé générée

## ⚙️ Configuration

### Option 1 : Variable d'environnement (recommandé)
```bash
# Windows PowerShell
$env:GEMINI_API_KEY = "ta-clé-api-ici"

# Linux/Mac
export GEMINI_API_KEY="ta-clé-api-ici"
```

### Option 2 : Directement dans le code
Ouvre `main.py` et remplace :
```python
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_API_KEY_HERE")
```
par :
```python
GEMINI_API_KEY = "ta-clé-api-ici"
```

## ▶️ Lancer le serveur

```bash
cd pdf_service
uvicorn main:app --reload
```

Ouvre http://localhost:8000 dans ton navigateur

## 📡 Endpoints API

| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/` | Page d'accueil avec formulaire |
| POST | `/extract-pdf` | Extrait le texte d'un PDF |
| POST | `/analyze-pdf` | Analyse un PDF et retourne les tâches en JSON |
| POST | `/analyze-text` | Analyse du texte directement |

## 📊 Format de Sortie

L'API retourne un JSON structuré avec :

```json
{
    "projet": {
        "nom": "Nom du projet",
        "description": "Description"
    },
    "resume": {
        "total_taches": 10,
        "duree_totale_estimee_jours": 15
    },
    "categories": [
        {
            "nom": "Backend",
            "taches": [
                {
                    "id": "T001",
                    "nom_tache": "Créer l'API d'authentification",
                    "complexite": "Moyenne",
                    "duree_estimee_heures": 8,
                    "priorite": "Haute"
                }
            ]
        }
    ]
}
```

## 👥 Pour l'équipe

Clonez le repo :
```bash
git clone https://github.com/sarajaouad8/testauto.git
```

## 📝 System Prompt Utilisé

Le prompt système qui force l'IA à répondre de façon structurée se trouve dans :
`pdf_service/task_extractor.py` (variable `SYSTEM_PROMPT`)
