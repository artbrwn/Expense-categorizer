from app.models.normalize_data import NormalizeData
from app.models.load_data import LoadData
from app.models.categorize_transactions import CategorizeTransactions
from datetime import datetime

class TransactionProcessor:

    def __init__(self, folder_path="statements"):
        self.folder_path = ""
        self.categories = []
        self.folder_path = folder_path
    
    def process_transactions(self) -> list:
        """
        Recieves a folder path and returns classified transactions.
        """
        
        # Create instance of LoadData for statements folder
        load_data = LoadData(self.folder_path)

        # Extract text from all pdf's in folder
        raw_text = load_data.extract_all_texts()

        # Create instance of NormalizeData for the extracted text
        normalize_data = NormalizeData(raw_text)

        # Get only transactions from text
        transactions_list = normalize_data.extract_transactions()

        # Format extracted transactions
        transformed_list = normalize_data.transform_transactions()

        # Apply correct signs to transactions
        normalize_data.apply_signs()

        # Create instance of CategorizeTransactions
        categorize_transactions = CategorizeTransactions()

        # Load config from json file
        categorize_transactions.load_config()

        # First categorization of data
        categorize_transactions.categorize(normalize_data.transactions)

        self.categories = list(categorize_transactions.categories.keys())
        return categorize_transactions.categorized_transactions
    
    def reconstruct_transactions(self, data_form: dict) -> list:
        """
        Recieves data form and returns list of dictionaries for each transaction
        """
        def cast_field(field, value):
            if field == "id":
                return int(value)
            elif field == "amount":
                return float(value)
            elif field == "date":
                return datetime.fromisoformat(value).date().isoformat()
            else:
                return value

        transactions = dict()
        for key, value in data_form.items():
            field, tx_id = key.split("-")
            tx_id = int(tx_id)
            if tx_id not in transactions:
                transactions[tx_id] = {}
            transactions[tx_id][field] = cast_field(field, value)

        return [transactions[i] for i in sorted(transactions.keys())]