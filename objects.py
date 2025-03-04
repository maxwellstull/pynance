from typing import List

class CategoryInfo():
    def __init__(self):
        # need/want/savings
        self.supercategory = None
        self.category = None
        self.percentage = None 
        self.total = None        
        
    def save_json(self):
        return {
            "Supercategory":self.supercategory,
            "Category":self.category,
            "Percentage":self.percentage,
            "Amount":self.total
        }
        
    def load_json(self, data):
        self.supercategory = data['Supercategory']
        self.category = data['Category']
        self.percentage = data['Percentage']
        self.total = data['Amount']

        
class Entry():
    def __init__(self, date, description, debit, credit, bank):
        self.date = date
        self.description = description
        if debit:
            self.debit = float(debit)
        else:
            self.debit = 0
        if credit:
            self.credit = float(credit)
        else:
            self.credit = 0
        
        self.bank = bank 
        self.categorized = False
        self.clean = False
    
        self.categories = []
    
    def __repr__(self):
        return """
==========
{bank} - {date}
{desc}
Debit: {db}
Credit: {cr}
==========
""".format(bank = self.bank, date = self.date, desc = self.description, db=self.debit,cr=self.credit)
    
    def save_json(self):
        to_save = {"Date":self.date,
                "Description":self.description,
                "Debit":self.debit,
                "Credit":self.credit,
                "Bank":self.bank,
                "Clean":self.clean,
                "Categorized":self.categorized,
                "Categories":[]}
        for category in self.categories:
            to_save['Categories'].append(category.save_json())
        
        return to_save
    
    def load_json(self, data):
        self.clean = data['Clean']
        self.categorized = data['Categorized']
        for cat in data['Categories']:
            new_cat = CategoryInfo()
            new_cat.load_json(cat)
            self.categories.append(new_cat)

    def generate_hash(self):
        return abs(hash((str(self.date) + self.description)))

    def categorize(self, categories: List[CategoryInfo]):
        self.category.categorize(categories)