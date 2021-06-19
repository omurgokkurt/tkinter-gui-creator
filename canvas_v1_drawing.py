from Tkinter import *
import colors_list
from random import choice
from BetterScrollbar import CustomScrollbar
from ColorlistWidget import ColorWidget
from ColorPicker import ColorPicker
from webcolors import rgb_to_hex
from webcolors import hex_to_rgb
from PIL import Image as PImage
from PIL import ImageTk
import tkFont

class GUI(Frame):
    def __init__(self, master):
        Frame.__init__(self,master)
        self.initUI(master)

    def initUI(self, master):
        self.color_1 = "gray30"
        self.color_2 = "gray20"
        self.color_3 = "gray10"
        self.color_4 = "gray30"
        self.color_button_on = "gray40"
        self.color_button_off = "gray10"
        self.configure(bg=self.color_3)
        self.selected_layer = ""
        self.layer_number = 1

        # Toolbar
        self.frame_tools = Frame(self, bg=self.color_3)
        self.pimage1 = PImage.open("move.png")
        self.image1 = ImageTk.PhotoImage(self.pimage1)

        self.pimage2 = PImage.open("pencil.png")
        self.image2 = ImageTk.PhotoImage(self.pimage2)

        self.pimage3 = PImage.open("oval.png")
        self.image3 = ImageTk.PhotoImage(self.pimage3)

        self.pimage4 = PImage.open("rect.png")
        self.image4 = ImageTk.PhotoImage(self.pimage4)


        self.button_move = Button(self.frame_tools, image=self.image1,fg="white", relief="flat", bg=self.color_button_off, command=self.choose_move)
        self.button_move.pack(pady=5)
        self.button_draw = Button(self.frame_tools, image=self.image2, fg="white", relief="flat", bg=self.color_button_off,command=self.choose_draw)
        self.button_draw.pack(pady=5)
        self.button_oval = Button(self.frame_tools, image=self.image3,fg="white", relief="flat", bg=self.color_button_off, command=self.choose_oval)
        self.button_oval.pack(pady=5)
        self.button_rect = Button(self.frame_tools, image=self.image4,fg="white", relief="flat", bg=self.color_button_off, command=self.choose_rect)
        self.button_rect.pack(pady=5)

        self.frame_tools.pack(pady=(20, 0), padx=(10, 0), side=LEFT, fill=Y, expand=True)

        # Canvas
        self.frame1 = Frame(self, bg=self.color_3)
        self.canvas1 = Canvas(self.frame1, width=800, height=500, bg="black",cursor="cross")
        self.canvas1.pack(padx=(10,10), pady=20)
        self.img_bg = PhotoImage(file="514.gif")
        self.bg = self.canvas1.create_image(0,0, image=self.img_bg, anchor=NW)
        self.canvas1.bind("<Button-1>", self.on_click)
        self.canvas1.bind("<B1-Motion>", self.on_motion)
        self.canvas1.bind("<ButtonRelease-1>", self.off_click)
        self.canvas1.bind("<Motion>", self.show_info)
        self.frame1.pack(side=LEFT)

        # Layers
        self.frame_layer = Frame(self, bg=self.color_2)
        self.frame_layerb = Frame(self.frame_layer)
        self.button_add_layer = Button(self.frame_layerb, relief="flat", bg=self.color_2,fg="white", text="New Layer", command=self.add_layer)
        self.button_add_layer.pack(fill=X, side=LEFT, expand=True)
        self.button_del_layer = Button(self.frame_layerb, relief="flat", bg=self.color_2,fg="white", text="Delete", state=DISABLED, command=self.del_layer)
        self.button_del_layer.pack(fill=X, side=LEFT,expand=True)
        self.layers = Listbox(self.frame_layer, bd=0,highlightthickness=0, width=49,fg="white", relief="flat", bg=self.color_2, selectbackground=self.color_3,highlightcolor=self.color_3, highlightbackground = self.color_3)
        self.layers.grid(row=0,column=0)
        self.layers.bind("<<ListboxSelect>>", self.select_layer)
        self.layer_scroll = CustomScrollbar(self.frame_layer, self.layers,color1=self.color_2,color2=self.color_1,color3=self.color_1, command=self.layers.yview)
        self.layer_scroll.grid(row=0,column=1,padx=(0,5))
        self.layers.config(yscrollcommand=self.layer_scroll.set)
        self.frame_layerb.grid(row=1, columnspan=2, column=0, sticky=N + S)
        self.frame_layer.pack(pady=(20, 20), padx=(0, 10))

        # Color pick
        self.colorpick = ColorPicker(self, detail=16, bg=self.color_2)
        self.colorpick.pack(padx=(0,10), fill=X,ipady=10)


        self.add_layer(name="Background")
        self.canvas1.create_rectangle(0,0,self.canvas1.winfo_reqwidth(),self.canvas1.winfo_reqheight(), fill="white", tags="Background")

        self.add_layer()


        self.infobar = Label(self, bg=self.color_1, fg="white", text="")

        self.pack()




    def add_layer(self,name=""):
        if name == "":
            self.layers.insert(0, "Layer"+str(self.layer_number))
            self.layer_number += 1
        else:
            self.layers.insert(0, name)

        self.layers.selection_clear(0,END)
        self.layers.select_set(0)
        self.select_layer()



    def del_layer(self):
        self.canvas1.delete(self.selected_layer)
        self.layers.delete(self.layers.curselection())
        self.button_del_layer.configure(state=DISABLED)


    def select_layer(self,event="None"):
        self.selected_layer = self.layers.get(self.layers.curselection())
        self.button_del_layer.configure(state=NORMAL)


    def choose_move(self):
        self.current_tool = "Move"
        self.button_move.configure(bg=self.color_button_on)
        self.button_oval.configure(bg=self.color_button_off)
        self.button_rect.configure(bg=self.color_button_off)
        self.button_draw.configure(bg=self.color_button_off)
    def choose_draw(self):
        self.current_tool = "Draw"
        self.button_draw.configure(bg=self.color_button_on)
        self.button_move.configure(bg=self.color_button_off)
        self.button_oval.configure(bg=self.color_button_off)
        self.button_rect.configure(bg=self.color_button_off)
    def choose_oval(self):
        self.current_tool = "Oval"
        self.button_move.configure(bg=self.color_button_off)
        self.button_oval.configure(bg=self.color_button_on)
        self.button_rect.configure(bg=self.color_button_off)
        self.button_draw.configure(bg=self.color_button_off)
    def choose_rect(self):
        self.current_tool = "Rect"
        self.button_move.configure(bg=self.color_button_off)
        self.button_oval.configure(bg=self.color_button_off)
        self.button_rect.configure(bg=self.color_button_on)
        self.button_draw.configure(bg=self.color_button_off)
    def show_info(self,event):
        if self.canvas1.find_overlapping(event.x-1,event.y-1,event.x+1,event.y+1) == (1,) or self.canvas1.find_overlapping(event.x-1,event.y-1,event.x+1,event.y+1) == ():
            self.infobar.configure(text="x:"+str(event.x) + " " + "y:"+str(event.y), fg="gray80")
        else:
            self.infobar.configure(text="x:" + str(event.x) + " " + "y:" + str(event.y), fg="white")


    def on_click(self, event):
        if self.selected_layer != "":
            if self.current_tool == "Oval":

                self.current_item = self.canvas1.create_oval(event.x,event.y,event.x,event.y, outline=self.colorpick.color)
                self.x = event.x
                self.y = event.y
            elif self.current_tool == "Rect":
                self.current_item = self.canvas1.create_rectangle(event.x,event.y,event.x,event.y, outline=self.colorpick.color)
                self.x = event.x
                self.y = event.y
            elif self.current_tool == "Draw":
                self.x = event.x
                self.y = event.y

            elif self.current_tool == "Move":
                self.x = event.x
                self.y = event.y
                self.canvas1.itemconfig(self.selected_layer)

    def on_motion(self,event):
        if self.selected_layer != "":
            if self.current_tool == "Oval" or self.current_tool == "Rect":
                self.canvas1.coords(self.current_item, self.x, self.y, event.x, event.y)
            elif self.current_tool == "Draw":
                # self.canvas1.create_line(self.x, self.y, event.x, event.y,width=1.2, fill=self.colorpick.colors,tags=self.selected_layer)
                self.canvas1.create_line(self.x, self.y, event.x,event.y, smooth=1, fill=self.colorpick.color,tags=self.selected_layer)
                self.x = event.x
                self.y = event.y
            elif self.current_tool == "Move":
                dx = event.x - self.x
                dy = event.y - self.y
                self.canvas1.move(self.selected_layer, dx, dy)
                self.x = event.x
                self.y = event.y

    def off_click(self, event):
        if self.selected_layer != "":
            if self.current_tool == "Oval" or self.current_tool == "Rect":
                self.canvas1.itemconfig(self.current_item, fill=self.colorpick.color)
                self.canvas1.itemconfig(self.current_item, tags=self.selected_layer)









def main():
    root = Tk()
    app = GUI(root)
    root.mainloop()
main()


