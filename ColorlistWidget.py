from Tkinter import *
import colors_list
from BetterScrollbar import CustomScrollbar
from webcolors import rgb_to_hex
class ColorWidget(Frame):
    def __init__(self, parent, color1="black", color2="white", color3="blue", column_number=2, width=30, height=10):
        Frame.__init__(self, parent)
        self.color_1= color1
        self.color_2= color2
        self.color_3= color3
        self.column_number = column_number
        self.width = width

        self.height = height



        ###############################################
        self.columns = {}
        a, b, c = 0, 0, 0
        red = True
        green = False
        blue= False
        for i in range(250):
            self.columns[i] = Listbox(self,height=self.height, cursor="hand2", width=0.1, fg="white", relief="flat", bg=self.color_2,
                                selectbackground=self.color_3, highlightcolor=self.color_3,
                                highlightbackground=self.color_3)
            self.columns[i].grid(row=0, column=i,ipady=0, sticky=N+S)
            self.columns[i].bind("<<ListboxSelect>>", self.choose_color)
            for j in range(len(colors_list.colors)/self.column_number*(i), len(colors_list.colors)/self.column_number*(i+1)):
                self.columns[i].insert(END, colors_list.colors[j])
                self.columns[i].itemconfig(END, bg="#5A0000", fg=colors_list.colors[j])
            #
            # for j in range(0,256,4):
            #     if red:
            #         code = rgb_to_hex((j,b,c))
            #         self.columns[i].insert(END, str(code))
            #         self.columns[i].itemconfig(END, bg=str(code), fg=code)
            #         if j == 255:
            #             b+=4
            #     if b >= 256:
            #         red = False
            #         green = True
            #     if green:
            #         code = rgb_to_hex((a, j, c))
            #         self.columns[i].insert(END, str(code))
            #         self.columns[i].itemconfig(END, bg=str(code), fg=code)
            #         if j == 255:
            #             a+=4







        self.rowconfigure(0, weight=1)


    def xconfigure(self, yscrollcommand=None):
        for i in self.columns:
            self.columns[i].configure(yscrollcommand=yscrollcommand.set, selectmode=SINGLE)


    def winfo_reqheight(self):
        print self.columns[0].winfo_reqheight()
        return self.columns[0].winfo_reqheight()-5



    def choose_color(self, event):
        w = event.widget
        self.selected_color = w.get(w.curselection())
        w.configure(selectforeground=self.selected_color,
                    selectbackground=self.selected_color)

    def yview(self, *args):
        for i in self.columns:
            self.columns[i].yview(*args)