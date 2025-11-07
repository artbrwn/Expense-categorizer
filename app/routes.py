from app import app
from flask import render_template, request, redirect, url_for
from app.models.transaction_processor import TransactionProcessor
import json
from app.models.analyze_transactions import AnalyzeTransactions
from datetime import datetime
from pathlib import Path
from app.models.utils import get_available_files, save_transactions
from app.models.categorize_transactions import CategorizeTransactions

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process")
def process():
    message = None
    try:
        processor = TransactionProcessor()
        all_transactions = processor.process_transactions()
        
        timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
        filename = f"transactions_{timestamp}.json"
        save_dir = Path("data/auto_processed")
        save_dir.mkdir(parents=True, exist_ok=True)

        with open("data/auto_processed/" + filename, "w") as file:
            json.dump(all_transactions, file, default=str)
    except Exception as e:
        message = f"An error has occurred: {e}"
    
    return render_template("process.html", message=message)


@app.route("/review/select", methods=["GET"])
def review_select():
    files = get_available_files()
    return render_template("review_select.html", available_files=files)

@app.route("/review", methods=["GET", "POST"])
def review():
    file_path = request.args.get("file")
    
    if not file_path:
        return redirect(url_for('review_select'))
    
    whole_path = f"data/{file_path}"
    
    # POST: Save edited transactions
    if request.method == "POST":
        # Reconstruct transactions
        processor = TransactionProcessor()
        edited_transactions = processor.reconstruct_transactions(request.form)
        
        # Save
        timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
        save_path = f"data/committed/transactions_{timestamp}.json"
        save_transactions(edited_transactions, save_path)
        
        return redirect(url_for('stats_select'))
    
    # GET: Show form with all transactions
    else:
        # Read all transactions
        with open(whole_path, "r") as f:
            all_transactions = json.load(f)
        
        # Get categories
        categorizer = CategorizeTransactions()
        categorizer.load_config()
        categories = list(categorizer.categories.keys())
        
        return render_template('review.html',
                             transactions=all_transactions, 
                             file_path=file_path,
                             categories=categories)

@app.route("/stats/select", methods=["GET"])
def stats_select():
    files = get_available_files()
    return render_template("stats_select.html", available_files=files)

@app.route("/stats")
def stats():
    file = request.args.get("file")
    file_path = "data/" + file
    df = AnalyzeTransactions()
    df.load_data(file_path)
    df.create_month_column()
    charts = df.prepare_for_chart()
    return render_template("stats.html", charts=charts)