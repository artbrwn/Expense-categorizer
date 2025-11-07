import os
import re
from datetime import datetime
import json

def get_available_files():
    files = []
    for file in os.listdir('data/auto_processed/'):
        files.append({
            'path': f'auto_processed/{file}',
            'name': file,
            'type': 'auto-classified',
            'date': extract_date(file),
            'editable': True
        })
    
    
    for file in os.listdir('data/committed/'):
        files.append({
            'path': f'committed/{file}',
            'name': file,
            'type': 'already reviewed',
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

def save_transactions(updated, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(updated, f)