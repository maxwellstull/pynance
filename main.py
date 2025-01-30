
import sys 
sys.path.append('resources')
import tkinter as tk
from pynance import Pynance, PynanceFramer

def main():
    
    p = Pynance()

    root = tk.Tk()
    root.title("FBGM")
    
    e = PynanceFramer(root)
    e.pynance = p

#    p.import_account_history('AccountHistory.csv')
#    p.import_account_history('bigbank.CSV')
    
    buttons_frame = tk.Frame(root)
    buttons_frame.grid(column=0, row=0)
    
    load_button = tk.Button(buttons_frame, text="Load from File", command=e.open_file_dialog)
    load_button.grid(column=0, row=0)
    
    button = tk.Button(buttons_frame, text="Save", command=p.save_data)
    button.grid(column=1,row=0)
    
    button2 = tk.Button(buttons_frame, text="Categorize Entries",command=e.toggle_categorization)
    button2.grid(column=2,row=0)
    
    root.mainloop()
#    p.save_data()


if __name__ == "__main__":
    main()