import os
import re
from datetime import datetime

def get_available_files():
    files = []
    for file in os.listdir('data/processed/'):
        files.append({
            'path': f'processed/{file}',
            'name': file,
            'type': 'auto-clasificado',
            'date': extract_date(file),
            'editable': True
        })
    
    
    for file in os.listdir('data/committed/'):
        files.append({
            'path': f'committed/{file}',
            'name': file,
            'type': 'ya revisado',
            'date': extract_date(file),
            'editable': True
        })
    
    
    files.sort(key=lambda x: x['date'], reverse=True)
    return files

def extract_date(filename):
    if not filename.endswith('.json'):
        return None
    
    match = re.search(r'(\d{4})_(\d{2})_(\d{2})_(\d{2})_(\d{2})', filename)
    
    if match:
        year, month, day, hour, minute = match.groups()
        try:
            return datetime(int(year), int(month), int(day), 
                          int(hour), int(minute))
        except ValueError:
            return None
    
    return None