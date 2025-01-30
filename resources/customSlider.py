from tkinter import *
from PIL import Image,ImageTk

class Slider():
    def __init__(self, canvas, radius,x,y,number):
        self.canvas = canvas
        self.radius = radius
        self.x = x 
        self.y = y
        self.id = None
        self.l_segment = None 
        self.r_segment = None
        self.number = number
        self.number_id = None
        
    def check_hit(self, x):
        if self.x - self.radius <= x and x <= self.x + self.radius:
            return True 
        return False
    
    def draw_self(self):
        self.id = self.canvas.create_oval(self.x - self.radius, self.y- self.radius, self.x + self.radius, self.y + self.radius,fill='blue')
        self.number_id = self.canvas.create_text(self.x, self.y+20, text=self.number)
        return self.id
    
    def move(self, new_x):
        self.x = new_x
        self.canvas.coords(self.id, self.x - self.radius, self.y- self.radius, self.x + self.radius, self.y + self.radius)
        self.canvas.coords(self.number_id, self.x, self.y+20)        
        
class Segment():
    def __init__(self, parent, l_slider, r_slider, color):
        self.frame = Frame()
        
        self.parent = parent
        self.canvas = parent.canvas
       
        self.l_slider = l_slider
        self.r_slider = r_slider
        
        if self.l_slider:
            self.x_l = self.l_slider.x
        else:
            self.x_l = 25
        if self.r_slider:
            self.x_r = self.r_slider.x 
        else:
            self.x_r = self.parent.width - 25
            
        self.locked = False            
            
        self.percentage = round(((self.x_r - self.x_l) / (self.parent.width - 50))*100,1)
        print(self.percentage)
        self.color = color
        self.color_line_id = None 

        self.lock_id = None
        icon = Image.open("C:/Users/maxws/Documents/Code/pynance/resources/img/lock.png")
        scaled_image = icon.resize((10, 10))
        self.icon = ImageTk.PhotoImage(scaled_image)
        
        
        self.entry = Entry(self.frame, width=20, bg=self.color)
        self.entry.insert(0, "0")
        self.entry.bind("<Return>", lambda e,s=self: self.parent.update_sliders_from_perc_entry(e,s))
        self.entry.grid(row=0, column=0)
        
        self.money_entry = Entry(self.frame, width=20, bg=self.color)
        self.money_entry.insert(0, "0")
        self.money_entry.bind("<Return>", lambda e,s=self: self.parent.update_sliders_from_money_entry(e,s))
        self.money_entry.grid(row=0,column=1)
        
        option_list = []
        supercategory_list = []
        for supercategory,categories in self.parent.categories.items():
            option_list.append("---" + str(supercategory) + "---")
            supercategory_list.append(supercategory)
            for category in categories:
                option_list.append(category)
        self.selected = StringVar(self.frame)
        self.selected.set("Select category")
        self.dropdown = OptionMenu(self.frame, self.selected, *option_list,command=self.update_supercategory)
        self.dropdown.config(width=20)
        self.dropdown.grid(row=0,column=2)
        
        self.supercategory_selected = StringVar(self.frame)
        self.supercategory_selected.set("Need/Want")
        self.supercategory_dropdown = OptionMenu(self.frame, self.supercategory_selected, *supercategory_list)
        self.supercategory_dropdown.config(width=20)
        self.supercategory_dropdown.grid(row=0,column=3)
    def update_supercategory(self,value):
        for supercategory,categories in self.parent.categories.items():
            if value in categories:
                self.supercategory_selected.set(supercategory)
                
    def draw_self(self):
        if self.l_slider:
            self.x_l = self.l_slider.x
        else:
            self.x_l = 25
        if self.r_slider:
            self.x_r = self.r_slider.x
        else:
            self.x_r = self.parent.width - 25
        
        self.percentage = round(((self.x_r - self.x_l) / (self.parent.width - 50))*100,1)
        
#        self.label_id = self.canvas.create_text(mid_x, self.parent.height/2, text=self.label_str)
        self.color_line_id = self.canvas.create_line(self.x_l, self.parent.height/2, self.x_r, self.parent.height/2, width=8, fill=self.color)
        if self.locked:
            self.lock_id = self.canvas.create_image(((self.x_r-self.x_l)/2) + self.x_l,self.parent.height/2,image=self.icon,anchor=CENTER)

        self.entry.delete(0,END)
        self.entry.insert(0, f"{self.percentage}")
        dollars = round(self.parent.fin_entry.debit*self.percentage/100,2)
        self.money_entry.delete(0,END)
        self.money_entry.insert(0,f"${dollars}")
    def new_r_slider(self, slider):
        self.r_slider = slider
        self.x_r = self.r_slider.x
    def get_transaction_amount(self):
        pass
    def __repr__(self):
        return "{x}--{pe}%--{xr}".format(x=self.x_l, pe=self.percentage, xr=self.x_r)

class Slider2(Frame):
    OVAL_RADIUS = 10
    LINE_THICKNESS = 10
    
    
    def __init__(self, window,entry, categories,width=800, height=100):
        Frame.__init__(self, window, height=height, width=width)
        self.window = window
        min_val = 0
        max_val = 100
        self.width = width 
        self.height = height 
