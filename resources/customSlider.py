from tkinter import *
from tkinter.ttk import *

class Slider2(Frame):
    OVAL_RADIUS = 10
    LINE_THICKNESS = 10
    
    
    def __init__(self, window, width=800, height=100):
        Frame.__init__(self, window, height=height, width=width)
        self.window = window
        min_val = 0
        max_val = 100
        self.width = width 
        self.height = height 
        
        self.canvas = Canvas(self, height=height, width=width)
        self.canvas.create_line(25, height/2, width-25, height/2, width=Slider2.LINE_THICKNESS,fill='deep sky blue')
        
        self.sliders = []
        self.slider_handles = []
        self.letter_handles = []
        self.percentage_entries = []
        self.canvas.bind("<Button-1>", self.add_slider)
        self.letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.canvas.pack()

    def add_slider(self, event):
        for slider in self.sliders:
            if event.x > slider - Slider2.OVAL_RADIUS  and event.x < slider + Slider2.OVAL_RADIUS:
                return 
        
        x = event.x
        self.sliders.append(x)
        slider = self.canvas.create_oval(x-Slider2.OVAL_RADIUS, self.height / 2 - Slider2.OVAL_RADIUS, x+Slider2.OVAL_RADIUS, self.height / 2 + Slider2.OVAL_RADIUS,fill='blue')
        self.slider_handles.append(slider)
        self.canvas.tag_bind(slider, "<B1-Motion>", lambda e, s=slider: self.move_slider(e,s))
        self.sliders.sort()
        print(self.sliders)
        self.update_labels_and_entries()
    def move_slider(self, event, slider):
        x = max(10, min(event.x, self.width - 10))
        self.canvas.coords(slider, x - Slider2.OVAL_RADIUS, self.height // 2 - Slider2.OVAL_RADIUS, x + Slider2.OVAL_RADIUS, self.height // 2 + Slider2.OVAL_RADIUS)
        index = self.slider_handles.index(slider)
        self.sliders[index] = x
        self.sliders.sort()
        self.update_labels_and_entries()
        
    def update_percentages(self):
        self.clear_labels()
        positions = [25] + self.sliders + [self.width - 25]
        total_width = self.width - 50
        
        for i in range(len(positions) - 1):
            percentage = round((positions[i+1] - positions[i]) / total_width * 100, 1)
            mid_x = (positions[i] + positions[i+1]) / 2
            
            label_id = self.canvas.create_text(mid_x, self.height / 2, text=f"{percentage}%")
            self.labels.append(label_id)
    
    def update_labels_and_entries(self):
        self.clear_labels_and_entries()

        positions = [25] + self.sliders + [self.width - 25]
        total_width = self.width - 50
        
        for i in range(len(positions) -1):
            letter = self.letters[i]
            mid_x = (positions[i] + positions[i+1]) /2
            percentage = round((positions[i+1] - positions[i]) / total_width * 100, 1)
            
            letter_id = self.canvas.create_text(mid_x, self.height/2, text=letter)
            self.letter_handles.append(letter_id)
            
            entry = Entry(self, width=20)
            entry.insert(0, f"{percentage}")
            entry.bind("<Return>", lambda e, idx=i: self.update_sliders_from_entry(idx))
            entry.pack()
#            entry.grid(row=1, column=i, padx=5)
            
            self.percentage_entries.append(entry)
    
    def update_sliders_from_entry(self, index):
        try:
            new_percentage = float(self.percentage_entries[index].get()) / 100
            total_width = self.width - 50
            new_x = int(new_percentage * total_width) + 25
        
            if index > 0 and new_x <= self.sliders[index - 1]:
                return 
            if index < len(self.sliders) and new_x >= self.sliders[index +1]:
                return 
            
            self.sliders[index] = new_x 
            self.canvas.coords(self.slider_handles[index], new_x-Slider2.OVAL_RADIUS, self.height/2 - Slider2.OVAL_RADIUS,new_x+Slider2.OVAL_RADIUS, self.height/ 2 + Slider2.OVAL_RADIUS)
            
            self.update_labels_and_entries()
        except ValueError:
            print("Shit")
            pass
    def clear_labels(self):
        for label in self.labels:
            self.canvas.delete(label)
        self.labels.clear()
        
    def clear_labels_and_entries(self):
        for label in self.letter_handles:
            self.canvas.delete(label)
        self.letter_handles.clear()
        
        for entry in self.percentage_entries:
            entry.destroy()
        self.percentage_entries.clear()