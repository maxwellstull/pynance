import pandas as pd
import os
import json
import datetime
import math
import hashlib
#from enum import Enum

categories = {
    "Income":["Paycheck","Received","Interest","Other"],
    "Home":["Rent","Utilities","Storage Unit","Renters Insurance","Other"],
    "Transportation":["Auto Loan","Parking","Gas","Maintenance","Car Insurance","Registration Fees","Other"],
    "Shopping":["Grocery","Clothing","Health","Trinkets","Furniture",],
    "Entertainment":["Dining Out","Going Out","Fitness","Hobbies"],
    "Saving":["General","Specific"],
}


class Entry():
    def __init__(self, date, description, debit, credit, bank):
        self.date = date
        self.description = description
        self.debit = debit
        self.credit = credit
        self.bank=bank 
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
                "Bank":self.bank}
    def load_json(self, data):
        # Initializer has already been ran, just need any additional information that gets added
        pass

    def generate_hash(self):
        return abs(hash(self.description))

class Database():
    def __init__(self):
        df_setup = {"Date":[],"Description":[],"Debit":[],"Credit":[],"Bank":[]}
        self.df = pd.DataFrame(df_setup)
        self.entries = []

    def new_financial_information(self):
        self.load_data()
        self.read_files()
        self.convert_dataframe_to_entries()
        self.clean_entries()
        self.remove_duplicate_entries()
        self.sort_entries_by_date()
        self.save_data()

    def read_files(self):
        for file in os.listdir(os.getcwd()):
            if ".csv" in file.lower():
                df2 = pd.read_csv(file)
                if "Chase" in file: #chase
                    df3 = pd.DataFrame().assign(Date=df2["Post Date"],Description=df2["Description"],Debit=df2["Amount"],Credit=df2["Amount"],Bank="Chase")
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
            
    def sort_entries_by_date(self):
        self.entries.sort(key= lambda x: x.date)

    def remove_duplicate_entries(self):
        to_keep = []
        hashmap = {}
        for entry in self.entries:
            hashbrown = entry.generate_hash()
            if hashbrown not in hashmap.keys():
                hashmap[hashbrown] = True
                to_keep.append(entry)
            else:
                print("\n\nDuplicate found:",entry)
        self.entries = to_keep

    def load_data(self):
        fp = open("savedata.json","r")
        to_load = json.load(fp)
        for entry_id, entry_data in to_load.items():
            clean_date = datetime.datetime.strptime(entry_data["Date"],"%Y-%m-%d").date()
            new_entry = Entry(clean_date, entry_data["Description"],entry_data["Debit"],entry_data["Credit"],entry_data["Bank"],)
            new_entry.load_json(entry_data)
            self.entries.append(new_entry)
            
    def save_data(self):
        to_save = {}
        entry_id_ctr = 0
        for entry in self.entries:
            to_save[entry_id_ctr] = entry.save_json()
            entry_id_ctr += 1
        with open("savedata.json","w") as fp:
            json.dump(to_save, fp, default=str)


db = Database()
db.new_financial_information()
