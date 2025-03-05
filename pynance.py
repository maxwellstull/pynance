import sys
sys.path.append('resources')
from customSlider import MultiSlideBar

import json
import csv
import os 
import math
from objects import Entry, CategoryInfo
import tkinter as tk
from tkinter import filedialog
import datetime
class Pynance():
    def __init__(self):
        self.entries = []
        
        with open('settings.json','r') as fp:
            settings = json.load(fp)
        self.settings = settings
        self.categories = settings['Categories']
        self.ingest = settings['Ingest']
        self.load_save_data('savedata.json')        
        
        
    def load_save_data(self, path):
        if not os.path.isfile(path):
            print("Skipping loading save data. This is not a problem if there isn't any.")
        else: #savedata.json exists
            print("savedata exists")
        
        self.process_entry_updates()
        
    def import_account_history(self, filename):
        if not os.path.isfile(filename):
            print("Skipping reading file:" + filename + ". It doesn't exist?")
        else:
            # Figure out what ingest scheme to use
            scheme = self.ingest[filename]
                
            with open(filename,'r') as fp:
                reader = csv.reader(fp)
                headers = next(reader)
                # Figure out reading index from ingest config
                date_idx = headers.index(scheme['date'])
                description_idx = headers.index(scheme['description'])
                debit_idx = headers.index(scheme['debit'])
                credit_idx = headers.index(scheme['credit'])
                
                for row in reader:
                    date = datetime.datetime.strptime(row[date_idx],scheme['date_fmt']).date()
                    description = row[description_idx]
                    debit = row[debit_idx]
                    credit = row[credit_idx]
                    bank = scheme['institution']
                    
                    entry = Entry(date, description, debit, credit, bank)
                    self.entries.append(entry)
        self.process_entry_updates()
    def process_entry_updates(self):
        # Clean entries
        for entry in self.entries:
            if entry.clean == True:
                continue
            if type(entry.date) == str:
                date_obj = datetime.datetime.strptime(entry.date,"%m/%d/%Y").date()
                entry.date = date_obj
            if (entry.debit - entry.credit) < 0.001 and entry.debit != 0:
                if entry.debit < 0: #is actual debit
                    entry.debit = abs(entry.debit)
                    entry.credit = None
                else: #entry.debit > 0
                    entry.debit = None

#            if entry.debit:
#                if math.isnan(entry.debit):
#                    entry.debit = None
#            if entry.credit:
#                if math.isnan(entry.credit):
#                    entry.credit = None
            entry.description = entry.description.upper()
            
        # Remove old entries
        to_keep = []
        for entry in self.entries:
            if entry.date.year >= datetime.datetime.strptime(self.settings["Cutoff Date"],"%m/%d/%Y").year:
                to_keep.append(entry)
        self.entries = to_keep
    
        # Remove duplicates
        to_keep = []
        hashmap = {}
        for entry in self.entries:
            hashbrown = entry.generate_hash()
            if hashbrown not in hashmap.keys():
                hashmap[hashbrown] = True
                to_keep.append(entry)
        self.entries = to_keep
        
    def save_data(self):
        to_save = {"Entries":[]}
        for entry in self.entries:
            to_save['Entries'].append(entry.save_json())
        with open('savedata.json','w') as fp:
            json.dump(to_save, fp, default=str)
    def load_json(self):
        with open('savedata.json','r') as fp:
            to_load = json.load(fp)
            for entry in to_load['Entries']:
                entry_obj = Entry([entry['Date'],entry['Description'],entry['Debit'],entry['Credit'],entry['Bank']])
                entry_obj.load_json(entry)

    def get_most_recent_uncategorized_entry(self):
        self.entries.sort(key=lambda x: x.date, reverse=True)
        for entry in self.entries:
            if entry.categorized != True:
                return entry


class PynanceFramer():
    def __init__(self, root):
        self.root = root 
        self.pynance = None
        
        self.category_frame = None
        self.is_visible = False 
        
        self.current_entry = None
    def toggle_categorization(self):
        self.is_visible = not self.is_visible
        
        if self.is_visible:
            self.category_frame = tk.Frame(self.root)
            self.category_frame.grid(row=1,column=0)
            
            self.display_next_entry()
        else:
            self.category_frame.destroy()
            self.category_frame=None
        self.submit = tk.Button(self.root, text="Submit", command=self.submit)
        self.submit.grid(row=2, column=0)
    def submit(self):
        if self.current_entry is not None:
            self.current_entry.categorized=True
            for seg in self.sliders.segments:
                cat = CategoryInfo()
                cat.supercategory = seg.supercategory_selected.get()
                cat.category = seg.selected.get()
                cat.percentage = seg.entry.get()
                cat.total = seg.money_entry.get()
                self.current_entry.categories.append(cat)
        self.display_next_entry()
        
        
    def display_next_entry(self):
        entry = self.pynance.get_most_recent_uncategorized_entry()
        print(entry)
        self.current_entry = entry
        for widget in self.category_frame.winfo_children():
            widget.destroy()
            
        if entry == None:
            tk.Label(self.category_frame, text="Everything Categorized").grid(row=0, column=0)
            return
        tk.Label(self.category_frame, text=entry.description + " " + str(entry.debit), font=("Arial", 12)).grid(row=0,column=0)
        
        self.sliders = MultiSlideBar(self.category_frame, entry, self.pynance.categories,width=500, height=50)
        self.sliders.grid(row=1,column=0)
        
        
        
    def open_file_dialog(self):
        initial_path = os.path.dirname(os.path.abspath(__file__))
        file_path = filedialog.askopenfilename(initialdir=initial_path, title="Select file to load...")
        self.pynance.import_account_history(os.path.basename(file_path))