#        self.letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
#        self.letter_ctr = 0
        self.colors=["OliveDrab1","SkyBlue4","medium purple","PaleVioletRed4"]
        self.color_ctr = 0
        
        self.canvas = Canvas(self, height=height, width=width)
        self.canvas.create_line(25, height/2, width-25, height/2, width=Slider2.LINE_THICKNESS,fill='deep sky blue')
        self.canvas.create_rectangle(3,3,width-3,height-3,width=1)
        self.canvas.bind("<Button-1>", self.add_slider)
        self.canvas.grid(row=0,column=0)
        
        self.segments = []
        self.sliders = []
        self.fin_entry = entry
        self.categories = categories
        
        seg = Segment(self, None, None,self.colors[self.color_ctr])
        self.color_ctr+=1
        seg.frame.grid(column=0, row=2)
        seg.draw_self()
        self.segments.append(seg)

#        self.grid(row=3,column=0)
        


    def set_financial_entry(self, ent):
        self.fin_entry = ent   
        print(ent)

        

    def add_slider(self, event):
        # Bypass this function if we've clicked on a slider
        for slider in self.sliders:
            if slider.check_hit(event.x):
                return 
        if len(self.sliders) >=3:
            return
        
        slider = Slider(self.canvas, Slider2.OVAL_RADIUS, event.x, self.height / 2, self.color_ctr)
        slider_id = slider.draw_self()
        self.canvas.tag_bind(slider_id, "<B1-Motion>", lambda e, s=slider: self.move_slider(e,s))
        self.sliders.append(slider)
        
        # need to split the segment
        for segment in self.segments:
            if segment.x_l < event.x and event.x < segment.x_r:
                print("You clicked on segment:" + segment.color)
                # clicked within this segment
                new_seg = Segment(self, slider, segment.r_slider,self.colors[self.color_ctr])
                self.color_ctr+=1
                if segment.r_slider:
                    segment.r_slider.l_segment = new_seg
                segment.new_r_slider(slider)
                self.segments.append(new_seg)
                new_seg.frame.grid(column=0,row=len(self.segments)+1)
                
                slider.l_segment = segment 
                slider.r_segment = new_seg
                segment.locked = False
                break
        
        self.update_labels_and_entries()
    def move_slider(self, event, slider):
        x = max(25, min(event.x, self.width - 25)) 
        # check if we are traveling left over another slider
        if x < slider.l_segment.x_l + 2:
            x = slider.l_segment.x_l + 2
        # check if we are traveling right over another slider
        if x > slider.r_segment.x_r - 2:
            x = slider.r_segment.x_r - 2
        # move da slider
        slider.move(x)
        # unlock the affected segments
        slider.l_segment.locked = False 
        slider.r_segment.locked = False        
        
        self.update_labels_and_entries()
        
    def update_labels_and_entries(self):
        self.clear_segments()

        for segment in self.segments:
            segment.draw_self()
        for slider in self.sliders:
            self.canvas.tag_raise(slider.id)
            self.canvas.tag_raise(slider.number_id)
            
    def update_sliders_from_dollar_entry(self, event, segment):
        pass        
    
        # before implementing this, fix all the duplicated stuff in update_sliders_from_perc_entry
    
    def update_sliders_from_perc_entry(self, event, segment):        
        total_width = self.width - 50
        unlocked_segments = []
        for test_segment in self.segments:
            if test_segment is segment:
                continue
            else:
                if test_segment.locked == True:
                    continue
                else:
                    unlocked_segments.append(test_segment)
        
        match len(unlocked_segments):
            case 0:
                print("Nobody is unlocked")
                if len(self.segments) != 1:
                    pass
                else:
                    # Functionality: make a new segment that has the correct value
                    x_should_be = (float(segment.entry.get())*total_width/100)+25
                    event.x = x_should_be
                    self.add_slider(event)
                    segment.locked = True
                
            case 5:
                print("There are " + str(len(unlocked_segments)) + " unlocked")
                old_perc = segment.percentage
                new_perc = float(segment.entry.get())
                delta_perc = old_perc - new_perc
                unlocked_segments.sort(key = lambda x: x.x_l)
                
                seg_percentages = []
                for i in range(0, len(unlocked_segments)):
                    seg_percentages.append(unlocked_segments[i].percentage)
                seg_proportions = []
                for i in range(0, len(unlocked_segments)):
                    prop = seg_percentages[i] / (sum(seg_percentages)) * 100
                    seg_proportions.append(prop)
                
                rs = []
                #print(len(unlocked_segments))
                for i in range(0, len(unlocked_segments)):
                    seg_new_width = seg_percentages[i] + (delta_perc * seg_proportions[i] / 100)
                    seg_r = seg_new_width * total_width / 100
                    rs.append(seg_r)
                                            
                rs_idx = 0  
                all_segments = sorted(self.segments, key=lambda x: x.x_l)
                for seg in all_segments[:-1]:
                    if seg.locked == True and seg is not segment:
                        continue
                    if seg is segment:
                        if seg.l_slider is None:
                            seg.r_slider.move((float(segment.entry.get())*total_width/100) + 25)
                        else:
                            seg.r_slider.move((float(segment.entry.get())*total_width/100) + seg.l_slider.x)
                    else:
                        if seg.l_slider is None:
                            seg.r_slider.move(rs[rs_idx] + 25)
                            rs_idx += 1                        
                        else:
                            seg.r_slider.move(seg.l_slider.x + rs[rs_idx])
                            rs_idx += 1            
            case _:
#                segments = sorted(self.segments, key=lambda x: x.x_l)
                print(self.segments)
                
                pass
        segment.locked = True
        self.update_labels_and_entries()
        
    def clear_segments(self):
        for segment in self.segments:
            if segment.color_line_id:
                self.canvas.delete(segment.color_line_id)
            if segment.lock_id:
                self.canvas.delete(segment.lock_id)