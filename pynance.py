import pandas as pd
import os
import json
import datetime
import math
import hashlib
#from enum import Enum


class Entry():
    def __init__(self, date, description, debit, credit, bank):
        self.date = date
        self.description = description
        self.debit = debit
        self.credit = credit
        self.bank=bank 

        self.category = None
        self.subcategory = None
        pass
    
    def __repr__(self):
        return """
{bank} - {date}
{desc}
Debit: {db}
Credit: {cr}
""".format(bank = self.bank, date = self.date, desc = self.description, db=self.debit,cr=self.credit)
    
    def save_json(self):
        return {"Date":self.date,
                "Description":self.description,
                "Debit":self.debit,
                "Credit":self.credit,
                "Bank":self.bank,
                "Category":self.category,
                "Subcategory":self.subcategory,}
    
    def load_json(self, data):
        # Initializer has already been ran, just need any additional information that gets added
        self.category = data["Category"]
        self.subcategory = data["Subcategory"]

    def generate_hash(self):
        return abs(hash((str(self.date) + self.description)))

categories = {
    "Income":["Paycheck","Received","Interest","Other"],
    "Home":["Rent","Utilities","Storage Unit","Renters Insurance","Other"],
    "Transportation":["Auto Loan","Parking","Gas","Maintenance","Car Insurance","Registration Fees","Fares","Other"],
    "Shopping":["Grocery","Goods","Health","Trinkets","Furniture",],
    "Entertainment":["Dining Out","Going Out","Fitness","Hobbies","Subscriptions"],
    "Saving":["General","Specific"],
    "Omit":["Work Recompensation","Other"]
}
class Database():
    def __init__(self):
        df_setup = {"Date":[],"Description":[],"Debit":[],"Credit":[],"Bank":[]}
        self.df = pd.DataFrame(df_setup)
        self.entries = []

        self.category_keywords = {}

    def fill_category_keywords(self):
        for key, value in categories.items():
            self.category_keywords[key] = {}
            for item in value:
                self.category_keywords[key][item] = []

    def new_financial_information(self):
        self.load_data()
        self.read_files()
        self.convert_dataframe_to_entries()
        self.clean_entries()
        self.clean_keywords()
        self.remove_duplicate_entries()
        self.remove_old_entries(2022)
        self.sort_entries_by_date()
        self.categorize()
        self.save_data()

    def read_files(self):
        for file in os.listdir(os.getcwd()):
            if ".csv" in file.lower():
                df2 = pd.read_csv(file)
                if "Chase" in file: #chase
                    df3 = pd.DataFrame().assign(Date=df2["Transaction Date"],Description=df2["Description"],Debit=df2["Amount"],Credit=df2["Amount"],Bank="Chase")
                elif "AccountHistory" in file: #advia
                    df3 = pd.DataFrame().assign(Date=df2["Post Date"],Description=df2["Description"],Debit=df2["Debit"],Credit=df2["Credit"],Bank="Advia")
                self.df = pd.concat([self.df, df3], ignore_index=True)

    def convert_dataframe_to_entries(self):
        for _index, row in self.df.iterrows():
            new_entry = Entry(row["Date"],row["Description"],row["Debit"],row["Credit"],row["Bank"])
            self.entries.append(new_entry)

    def clean_entries(self):
        for entry in self.entries:
            if type(entry.date) == str:
                date_obj = datetime.datetime.strptime(entry.date,"%m/%d/%Y").date()
                entry.date = date_obj
            if entry.debit == entry.credit: #implies they dont differentiate, need to do math
                if entry.debit < 0: #ok, it is actually a debit
                    entry.debit = abs(entry.debit)
                    entry.credit = None
            if entry.debit:
                if math.isnan(entry.debit):
                    entry.debit = None
            if entry.credit:
                if math.isnan(entry.credit):
                    entry.credit=None 
            entry.description = entry.description.upper()
    
    def remove_old_entries(self, cutoff=2022):
        to_keep = []
        for entry in self.entries:
            if entry.date.year >= cutoff:
                to_keep.append(entry)
        self.entries = to_keep
            
    def clean_keywords(self):
        # make all keywords uppercase
        for category, subcategory_dict in self.category_keywords.items():
                for subcategory, keyword_list in subcategory_dict.items():
                    for i in range(0, len(keyword_list)):
                        keyword = self.category_keywords[category][subcategory][i]
                        self.category_keywords[category][subcategory][i] = keyword.upper()
                
    def sort_entries_by_date(self):
        self.entries.sort(key=lambda x: x.date,reverse=True)

    def remove_duplicate_entries(self):
        to_keep = []
        hashmap = {}
        for entry in self.entries:
            hashbrown = entry.generate_hash()
            if hashbrown not in hashmap.keys():
                hashmap[hashbrown] = True
                to_keep.append(entry)
            else:
#                print("\n\nDuplicate found:",entry)
                pass
        self.entries = to_keep

    def load_data(self):
        fp = open("savedata.json","r")
        to_load = json.load(fp)
        for entry_id, entry_data in to_load["Entries"].items():
            clean_date = datetime.datetime.strptime(entry_data["Date"],"%Y-%m-%d").date()
            new_entry = Entry(clean_date, entry_data["Description"],entry_data["Debit"],entry_data["Credit"],entry_data["Bank"],)
            new_entry.load_json(entry_data)
            self.entries.append(new_entry)

        fp = open("keywords.json","r")
        to_load = json.load(fp)
        self.category_keywords = to_load

    def save_data(self):
        to_save = {}
        to_save["Entries"] = {}
        entry_id_ctr = 0
        for entry in self.entries:
            to_save["Entries"][entry_id_ctr] = entry.save_json()
            entry_id_ctr += 1
        with open("savedata.json","w") as fp:
            json.dump(to_save, fp, default=str)
        with open("keywords.json","w") as fp:
            json.dump(self.category_keywords, fp, default=str)

    def scan_category_list(self, entry):
        for category, subcategory_dict in self.category_keywords.items():
            for subcategory, keyword_list in subcategory_dict.items():
                for keyword in keyword_list:
                    if keyword.upper() in entry.description:
                        entry.category = category
                        entry.subcategory = subcategory
                        return True
        return False
    def categorize(self):
        for entry in self.entries:
            if entry.category:
                if entry.subcategory:
                    continue
            #Ok, here's where it gets rough. This is going to be slow and
            # brute forced, but this isn't production software
            ## TODO: once large amount of keywords, flip dictionary such that
            ##   any lookup word is the key, and the value is the category
            results = self.scan_category_list(entry)
            if results == True:
                continue 

        
            print("No Association: ", entry)
            keys = list(categories.keys())
            keys.append("SPLIT")
            for key in keys:
                print("| {:^8.8}".format(key), end=" ")
            print("|")
            for i in range(0,len(keys)):
                print("|    {:}    ".format(i), end=" ")
            print("|")
            user_in = input("Category numbers: ")
            


"""
1. Print categories and numbers 1-n
2. user inputs number for category, or "S" if transaction should be split
3. print out subcategories and numbers
4. user inputs number for subcategory
5. Ask if any keywords should be added
6. User inputs keywords

"""







db = Database()
db.new_financial_information()