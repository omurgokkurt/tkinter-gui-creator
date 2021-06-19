from Tkinter import *
import colors_list
from random import choice
from BetterScrollbar import CustomScrollbar
from ColorlistWidget import ColorWidget
from ColorPicker import ColorPicker
from webcolors import rgb_to_hex
from webcolors import hex_to_rgb
import base64
import io
import tkFileDialog
from PIL import Image as PImage
from PIL import ImageTk
import tkMessageBox
import tkFont
import tkColorChooser
import tkSimpleDialog
from ttk import Combobox
import encoded_icon_list
class GUI(Frame):
    def __init__(self, master):
        Frame.__init__(self,master)
        self.master = master
        self.initUI()
    def ask_canvas_size(self):
        self.master.title("New File")
        self.frame_ask = Frame(self)

        self.canvas_name_label = Label(self.frame_ask, text="File name: ")
        self.canvas_name_label.pack(side=LEFT)
        self.canvas_name_entry = Entry(self.frame_ask)
        self.canvas_name_entry.pack(side=LEFT)

        self.canvas_width_label = Label(self.frame_ask, text="Width: ")
        self.canvas_width_label.pack(side=LEFT, padx=(5,0))
        self.canvas_width_entry=Entry(self.frame_ask)
        self.canvas_width_entry.pack(side=LEFT)
        self.canvas_width_entry.insert(0,800)

        self.canvas_height_label = Label(self.frame_ask, text="Height: ")
        self.canvas_height_label.pack(side=LEFT, padx=(5,0))
        self.canvas_height_entry=Entry(self.frame_ask)
        self.canvas_height_entry.pack(side=LEFT)
        self.canvas_height_entry.insert(0, 800)
        self.canvas_size_ask_button = Button(self.frame_ask, text="Create", command=self.check_init)
        self.canvas_size_ask_button.pack(side=LEFT,padx=5)
        self.ask_info_bar = Label(self.frame_ask,text="")
        self.ask_info_bar.pack(side=LEFT)

        self.frame_ask.pack(pady=5,padx=5)
        self.pack()
    def check_init(self):
        try:
            if self.canvas_name_entry.get().strip() == "" or int(self.canvas_width_entry.get())<= 50 or int(self.canvas_height_entry.get())<=50:
                self.ask_info_bar.configure(text="Please check the information and try again.\n(Minimum size is 50x50)")
            else:
                self.frame_ask.pack_forget()
                self.pack_forget()
                self.initUI(self.canvas_name_entry.get(), w=self.canvas_width_entry.get(), h=self.canvas_height_entry.get())

        except ValueError:
            self.ask_info_bar.configure(text="Please check the information and try again.")
    def initUI(self, name="gui", w=1500, h=900):
        self.name = name
        self.master.title(name)
        self.color_1 = "gray30"
        self.color_2 = "gray10"
        self.color_main_bg = "gray15"
        self.color_4 = "gray30"
        self.listbox_bgcolor = "gray10"
        self.color_toolbar_options_bg = "gray5"
        self.color_toolbar_bg = "gray5"
        self.color_radio_on = "gray10"
        self.color_radio_off = "gray5"
        self.color_radio_active = "gray30"
        self.color_lb_selected = "#2E4172"
        self.configure(bg=self.color_main_bg)
        self.icon = "505.ico"
        self.selected_layer = ""
        self.image_dump = []
        self.layer_number = 1
        self.tool_var = StringVar()
        self.tool_var.set("Move")
        self.tool_var.trace("w", self.show_corners)
        self.button_text_var = StringVar()
        self.button_text_var.set("Button")
        self.button_text_var.trace("w", self.set_button_attributes)




        self.layer_dict = {}



        # MENU
        self.top_menu = Frame(self, height=30, bg=self.color_main_bg)
        self.top_menu.pack(fill=X)
        self.top_menu.pack_propagate(0)
        self.button_export = Button(self.top_menu, disabledforeground="gray60", text="Export", relief="flat", bg=self.color_main_bg, fg= "white", bd=0, activebackground=self.color_1, activeforeground="white", command=self.export)
        self.button_export.pack(fill=Y, ipadx=5, side=LEFT)
        #---

        # TOOLBAR TOOL OPTIONS
        self.all_options = []
        self.frame_tools_option = Frame(self, bg=self.color_toolbar_options_bg)
        self.invisible_text= Label(self.frame_tools_option, width=0,height=2,bg=self.color_toolbar_options_bg)
        self.invisible_text.pack()
        self.all_options.append(self.invisible_text)

        #---

        #---BUTTON OPTIONS
        self.relief_var = StringVar()
        self.relief_var.set("groove")
        self.frame_tools_option_button = Frame(self.frame_tools_option, bg=self.color_toolbar_options_bg)
        self.label_button_text = Label(self.frame_tools_option_button, text="Text: ", fg="white", bg=self.color_toolbar_options_bg)
        self.label_button_text.pack(side=LEFT)
        self.entry_button_text = Entry(self.frame_tools_option_button, width=30, textvariable=self.button_text_var)
        self.entry_button_text.pack(side=LEFT)

        self.label_button_relief = Label(self.frame_tools_option_button, text="Relief: ", fg="white", bg=self.color_toolbar_options_bg)
        self.label_button_relief.pack(side=LEFT,padx=(30,0))
        self.combo_button_relief = Combobox(self.frame_tools_option_button, height=50,state="readonly", values=["flat","groove","raised","sunken","ridge","solid"], width=10)
        self.combo_button_relief.current(0)
        self.combo_button_relief.bind("<<ComboboxSelected>>", self.set_button_attributes)
        self.combo_button_relief.pack(side=LEFT)

        self.label_button_font = Label(self.frame_tools_option_button, text="Font: ", fg="white", bg=self.color_toolbar_options_bg)
        self.label_button_font.pack(side=LEFT,padx=(30,0))
        self.combo_button_font = Combobox(self.frame_tools_option_button, height=50,state="readonly", values=sorted(tkFont.families()), width=10)
        self.combo_button_font.bind("<<ComboboxSelected>>", self.set_button_attributes)
        self.combo_button_font.current(50)
        self.combo_button_font.pack(side=LEFT)
        sizes = []
        for i in range(50):
            sizes.append(i)
        self.combo_button_font_size = Combobox(self.frame_tools_option_button, state="readonly",values=sizes, width=5)
        self.combo_button_font_size.current(9)
        self.combo_button_font_size.bind("<<ComboboxSelected>>", self.set_button_attributes)
        self.combo_button_font_size.pack(side=LEFT)

        self.color_button_bg_label = Label(self.frame_tools_option_button, text="Background Color: ", fg="white", bg=self.color_toolbar_options_bg)
        self.color_button_bg_label.pack(padx=(30,0), side=LEFT)
        self.color_button_bg = Canvas(self.frame_tools_option_button, bg="#f0f0f0",width=60,height=19, bd=0, highlightthickness=0)
        self.color_button_bg.pack(side=LEFT)
        self.color_button_bg.bind("<Button-1>", self.choose_color)

        self.color_button_fg_label = Label(self.frame_tools_option_button, text="Foreground Color: ", fg="white", bg=self.color_toolbar_options_bg)
        self.color_button_fg_label.pack(padx=(30,0), side=LEFT)
        self.color_button_fg = Canvas(self.frame_tools_option_button, bg="black",width=60,height=19, bd=0, highlightthickness=0)
        self.color_button_fg.pack(side=LEFT, padx=(5,0))
        self.color_button_fg.bind("<Button-1>", self.choose_color)

        self.image_select_button = Button(self.frame_tools_option_button, text = "Add Image", command=self.button_add_image)
        self.image_select_button.pack(side=LEFT, padx=(30,0))
        self.invisible_text= Label(self.frame_tools_option_button, width=0,height=2,bg=self.color_toolbar_options_bg)
        self.invisible_text.pack()

        self.all_options.append(self.frame_tools_option_button)
        #--- TEXT OPTIONS
        self.frame_tools_option_text = Frame(self.frame_tools_option, bg=self.color_toolbar_options_bg)
        self.label_text_text = Label(self.frame_tools_option_text, text="Text: ", fg="white",bg=self.color_toolbar_options_bg)
        self.label_text_text.pack(side=LEFT)
        self.entry_text_text = Entry(self.frame_tools_option_text, width=30)
        self.entry_text_text.pack(side=LEFT)
        self.entry_text_text.insert(END,"Enter text")

        self.label_text_font = Label(self.frame_tools_option_text, text="Font: ", fg="white", bg=self.color_toolbar_options_bg)
        self.label_text_font.pack(side=LEFT, padx=(30, 0))
        self.combo_text_font = Combobox(self.frame_tools_option_text, state="readonly", values=sorted(tkFont.families()),width=10)
        self.combo_text_font.current(50)
        self.combo_text_font.pack(side=LEFT)
        sizes = []
        for i in range(50):
            sizes.append(i)
        self.combo_text_font_size = Combobox(self.frame_tools_option_text, state="readonly", values=sizes, width=5)
        self.combo_text_font_size.current(9)
        self.combo_text_font_size.pack(side=LEFT)


        self.color_text_bg_label = Label(self.frame_tools_option_text, text="Background Color: ", fg="white", bg=self.color_toolbar_options_bg)
        self.color_text_bg_label.pack(padx=(30,0), side=LEFT)
        self.color_text_bg = Canvas(self.frame_tools_option_text, bg="#f0f0f0",width=60,height=19, bd=0, highlightthickness=0)
        self.color_text_bg.pack(side=LEFT)
        self.color_text_bg.bind("<Button-1>", self.choose_color)

        self.color_text_fg_label = Label(self.frame_tools_option_text, text="Foreground Color: ", fg="white", bg=self.color_toolbar_options_bg)
        self.color_text_fg_label.pack(padx=(30,0), side=LEFT)
        self.color_text_fg = Canvas(self.frame_tools_option_text, bg="black",width=60,height=19, bd=0, highlightthickness=0)
        self.color_text_fg.pack(side=LEFT, padx=(5,0))
        self.color_text_fg.bind("<Button-1>", self.choose_color)

        self.invisible_text= Label(self.frame_tools_option_text, width=0,height=2,bg=self.color_toolbar_options_bg)
        self.invisible_text.pack()

        self.all_options.append(self.frame_tools_option_text)
        #---
        self.frame_tools_option.pack(fill=X, pady=(0,5),ipadx=5)



        # TOOLBAR IMAGES
        self.pimage_move = PImage.open("move.png")
        self.image_move = ImageTk.PhotoImage(self.pimage_move)

        self.pimage_pencil = PImage.open("pencil.png")
        self.image_pencil = ImageTk.PhotoImage(self.pimage_pencil)

        self.pimage_add_button = PImage.open("add_button.png")
        self.image_add_button = ImageTk.PhotoImage(self.pimage_add_button)

        self.pimage_add_list = PImage.open("add_list.png")
        self.image_add_list = ImageTk.PhotoImage(self.pimage_add_list)

        self.pimage_add_text = PImage.open("add_text.png")
        self.image_add_text = ImageTk.PhotoImage(self.pimage_add_text)

        # TOOLS
        self.frame_tools = Frame(self, bg=self.color_toolbar_bg)
        self.radio_move = Radiobutton(self.frame_tools,height=10,width=10,  image=self.image_move, activebackground=self.color_radio_active, selectcolor=self.color_radio_on, bg=self.color_radio_off, offrelief="flat", indicatoron=False, variable=self.tool_var, value="Move", command=self.show_tool_options)
        self.radio_move.pack(pady=(8,5))
        self.radio_draw_button = Radiobutton(self.frame_tools,height=10,width=10, image=self.image_add_button, activebackground=self.color_radio_active, selectcolor=self.color_radio_on, bg=self.color_radio_off, offrelief="flat", indicatoron=False, variable=self.tool_var, value="Create Button", command=self.show_tool_options)
        self.radio_draw_button.pack(pady=5)
        self.radio_draw_list = Radiobutton(self.frame_tools,height=10,width=10, image=self.image_add_list, activebackground=self.color_radio_active, selectcolor=self.color_radio_on, bg=self.color_radio_off, offrelief="flat", indicatoron=False, variable=self.tool_var, value="Create List", command=self.show_tool_options)
        self.radio_draw_list.pack(pady=5)
        self.radio_draw_text = Radiobutton(self.frame_tools,height=10,width=10, image=self.image_add_text, activebackground=self.color_radio_active, selectcolor=self.color_radio_on, bg=self.color_radio_off, offrelief="flat", indicatoron=False, variable=self.tool_var, value="Create Label", command=self.show_tool_options)
        self.radio_draw_text.pack(pady=5)

        self.frame_tools.pack(side=LEFT, fill=Y, ipadx=4)

        # MAIN CANVAS
        self.frame_canvas = Frame(self, bg=self.color_1)
        self.main_canvas = Canvas(self.frame_canvas, width=w, height=h, bg="#f0f0f0", cursor="cross", highlightthickness=0,bd=0)
        self.main_canvas.pack(anchor=CENTER, expand=True)
        self.main_canvas.bind("<Motion>", self.entered)
        self.main_canvas.bind("<Button-1>", self.on_click)
        self.main_canvas.bind("<B1-Motion>", self.on_motion)
        self.main_canvas.bind("<ButtonRelease-1>", self.off_click)

        self.frame_canvas.pack(side=LEFT, padx=5, pady=(0,10), fill=BOTH, expand=True)

    #RIGHT PART
        self.frame_right = Frame(self, bg=self.color_main_bg)
        self.frame_right.pack(padx=(0,5), anchor="ne")
        # LAYERS
        self.frame_layer = Frame(self.frame_right, bg=self.color_2)
        self.frame_layerb = Frame(self.frame_layer, bg=self.color_1)
        self.button_add_layer = Button(self.frame_layerb, relief="flat", bg=self.color_1,fg="white", text="New Layer", command=self.add_layer)
        self.button_add_layer.pack(fill=X, side=LEFT, expand=True)
        self.button_del_layer = Button(self.frame_layerb, relief="flat", bg=self.color_1,fg="white", text="Delete", state=DISABLED, command=self.del_layer)
        self.button_del_layer.pack(fill=X, side=LEFT,expand=True)
        self.layers = Listbox(self.frame_layer, bd=0,highlightthickness=0, width=49,fg="white", relief="flat", bg=self.listbox_bgcolor, selectbackground=self.color_lb_selected,highlightcolor=self.color_main_bg, highlightbackground = self.color_main_bg, exportselection=False)
        self.layers.grid(row=0,column=0)
        self.layers.bind("<<ListboxSelect>>", self.select_layer)
        self.layers.bind("<Delete>", self.del_layer)
        self.layer_scroll = CustomScrollbar(self.frame_layer, self.layers, command=self.layers.yview)
        self.layer_scroll.grid(row=0,column=1)
        self.layers.config(yscrollcommand=self.layer_scroll.set)
        self.frame_layerb.grid(row=1, columnspan=2, column=0, sticky=N + S + E + W)
        self.frame_layer.pack()


        # FILE OPTIONS
        self.options_frame = Frame(self.frame_right,bg=self.color_main_bg)
        self.options_frame.pack(pady=30)
        self.options_frame_bg = Frame(self.options_frame)
        self.button_background_color_preview = Button(self.options_frame_bg, relief="flat", bd=0, bg="#f0f0f0")
        self.button_background_color_preview.pack(fill=X)
        self.button_background_color = Button(self.options_frame_bg, text="Choose Background Color", relief = "flat", bd=0, bg=self.color_1, fg="white", command=self.choose_color_bg)
        self.button_background_color.pack(ipady=3)
        self.options_frame_bg.pack(side=LEFT, padx=(0,10))


        self.options_frame_favicon = Frame(self.options_frame)
        self.button_favicon_preview = Button(self.options_frame_favicon, relief = "flat", bd=0,activebackground=self.color_toolbar_bg,bg=self.color_toolbar_bg, fg="white",)
        self.button_favicon_preview.pack(fill=X, ipady=3)
        self.button_favicon = Button(self.options_frame_favicon, relief="flat",  text="Choose Favicon", bg=self.color_1, fg="white", compound="right", command=self.choose_favicon)
        self.button_favicon.pack()

        self.options_frame_favicon.pack(side=LEFT)

        self.image1 = PImage.open("D:/Python Works/ENGR 102/Week 6 - Canvas/Favicons/505.ico")
        self.image1 = self.image1.resize((16, 16), PImage.ANTIALIAS)
        self.img1 = ImageTk.PhotoImage(self.image1)
        self.button_favicon_preview.configure(image=self.img1)





        # INITIALIZE
        self.pack(fill=BOTH, expand=True)
    def set_button_attributes(self, *args):
        if self.change:
            active_bg = rgb_to_hex(((hex_to_rgb(self.color_button_bg.cget("bg"))[0]-10),(hex_to_rgb(self.color_button_bg.cget("bg"))[1]-10),(hex_to_rgb(self.color_button_bg.cget("bg"))[2]-10)))
            highlight_color =rgb_to_hex(((hex_to_rgb(self.color_button_bg.cget("bg"))[0]+60),(hex_to_rgb(self.color_button_bg.cget("bg"))[1]+60),(hex_to_rgb(self.color_button_bg.cget("bg"))[2]+60)))
            self.layer_dict[self.selected_layer]["widget"].configure(text = self.entry_button_text.get(),highlightthickness=1,highlightbackground="blue",highlightcolor=highlight_color,bg=self.color_button_bg.cget("bg"), fg=self.color_button_fg.cget("bg"), relief=self.combo_button_relief.get(), font=(self.combo_button_font.get(), self.combo_button_font_size.get()), activeforeground=self.color_button_fg.cget("bg"), activebackground=active_bg)




    def choose_favicon(self):
        self.icon = tkFileDialog.askopenfilename(initialdir="/", title="Choose Favicon",filetypes=(("Icon", "*.ico *.png"), ("all files", "*.*")))
        print self.icon
        self.image = PImage.open(self.icon)
        self.image = self.image.resize((16, 16), PImage.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.image)
        self.button_favicon_preview.configure(image=self.img)




    def button_add_image(self):
        try:
            image_file = tkFileDialog.askopenfilename(initialdir="/", title="Select Image", filetypes=(("Image", "*.png *.jpg *.bitmap *.ico"), ("all files", "*.*")))
            pimage = PImage.open(image_file)
            self.image_dump.append(ImageTk.PhotoImage(pimage))

            self.layer_dict[self.selected_layer]["image"] = image_file
            self.layer_dict[self.selected_layer]["widget"].configure(image=self.image_dump[-1])
        except Exception:
            pass



    def entered(self, event=None):
        if self.selected_layer in self.layer_dict:
            if self.tool_var.get() == "Create Button":
                self.main_canvas.configure(cursor="sizing")
            if self.tool_var.get() == "Move":
                self.main_canvas.configure(cursor="fleur")
        else:
            if self.tool_var.get() == "Create Button":
                self.main_canvas.configure(cursor="plus")



    def choose_color_bg(self):
        color = tkColorChooser.askcolor(self.button_background_color_preview.cget("bg"))[1]
        self.button_background_color_preview.configure(bg=color, activebackground = color)
        self.main_canvas.configure(bg = color)

    def choose_color(self, event):
        color = tkColorChooser.askcolor(event.widget.cget("bg"))[1]
        event.widget.configure(bg=color)
        self.set_button_attributes()

    def show_tool_options(self):
        for i in self.all_options:
            i.pack_forget()
        if self.tool_var.get() == "Create Button":
            self.frame_tools_option_button.pack(padx=4,anchor=W,fill=X,expand=True)
        if self.tool_var.get() == "Create Label":
            self.frame_tools_option_text.pack(padx=4,anchor=W,fill=X,expand=True)



    def add_layer(self,event=None):
        message = "Layer Name:"
        cryptic_names = ["as", "def", "class", "list", "in", "print", "if", "else", "elif", "try", "except", "self", "import", "from"]
        while True:
            input = tkSimpleDialog.askstring("New Layer", message)
            if input.strip() != "" and input.replace(" ", "_") not in self.layers.get(0,END) and input not in cryptic_names:
                if input == None:
                    break
                layer_name = input.replace(" ", "_")
                self.layers.insert(0, layer_name)
                self.layer_number += 1
                self.layers.selection_clear(0,END)
                self.layers.select_set(0)
                self.select_layer()
                break
            else:
                if input.strip() == "":
                    message = "Layer name can not be empty. Please try again."
                if input.replace(" ", "_") in self.layers.get(0,END):
                    message = "Layer '%s' already exists. Please try another name" % input.replace(" ", "_")
                if input in cryptic_names:
                    message = "'%s' can not be used, try another name" % input



    def del_layer(self, event=None):
        if self.layers.size()>0:
            result = tkMessageBox.askyesno("Delete Layer", "Would you like to delete "+self.selected_layer+"?")
            if result:
                if self.selected_layer in self.layer_dict:
                    del self.layer_dict[self.selected_layer]
                last= self.layers.curselection()[0]
                self.main_canvas.delete(self.selected_layer)
                self.layers.delete(self.layers.curselection())
                self.button_del_layer.configure(state=DISABLED)
                try:
                    self.layers.select_set(last)
                    self.select_layer()
                except TclError:
                    try:
                        self.layers.select_set(last-1)
                        self.select_layer()
                    except TclError:
                        self.selected_layer = ""

    def select_layer(self,event="None"):
        self.main_canvas.itemconfig(self.selected_layer+"corner",state="hidden")
        self.selected_layer = self.layers.get(self.layers.curselection())
        if self.tool_var.get()== "Move":
            self.main_canvas.itemconfig(self.selected_layer + "corner", state="normal")
        print self.selected_layer
        self.button_del_layer.configure(state=NORMAL)
        self.change = False
        if self.selected_layer in self.layer_dict:
            if self.layer_dict[self.selected_layer]["type"] == "Button":
                self.entry_button_text.delete(0, END)
                self.entry_button_text.insert(END,self.layer_dict[self.selected_layer]["widget"].cget("text"))
                self.combo_button_relief.set(self.layer_dict[self.selected_layer]["widget"].cget("relief"))
                font = self.layer_dict[self.selected_layer]["widget"].cget("font").strip("{").strip("}").split(" ")
                font_style = ""
                if len(font) == 1:
                    self.combo_button_font.set(font)
                    self.combo_button_font_size.set("9")
                else:
                    for i in font[:-1]:
                        font_style+= i+" "
                    font_style = font_style[:-1]
                    self.combo_button_font.set(font_style.strip("}"))
                    self.combo_button_font_size.set(font[-1])
                self.color_button_bg.configure(bg=self.layer_dict[self.selected_layer]["widget"].cget("bg"))
                self.color_button_fg.configure(bg=self.layer_dict[self.selected_layer]["widget"].cget("fg"))
        self.change = True

    def show_corners(self, *args):
        if self.tool_var.get() == "Move":
            self.main_canvas.itemconfig(self.selected_layer+"corner", state="normal")
            print "yes"
        else:
            self.main_canvas.itemconfig(self.selected_layer + "corner", state="hidden")
            print "no"


    def on_click(self, event):
        if self.selected_layer != "":
            if self.tool_var.get() == "Create Button":
                if self.selected_layer not in self.layer_dict:
                    self.x = event.x
                    self.y = event.y
                    self.width = 0
                    self.height = 0
                    self.button_frame = Frame()
                    self.button_frame.pack_propagate(0)
                    self.button_frame.rowconfigure(0, weight=1)
                    self.button_frame.columnconfigure(0, weight=1)
                    self.layer_dict[self.selected_layer] = {}
                    self.layer_dict[self.selected_layer]["widget"] = Button(self.button_frame,text=self.entry_button_text.get(), activeforeground=self.color_button_fg.cget("bg"), activebackground=rgb_to_hex(((hex_to_rgb(self.color_button_bg.cget("bg"))[0]-30),(hex_to_rgb(self.color_button_bg.cget("bg"))[1]-30),(hex_to_rgb(self.color_button_bg.cget("bg"))[2]-30))),font=(self.combo_button_font.get(), self.combo_button_font_size.get()),fg=self.color_button_fg.cget("bg"), bg=self.color_button_bg.cget("bg"), relief=self.combo_button_relief.get(), compound="left")
                    if event.x % 10 <= 5:
                        self.layer_dict[self.selected_layer]["placex"] = event.x - event.x % 10
                    else:
                        self.layer_dict[self.selected_layer]["placex"] = event.x + 10 - event.x % 10
                    if event.y % 10 <= 5:
                        self.layer_dict[self.selected_layer]["placey"] = event.y - event.y % 10
                    else:
                        self.layer_dict[self.selected_layer]["placey"] = event.y + 10 - event.y % 10
                    self.layer_dict[self.selected_layer]["frame"] = self.main_canvas.create_window(self.layer_dict[self.selected_layer]["placex"], self.layer_dict[self.selected_layer]["placey"], window=self.button_frame, anchor=N+W, tags=self.selected_layer)
                    self.layer_dict[self.selected_layer]["widget"].pack(fill=BOTH, ipady=5, expand=True)
                    self.layer_dict[self.selected_layer]["type"] = "Button"

            elif self.tool_var.get() == "Create List":
                if self.selected_layer not in self.layer_dict:
                    self.x = event.x
                    self.y = event.y
                    self.width = 0
                    self.height = 0

                    self.list_frame = Frame()
                    self.list_frame.pack_propagate(0)
                    self.list_frame.rowconfigure(0, weight=1)
                    self.list_frame.columnconfigure(0, weight=1)
                    self.layer_dict[self.selected_layer] = {}
                    self.layer_dict[self.selected_layer]["widget"] = Listbox(self.list_frame, relief="flat")
                    self.layer_dict[self.selected_layer]["scrollbar"] = CustomScrollbar(self.list_frame, self.layer_dict[self.selected_layer]["widget"], command=self.layer_dict[self.selected_layer]["widget"].yview)
                    self.layer_dict[self.selected_layer]["type"] = "Listbox"
                    if event.x % 10 <= 5:
                        self.layer_dict[self.selected_layer]["placex"] = event.x - event.x % 10
                    else:
                        self.layer_dict[self.selected_layer]["placex"] = event.x + 10 - event.x % 10
                    if event.y % 10 <= 5:
                        self.layer_dict[self.selected_layer]["placey"] = event.y - event.y % 10
                    else:
                        self.layer_dict[self.selected_layer]["placey"] = event.y + 10 - event.y % 10
                    self.layer_dict[self.selected_layer]["frame"] = self.main_canvas.create_window(self.layer_dict[self.selected_layer]["placex"], self.layer_dict[self.selected_layer]["placey"], window=self.list_frame, anchor=N+W, tags=self.selected_layer)
                    self.layer_dict[self.selected_layer]["widget"].pack(fill=BOTH, expand=True, side=LEFT)
                    self.layer_dict[self.selected_layer]["scrollbar"].pack(fill=Y,expand=True)


            elif self.tool_var.get() == "Create Label":
                if self.selected_layer not in self.layer_dict:
                    self.x = event.x
                    self.y = event.y
                    self.width = 0
                    self.height = 0
                    self.text_frame = Frame()
                    self.text_frame.pack_propagate(0)
                    self.text_frame.rowconfigure(0, weight=1)
                    self.text_frame.columnconfigure(0, weight=1)
                    self.layer_dict[self.selected_layer] = {}
                    self.layer_dict[self.selected_layer]["widget"] = Label(self.text_frame, text=self.entry_text_text.get(), bg=self.color_text_bg.cget("bg"), fg=self.color_text_fg.cget("bg"),font=(self.combo_text_font.get(), self.combo_text_font_size.get()))
                    self.layer_dict[self.selected_layer]["type"] = "Label"
                    if event.x % 10 <= 5:
                        self.layer_dict[self.selected_layer]["placex"] = event.x - event.x % 10
                    else:
                        self.layer_dict[self.selected_layer]["placex"] = event.x + 10 - event.x % 10
                    if event.y % 10 <= 5:
                        self.layer_dict[self.selected_layer]["placey"] = event.y - event.y % 10
                    else:
                        self.layer_dict[self.selected_layer]["placey"] = event.y + 10 - event.y % 10
                    self.layer_dict[self.selected_layer]["frame"] = self.main_canvas.create_window(self.layer_dict[self.selected_layer]["placex"], self.layer_dict[self.selected_layer]["placey"], window=self.text_frame, anchor=N+W, tags=self.selected_layer)
                    self.layer_dict[self.selected_layer]["widget"].pack(fill=BOTH, expand=True)
            elif self.tool_var.get() == "Draw":
                self.x = event.x
                self.y = event.y

            elif self.tool_var.get() == "Move":
                self.x = event.x
                self.y = event.y


    def on_motion(self,event):
        if self.selected_layer != "":
            if self.layer_dict[self.selected_layer]["type"] == "Button" and self.tool_var.get()=="Create Button":
                if event.x <= self.main_canvas.winfo_reqwidth() and event.y <= self.main_canvas.winfo_reqheight():
                    if event.x >= self.layer_dict[self.selected_layer]["placex"] and event.y >= self.layer_dict[self.selected_layer]["placey"]:
                        self.main_canvas.itemconfig(self.selected_layer, anchor=N+W)
                        if event.x % 10 <= 5:
                            width = abs((event.x - event.x % 10) - self.layer_dict[self.selected_layer]["placex"])
                        else:
                            width = abs((event.x + 10 - event.x % 10) - self.layer_dict[self.selected_layer]["placex"])
                        if event.y % 10 <= 5:
                            height = abs((event.y - event.y % 10) - self.layer_dict[self.selected_layer]["placey"])
                        else:
                            height = abs((event.y + 10 - event.y % 10) - self.layer_dict[self.selected_layer]["placey"])
                    elif event.x <= self.layer_dict[self.selected_layer]["placex"] and event.y >= self.layer_dict[self.selected_layer]["placey"]:
                        self.main_canvas.itemconfig(self.selected_layer, anchor=N+E)
                        if event.x % 10 <= 5:
                            width = abs((event.x - event.x % 10) - self.layer_dict[self.selected_layer]["placex"])
                        else:
                            width = abs((event.x + 10 - event.x % 10) - self.layer_dict[self.selected_layer]["placex"])
                        if event.y % 10 <= 5:
                            height = abs((event.y - event.y % 10) - self.layer_dict[self.selected_layer]["placey"])
                        else:
                            height = abs((event.y + 10 - event.y % 10) - self.layer_dict[self.selected_layer]["placey"])
                    elif event.x <= self.layer_dict[self.selected_layer]["placex"] and event.y <= self.layer_dict[self.selected_layer]["placey"]:
                        self.main_canvas.itemconfig(self.selected_layer, anchor=S+E)
                        if event.x % 10 <= 5:
                            width = abs((event.x - event.x % 10) - self.layer_dict[self.selected_layer]["placex"])
                        else:
                            width = abs((event.x + 10 - event.x % 10) - self.layer_dict[self.selected_layer]["placex"])
                        if event.y % 10 <= 5:
                            height = abs((event.y - event.y % 10) - self.layer_dict[self.selected_layer]["placey"])
                        else:
                            height = abs((event.y + 10 - event.y % 10) - self.layer_dict[self.selected_layer]["placey"])
                    elif event.x >= self.layer_dict[self.selected_layer]["placex"] and event.y <= self.layer_dict[self.selected_layer]["placey"]:
                        self.main_canvas.itemconfig(self.selected_layer, anchor=S+W)
                        if event.x % 10 <= 5:
                            width = abs((event.x - event.x % 10) - self.layer_dict[self.selected_layer]["placex"])
                        else:
                            width = abs((event.x + 10 - event.x % 10) - self.layer_dict[self.selected_layer]["placex"])
                        if event.y % 10 <= 5:
                            height = abs((event.y - event.y % 10) - self.layer_dict[self.selected_layer]["placey"])
                        else:
                            height = abs((event.y + 10 - event.y % 10) - self.layer_dict[self.selected_layer]["placey"])

                    self.main_canvas.itemconfig(self.layer_dict[self.selected_layer]["frame"],width=width,height=height)
            elif self.layer_dict[self.selected_layer]["type"] == "Listbox" and self.tool_var.get()=="Create List":
                if self.selected_layer in self.layer_dict:
                    if event.x <= self.main_canvas.winfo_reqwidth() and event.y <= self.main_canvas.winfo_reqheight():
                        if event.x >= self.layer_dict[self.selected_layer]["placex"] and event.y >= \
                                self.layer_dict[self.selected_layer]["placey"]:
                            self.main_canvas.itemconfig(self.selected_layer, anchor=N + W)
                            if event.x % 10 <= 5:
                                width = abs((event.x - event.x % 10) - self.layer_dict[self.selected_layer]["placex"])
                            else:
                                width = abs(
                                    (event.x + 10 - event.x % 10) - self.layer_dict[self.selected_layer]["placex"])
                            if event.y % 10 <= 5:
                                height = abs((event.y - event.y % 10) - self.layer_dict[self.selected_layer]["placey"])
                            else:
                                height = abs(
                                    (event.y + 10 - event.y % 10) - self.layer_dict[self.selected_layer]["placey"])
                        elif event.x <= self.layer_dict[self.selected_layer]["placex"] and event.y >= \
                                self.layer_dict[self.selected_layer]["placey"]:
                            self.main_canvas.itemconfig(self.selected_layer, anchor=N + E)
                            if event.x % 10 <= 5:
                                width = abs((event.x - event.x % 10) - self.layer_dict[self.selected_layer]["placex"])
                            else:
                                width = abs(
                                    (event.x + 10 - event.x % 10) - self.layer_dict[self.selected_layer]["placex"])
                            if event.y % 10 <= 5:
                                height = abs((event.y - event.y % 10) - self.layer_dict[self.selected_layer]["placey"])
                            else:
                                height = abs(
                                    (event.y + 10 - event.y % 10) - self.layer_dict[self.selected_layer]["placey"])
                        elif event.x <= self.layer_dict[self.selected_layer]["placex"] and event.y <= \
                                self.layer_dict[self.selected_layer]["placey"]:
                            self.main_canvas.itemconfig(self.selected_layer, anchor=S + E)
                            if event.x % 10 <= 5:
                                width = abs((event.x - event.x % 10) - self.layer_dict[self.selected_layer]["placex"])
                            else:
                                width = abs(
                                    (event.x + 10 - event.x % 10) - self.layer_dict[self.selected_layer]["placex"])
                            if event.y % 10 <= 5:
                                height = abs((event.y - event.y % 10) - self.layer_dict[self.selected_layer]["placey"])
                            else:
                                height = abs(
                                    (event.y + 10 - event.y % 10) - self.layer_dict[self.selected_layer]["placey"])
                        elif event.x >= self.layer_dict[self.selected_layer]["placex"] and event.y <= \
                                self.layer_dict[self.selected_layer]["placey"]:
                            self.main_canvas.itemconfig(self.selected_layer, anchor=S + W)
                            if event.x % 10 <= 5:
                                width = abs((event.x - event.x % 10) - self.layer_dict[self.selected_layer]["placex"])
                            else:
                                width = abs(
                                    (event.x + 10 - event.x % 10) - self.layer_dict[self.selected_layer]["placex"])
                            if event.y % 10 <= 5:
                                height = abs((event.y - event.y % 10) - self.layer_dict[self.selected_layer]["placey"])
                            else:
                                height = abs(
                                    (event.y + 10 - event.y % 10) - self.layer_dict[self.selected_layer]["placey"])
                        self.main_canvas.itemconfig(self.layer_dict[self.selected_layer]["frame"],width=width,height=height)
                        self.layer_dict[self.selected_layer]["scrollbar"].height = height

            elif self.layer_dict[self.selected_layer]["type"] == "Label" and self.tool_var.get()=="Create Label":
                if self.selected_layer in self.layer_dict:
                    if event.x <= self.main_canvas.winfo_reqwidth() and event.y <= self.main_canvas.winfo_reqheight():
                        if event.x >= self.layer_dict[self.selected_layer]["placex"] and event.y >= \
                                self.layer_dict[self.selected_layer]["placey"]:
                            self.main_canvas.itemconfig(self.selected_layer, anchor=N + W)
                            if event.x % 10 <= 5:
                                width = abs((event.x - event.x % 10) - self.layer_dict[self.selected_layer]["placex"])
                            else:
                                width = abs(
                                    (event.x + 10 - event.x % 10) - self.layer_dict[self.selected_layer]["placex"])
                            if event.y % 10 <= 5:
                                height = abs((event.y - event.y % 10) - self.layer_dict[self.selected_layer]["placey"])
                            else:
                                height = abs(
                                    (event.y + 10 - event.y % 10) - self.layer_dict[self.selected_layer]["placey"])
                        elif event.x <= self.layer_dict[self.selected_layer]["placex"] and event.y >= \
                                self.layer_dict[self.selected_layer]["placey"]:
                            self.main_canvas.itemconfig(self.selected_layer, anchor=N + E)
                            if event.x % 10 <= 5:
                                width = abs((event.x - event.x % 10) - self.layer_dict[self.selected_layer]["placex"])
                            else:
                                width = abs(
                                    (event.x + 10 - event.x % 10) - self.layer_dict[self.selected_layer]["placex"])
                            if event.y % 10 <= 5:
                                height = abs((event.y - event.y % 10) - self.layer_dict[self.selected_layer]["placey"])
                            else:
                                height = abs(
                                    (event.y + 10 - event.y % 10) - self.layer_dict[self.selected_layer]["placey"])
                        elif event.x <= self.layer_dict[self.selected_layer]["placex"] and event.y <= \
                                self.layer_dict[self.selected_layer]["placey"]:
                            self.main_canvas.itemconfig(self.selected_layer, anchor=S + E)
                            if event.x % 10 <= 5:
                                width = abs((event.x - event.x % 10) - self.layer_dict[self.selected_layer]["placex"])
                            else:
                                width = abs(
                                    (event.x + 10 - event.x % 10) - self.layer_dict[self.selected_layer]["placex"])
                            if event.y % 10 <= 5:
                                height = abs((event.y - event.y % 10) - self.layer_dict[self.selected_layer]["placey"])
                            else:
                                height = abs(
                                    (event.y + 10 - event.y % 10) - self.layer_dict[self.selected_layer]["placey"])
                        elif event.x >= self.layer_dict[self.selected_layer]["placex"] and event.y <= \
                                self.layer_dict[self.selected_layer]["placey"]:
                            self.main_canvas.itemconfig(self.selected_layer, anchor=S + W)
                            if event.x % 10 <= 5:
                                width = abs((event.x - event.x % 10) - self.layer_dict[self.selected_layer]["placex"])
                            else:
                                width = abs(
                                    (event.x + 10 - event.x % 10) - self.layer_dict[self.selected_layer]["placex"])
                            if event.y % 10 <= 5:
                                height = abs((event.y - event.y % 10) - self.layer_dict[self.selected_layer]["placey"])
                            else:
                                height = abs(
                                    (event.y + 10 - event.y % 10) - self.layer_dict[self.selected_layer]["placey"])

                        self.main_canvas.itemconfig(self.layer_dict[self.selected_layer]["frame"],width=width,height=height)

            elif self.tool_var.get() == "Move":
                    dx = int(event.x - self.x)
                    dy = int(event.y - self.y)
                    if dx >= 5:
                        self.main_canvas.move(self.selected_layer, dx - (dx % 5), 0)
                        self.x = event.x
                    if dx <= -5:
                        self.main_canvas.move(self.selected_layer, dx - (dx % (-5)), 0)
                        self.x = event.x
                    if dy >= 5:
                        self.main_canvas.move(self.selected_layer, 0, dy - (dy % 5))
                        self.y = event.y
                    if dy <= -5:
                        self.main_canvas.move(self.selected_layer, 0, dy - (dy % (-5)))
                        self.y = event.y
                    self.layer_dict[self.selected_layer]["placex"] = self.main_canvas.coords(self.selected_layer)[0]
                    self.layer_dict[self.selected_layer]["placey"] = self.main_canvas.coords(self.selected_layer)[1]

    def off_click(self, *args):
        if self.main_canvas.itemcget(self.selected_layer, "anchor") == "sw":
            self.main_canvas.itemconfig(self.selected_layer, anchor="nw")
            self.main_canvas.move(self.selected_layer, 0, -int((self.main_canvas.itemcget(self.selected_layer, "height"))))
        elif self.main_canvas.itemcget(self.selected_layer, "anchor") == "ne":
            self.main_canvas.itemconfig(self.selected_layer, anchor="nw")
            self.main_canvas.move(self.selected_layer, -int((self.main_canvas.itemcget(self.selected_layer, "width"))),0)
        elif self.main_canvas.itemcget(self.selected_layer, "anchor") == "se":
            self.main_canvas.itemconfig(self.selected_layer, anchor="nw")
            self.main_canvas.move(self.selected_layer, -int((self.main_canvas.itemcget(self.selected_layer, "width"))),-int((self.main_canvas.itemcget(self.selected_layer, "height"))))
        self.layer_dict[self.selected_layer]["placex"] = self.main_canvas.coords(self.selected_layer)[0]
        self.layer_dict[self.selected_layer]["placey"] = self.main_canvas.coords(self.selected_layer)[1]

    def export(self):
        width = str(self.main_canvas.winfo_reqwidth())
        height = str(self.main_canvas.winfo_reqheight())

        start = """
from Tkinter import *
from BetterScrollbar import CustomScrollbar
import encoded_icon_list
from PIL import Image as PImage
from PIL import ImageTk
import base64
import io
root=Tk()
imagedb = {}
root.title("%s")
root.iconbitmap("%s")
root.resizable(False, False)
root.geometry("%sx%s")
file = open("random_sentence.txt")
lines = file.readlines()\n""" % (self.name,self.icon, width, height)
        content =""
        for layer in self.layer_dict:
            # if layer["type"] == "Label":
            widget_code_temp = "%s = %s(frame_%s," % (layer, self.layer_dict[layer]["type"], layer)
            for item in self.layer_dict[layer]["widget"].keys():
                if item != "image":
                    widget_code_temp += "%s='%s'," % (item, self.layer_dict[layer]["widget"].cget(item))
            if "icon" in self.layer_dict[layer]:
                content += """image_code = base64.b64decode(encoded_icon_list.icon_list[%s])
image_buf = io.BytesIO(image_code)
img = PImage.open(image_buf)
imagedb["%s"] = ImageTk.PhotoImage(img)\n""" % (self.layer_dict[layer]["icon"], self.layer_dict[layer]["icon"])
                widget_code_temp += "image=imagedb['%s']," % self.layer_dict[layer]["icon"]
            widget_code = widget_code_temp[:-1]+")\n"
            widget_x = self.main_canvas.coords(layer)[0]
            widget_y = self.main_canvas.coords(layer)[1]
            widget_width = "width="+str(self.main_canvas.itemcget(layer,"width"))
            widget_height = "height="+str(self.main_canvas.itemcget(layer,"height"))
            content += "\t#%s\n" % layer
            content += "frame_%s = Frame(root,%s,%s)\n" % (layer,widget_height,widget_width)
            content += "frame_%s.pack_propagate(0)\n"%(layer)
            content += widget_code

            if "scrollbar" in self.layer_dict[layer]:
                content += "%s.pack(fill=BOTH, side=LEFT, expand=True)\n" % layer
                content += "%s_scroll = CustomScrollbar(frame_%s, %s, widget_or_frame=1, command=%s.yview)\n" % (layer, layer, layer,layer)
                content += "%s_scroll.pack(fill=X, expand=True, anchor='w')\n" % (layer)
                content += "%s.config(yscrollcommand=%s_scroll.set)\n" % (layer,layer)
            else:
                content += "%s.pack(fill=BOTH,expand=True)\n" % layer
            content += "frame_%s.place(x=%s,y=%s,anchor=N+W)\n" % (layer, widget_x, widget_y)
            content += "\t#---\n\n"
    #
    #         for i in sorted(self.dict_list):
    #
    #             layer = i
    #             if layer != "Background":
    #                 widget_x = self.main_canvas.coords(layer)[0]
    #                 widget_y = self.main_canvas.coords(layer)[1]
    #                 bg = self.dict_list[layer][0].cget("bg")
    #                 fg = self.dict_list[layer][0].cget("fg")
    #                 relief = "flat"
    #                 widget_width = "width="+str(self.main_canvas.itemcget(layer,"width"))
    #                 widget_height = "height="+str(self.main_canvas.itemcget(layer,"height"))
    #                 content += "\t#%s\n" % layer
    #                 content += "frame_%s = Frame(root,%s,%s)\n" % (str(layer),widget_height,widget_width)
    #                 content += "frame_%s.pack_propagate(0)\n"%(str(layer))
    #                 content += "%s = Listbox(frame_%s, bg='%s', fg='%s', relief='%s')\n" % (str(layer),str(layer), bg, fg, relief)
    #                 content += "%s.pack(side=LEFT,fill=BOTH,expand=True)\n" % layer
    #                 content +="for i in lines:\n"
    #                 content +="\t%s.insert(END,i)\n" %(layer)
    #                 content += "%s_scroll = CustomScrollbar(frame_%s, %s, widget_or_frame=1, command=%s.yview)\n" % (layer, layer, layer,layer)
    #                 content += "%s_scroll.pack(fill=X, expand=True, anchor='w')\n" % (layer)
    #                 content += "%s.config(yscrollcommand=%s_scroll.set)\n" % (layer,layer)
    #                 content += "frame_%s.place(x=%s,y=%s,anchor=N+W)\n" % (str(layer), widget_x, widget_y)
    #                 content += "\t#---\n\n"
    #
    #
    #         for i in sorted(self.dict_button):
    #             layer = i
    #             if layer != "Background":
    #                 widget_x = self.main_canvas.coords(layer)[0]
    #                 widget_y = self.main_canvas.coords(layer)[1]
    #                 bg = self.dict_button[layer].cget("bg")
    #                 fg = self.dict_button[layer].cget("fg")
    #                 image = self.dict_button[layer].cget("image")
    #                 relief = self.dict_button[layer].cget("relief")
    #                 text = self.dict_button[layer].cget("text")
    #                 font = self.dict_button[layer].cget("font")
    #                 content += """image_code = base64.b64decode(encoded_icon_list.icon_list[%s])
    # image_buf = io.BytesIO(image_code)
    # img = PImage.open(image_buf)
    # imagedb["%s"] = ImageTk.PhotoImage(img)\n""" % (self.dict_icons_to_save[i],i)
    #                 widget_width = "width="+str(self.main_canvas.itemcget(layer,"width"))
    #                 widget_height = "height="+str(self.main_canvas.itemcget(layer,"height"))
    #                 content += "\t#%s\n" % layer
    #                 content += "frame_%s = Frame(root,%s,%s)\n" % (str(layer),widget_height,widget_width)
    #                 content += "frame_%s.pack_propagate(0)\n"%(str(layer))
    #                 content += "%s = Button(frame_%s, compound='left', text='%s', bg='%s', fg='%s', relief='%s', font='%s',image=imagedb['%s'])\n" % (str(layer),str(layer), text, bg, fg, relief, font,i)
    #                 content += "%s.pack(fill=BOTH,expand=True)\n" % layer
    #                 content += "frame_%s.place(x=%s,y=%s,anchor=N+W)\n" % (str(layer), widget_x, widget_y)
    #                 content += "\t#---\n\n"




        filename = "deneme.py"
        file = open(filename, "w")
        file.write(start)
        content += "root.configure(bg='%s')\n" % self.main_canvas.cget("bg")
        file.write(content)
        file.write("root.mainloop()")


root = Tk()
app = GUI(root)
root.mainloop()


