import os
from pathlib import Path
from typing import Optional, Union, Dict

def extract_text_from_any_file(file_path: Union[str, Path]) -> Optional[str]:
    """
    Extrait le texte de différents types de fichiers.
    
    Args:
        file_path: Chemin vers le fichier
        
    Returns:
        Texte extrait ou None si échec
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        print(f"Erreur: Le fichier {file_path} n'existe pas")
        return None
    
    extension = file_path.suffix.lower()
    
    try:
        # Fichiers texte simples
        if extension in ['.txt', '.md', '.log', '.csv', '.json', '.xml', '.html', '.py', '.js', '.java', '.cpp']:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        
        # PDF
        elif extension == '.pdf':
            import PyPDF2
            text = []
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text.append(page.extract_text())
            return '\n'.join(text)
        
        # Word (.docx)
        elif extension == '.docx':
            from docx import Document
            doc = Document(str(file_path))
            return '\n'.join([para.text for para in doc.paragraphs])
        
        # Excel
        elif extension in ['.xlsx', '.xls']:
            import pandas as pd
            df = pd.read_excel(file_path, sheet_name=None)
            text = []
            for sheet_name, sheet_df in df.items():
                text.append(f"=== Sheet: {sheet_name} ===")
                text.append(sheet_df.to_string())
            return '\n\n'.join(text)
        
        # HTML
        elif extension in ['.html', '.htm']:
            from bs4 import BeautifulSoup
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
                return soup.get_text(separator='\n', strip=True)
        
        # Image (OCR avec pytesseract)
        elif extension in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']:
            from PIL import Image
            import pytesseract
            image = Image.open(file_path)
            return pytesseract.image_to_string(image)
        
        # Autres formats texte
        else:
            print(f"Avertissement: Type de fichier {extension} non spécifiquement supporté, tentative de lecture en texte brut")
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
                
    except Exception as e:
        print(f"Erreur lors de l'extraction du texte de {file_path}: {str(e)}")
        return None
    

def detect_language(text: str) -> str:
    """
    Détecte la langue d'un texte.
    
    Args:
        text: Texte à analyser
        
    Returns:
        Code de langue (ex: 'en', 'fr', 'es') ou message d'erreur
    """
    if not text or len(text.strip()) < 10:
        return "Erreur: Texte trop court ou vide"
    
    try:
        from langdetect import detect
        return detect(text)
    except ImportError:
        return "Erreur: La bibliothèque langdetect n'est pas installée"
    except Exception as e:
        return f"Erreur detection de langue : {str(e)}"



# Exemple d'utilisation
if __name__ == "__main__":
    # Test avec un fichier
    file_path = r"Data Justin\directives\1.DIRECTIVE (UE) 20192161 DU PARLEMENT EUROPÉEN ET DU CONSEIL.html"
    text = extract_text_from_any_file(file_path)
    
    if text:
        print(f"\n\nTexte extrait ({len(text)} caractères):\n")
        # print(text[:1000])  # Afficher les 1000 premiers caractères
        print(detect_language(text))