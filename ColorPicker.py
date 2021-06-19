from Tkinter import *
from webcolors import hex_to_rgb
from webcolors import rgb_to_hex

class ColorPicker(Frame):
    def __init__(self, parent,bg="white", detail=16,height=20):
        Frame.__init__(self,parent)
        self.configure(bg=bg)
        self.f1= Frame(self,bg=bg)

        self.color = "Black"
        self.colors = "Black"
        self.width = 0
        x1 = 0
        y1 = 0
        x2 = 2
        y2 = height
        number = 0
        self.container = Canvas(self.f1,width=self.width,height=height, bd=-2, highlightthickness=0)

        self.container.pack(side=LEFT)

        self.preview = Canvas(self.f1, bg="black",width=50,height=height, bd=-2, highlightthickness=0)
        self.preview.pack(side=LEFT,padx=(20,0))
        self.f1.pack(pady=(20,0))
        self.container.bind("<B1-Motion>", self.showit)
        r = 256
        g = 0
        b = 0
        width=0
        while True:
            rgbcolor = (r, g, b)
            hexcolor = rgb_to_hex(rgbcolor)
            self.container.create_rectangle(x1, y1, x2, y2, fill=hexcolor, outline="", tags="a" + str(number))
            self.width+=2
            self.container.configure(width=self.width)
            x1 += 2
            x2 += 2
            self.container.tag_bind("a" + str(number), "<Button-1>", self.showit)

            # 1st part: RED STAYS 256, GREEN INCREASES TO 256, BLUE STAYS 0
            # 2ND PART: RED DECREASES TO 0, GREEN STAYS 256, BLUE STAYS 0
            # 3RD PART: RED STAYS 0, GREEN STAYS 256, BLUE INCREASES TO 256
            # 4RD PART: RED SYAYS 0, GREEN DECREASES TO 0, BLUE STAYS 256
            # 5TH PART: RED INCREASES TO 256, GREEN STAYS 0, BLUE STAYS 256

            if g < 256 and r == 256 and b == 0:
                g += detail
                # => 256, 256, 0
            if r > 0 and g == 256 and b == 0:
                r -= detail
                # => 0, 256, 0
            if r == 0 and g == 256 and b < 256:
                b += detail
                # => 0, 256, 256
            if b == 256 and g > 0 and r == 0:
                g -= detail
                # => 0, 0, 256
            if b == 256 and g == 0 and r < 256:
                r += detail
            if r == 256 and b == 256:
                break
    def showit(self, event):
        id = self.container.find_closest(event.x, event.y)
        self.color = self.container.itemcget(id, "fill")
        self.colors = rgb_to_hex((hex_to_rgb(self.color)[0]-20,hex_to_rgb(self.color)[1]-20,hex_to_rgb(self.color)[2]-20,))
        self.preview.configure(bg = self.color)



