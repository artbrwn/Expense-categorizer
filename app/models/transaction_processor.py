from app.models.normalize_data import NormalizeData
from app.models.load_data import LoadData
from app.models.categorize_transactions import CategorizeTransactions

class TransactionProcessor:
    """
    Recieves a folder path and returns classified transactions.
    """
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.categories = []
    
    def process_transactions(self):
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

    