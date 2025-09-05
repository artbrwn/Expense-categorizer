import pdfplumber
import os

class LoadData:
    def __init__(self, folder_path):
        if os.path.isdir(folder_path):
            self.folder_path = folder_path
        else: 
            raise FileNotFoundError(f"No folder exists at {folder_path} path")
    
    def list_pdfs(self) -> list:
        all_files = os.listdir(self.folder_path)
        pdf_list = [file for file in all_files if file.endswith(".pdf")]

        return pdf_list

    def extract_text_from_pdf(self, file_path) -> str:
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                pdf_text = page.extract_text()
                if pdf_text:
                    text += pdf_text
        return text
    
    def extract_all_texts(self) -> dict:
        all_texts = {}
        for file in self.list_pdfs():
            file_path = os.path.join(self.folder_path, file)
            all_texts[file] = self.extract_text_from_pdf(file_path)
        
        return all_texts