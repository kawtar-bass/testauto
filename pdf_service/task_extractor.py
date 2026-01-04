"""
Spécialiste Cahier des Charges
Transforme un document complexe en liste de tâches structurées
Utilise Google Gemini API
"""

import google.generativeai as genai
import json
from typing import Optional

# ============================================
# 🎯 SYSTEM PROMPT - LE CŒUR DU SYSTÈME
# ============================================
# Ce prompt oblige l'IA à toujours répondre de la même façon

SYSTEM_PROMPT = """Tu es un expert en gestion de projet et en analyse de cahiers des charges.

🎯 TA MISSION :
Analyser le document fourni et extraire TOUTES les tâches, fonctionnalités et exigences sous forme d'une liste structurée.

📋 RÈGLES STRICTES :
1. Tu DOIS répondre UNIQUEMENT en JSON valide
2. Tu DOIS utiliser EXACTEMENT le format ci-dessous
3. Tu DOIS estimer la complexité et la durée de chaque tâche
4. Tu DOIS regrouper les tâches par catégorie
5. Ne JAMAIS ajouter de texte avant ou après le JSON

📊 FORMAT DE RÉPONSE OBLIGATOIRE :
{
    "projet": {
        "nom": "Nom du projet extrait du document",
        "description": "Description courte du projet",
        "date_analyse": "Date d'aujourd'hui"
    },
    "resume": {
        "total_taches": 0,
        "duree_totale_estimee_jours": 0,
        "complexite_moyenne": "Faible/Moyenne/Élevée"
    },
    "categories": [
        {
            "nom": "Nom de la catégorie (ex: Backend, Frontend, Base de données)",
            "taches": [
                {
                    "id": "T001",
                    "nom_tache": "Nom clair et concis de la tâche",
                    "description": "Description détaillée de ce qu'il faut faire",
                    "complexite": "Faible|Moyenne|Élevée",
                    "duree_estimee_heures": 0,
                    "priorite": "Haute|Moyenne|Basse",
                    "dependances": ["T000"],
                    "competences_requises": ["Python", "SQL", "etc."]
                }
            ]
        }
    ],
    "risques": [
        {
            "description": "Description du risque identifié",
            "impact": "Faible|Moyen|Élevé",
            "mitigation": "Comment réduire ce risque"
        }
    ],
    "recommandations": [
        "Recommandation 1 pour le succès du projet",
        "Recommandation 2..."
    ]
}

🔢 RÈGLES D'ESTIMATION :
- Tâche simple (formulaire, CRUD basique) : 2-4 heures, Complexité Faible
- Tâche moyenne (API, intégration) : 4-8 heures, Complexité Moyenne  
- Tâche complexe (algorithme, sécurité) : 8-16 heures, Complexité Élevée
- Tâche très complexe (ML, architecture) : 16-40 heures, Complexité Élevée

🎯 SOIS EXHAUSTIF : Ne manque AUCUNE tâche mentionnée ou implicite dans le document !
"""


class TaskExtractor:
    """Classe pour extraire les tâches d'un cahier des charges"""
    
    def __init__(self, api_key: str):
        """
        Initialise l'extracteur avec la clé API Gemini
        
        Args:
            api_key: Ta clé API Google Gemini
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",  # Rapide et gratuit
            system_instruction=SYSTEM_PROMPT
        )
    
    def extract_tasks(self, document_text: str) -> dict:
        """
        Extrait les tâches d'un texte de document
        
        Args:
            document_text: Le texte du cahier des charges
            
        Returns:
            dict: Les tâches structurées en JSON
        """
        try:
            # Envoyer le document à Gemini
            response = self.model.generate_content(
                f"Analyse ce cahier des charges et extrait toutes les tâches :\n\n{document_text}"
            )
            
            # Nettoyer la réponse (enlever ```json si présent)
            response_text = response.text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            # Parser le JSON
            tasks_data = json.loads(response_text.strip())
            return {
                "success": True,
                "data": tasks_data
            }
            
        except json.JSONDecodeError as e:
            return {
                "success": False,
                "error": f"Erreur de format JSON: {str(e)}",
                "raw_response": response.text if 'response' in locals() else None
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def extract_tasks_from_pdf(self, pdf_text: str) -> dict:
        """
        Wrapper pour extraire depuis du texte PDF
        (Utilise la même méthode, mais nom plus clair)
        """
        return self.extract_tasks(pdf_text)


# ============================================
# 🧪 TEST RAPIDE
# ============================================
if __name__ == "__main__":
    # Exemple de test
    API_KEY = "YOUR_API_KEY_HERE"  # Remplace par ta vraie clé
    
    # Exemple de cahier des charges
    exemple_cahier = """
    Projet : Application de Gestion de Bibliothèque
    
    L'application doit permettre :
    1. Aux utilisateurs de s'inscrire et se connecter
    2. De rechercher des livres par titre, auteur ou ISBN
    3. De réserver un livre disponible
    4. De voir l'historique des emprunts
    5. Aux administrateurs de gérer le catalogue (ajouter, modifier, supprimer des livres)
    6. D'envoyer des notifications par email pour les retours en retard
    7. De générer des statistiques d'utilisation
    
    Contraintes techniques :
    - Backend en Python avec FastAPI
    - Base de données PostgreSQL
    - Interface web responsive
    """
    
    extractor = TaskExtractor(API_KEY)
    result = extractor.extract_tasks(exemple_cahier)
    
    if result["success"]:
        print(json.dumps(result["data"], indent=2, ensure_ascii=False))
    else:
        print(f"Erreur: {result['error']}")
