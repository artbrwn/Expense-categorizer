import os.path
import json

class CategorizeTransactions:
    def __init__(self):
        self.categories = {}
        self.categorized_transactions = []
    
    def load_config(self):
        path = "config/categories.json"
        example_path = "config/categories_example.json"
        if not os.path.exists(path):
            path = example_path
        
        with open(path, "r") as config_file:
            categories = json.load(config_file)
            self.categories = {cat: set(keywords) for cat, keywords in categories.items()}

    def categorize(self, transactions_list: list):
        for transaction in transactions_list:
            found = False
            for category, keywords in self.categories.items():
                for keyword in keywords:
                    if keyword.lower() in transaction["description"].lower():
                        transaction["category"] = category
                        found = True
                        break  
                if found:
                    break 

            if not found:
                transaction["category"] = "uncategorized"

        self.categorized_transactions = transactions_list



    def manual_correction(self):
        pass

    def export_result(self):
        pass