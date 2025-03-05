import sys
sys.path.append('resources')
import tkinter as tk
from tkSliderWidget import Slider

from customSlider import MultiSlideBar
window = tk.Tk()
window.title("My GUI")

label = tk.Label(window, text="Hello, World!")
label.pack()

button = tk.Button(window, text="Click Me", command=lambda: print("Button clicked!"))
button.pack()

slider = Slider(window, width=400, height=60, min_val=0,max_val=100, init_lis=[30,60,80], show_value=True)
slider.pack()

sliders = MultiSlideBar(window, width=500, height=200)
sliders.pack()

window.mainloop()