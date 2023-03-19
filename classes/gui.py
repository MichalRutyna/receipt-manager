import tkinter
from tkinter import ttk
from PIL import Image, ImageTk
from colormap import rgb2hex


class Root(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("Budget manager")
        self.iconbitmap(default="resources/icon.ico")
        self.attributes('-alpha', 0.0)

        self.bind("<Unmap>", self.childrenIconify)
        self.bind("<Map>", self.childrenDeiconify)
        self.bind("<FocusIn>", self.childrenLift)

    def childrenIconify(self, event):
        for child in self.winfo_children():
            if isinstance(child, Window):
                child.withdraw()

    def childrenDeiconify(self, event):
        for child in self.winfo_children():
            if isinstance(child, Window):
                child.deiconify()

    def childrenLift(self, event):
        for child in self.winfo_children():
            child.lift()


class Window(tkinter.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        w, h = master.winfo_screenwidth(), master.winfo_screenheight()

        self.master = master
        super().overrideredirect(True)
        super().geometry(f'{int(w/2)}x{int(h/2)}+100+100')
        self.config(background='#121212')
        self.title("Budget manager")
        self.iconbitmap(default="resources/icon.ico")
        self.ikona = ImageTk.PhotoImage(Image.open('resources/icon.png').resize((17, 17)))
        self.update()
        self._offsetx = 0
        self._offsety = 0

    def resize(self, event):
        w = event.width - self.winfo_width()
        h = event.height - self.winfo_height()
        self.geometry(f"{w}x{h}")

    def malize(self):
        if self.wm_state() == 'zoomed':
            self.state('normal')
        else:
            self.state('zoomed')

    def dragClick(self, event):
        self._offsetx = super().winfo_pointerx() - super().winfo_rootx()
        self._offsety = super().winfo_pointery() - super().winfo_rooty()

    def drag_motion(self, event):
        x = super().winfo_pointerx() - self._offsetx
        y = super().winfo_pointery() - self._offsety
        super().geometry(f"+{x}+{y}")


class Title_bar(tkinter.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.startY = None
        self.startX = None
        self['bg'] = 'black'
        self['height'] = 30

        self.bind('<Button-1>', self.master.dragClick)
        self.bind('<B1-Motion>', self.master.drag_motion)


class Button(tkinter.Button):
    def __init__(self, master, hover_color, **kwargs):
        super().__init__(master, **kwargs)
        if 'font' not in kwargs:
            self['font'] = 'Inter 10'
        if 'bg' not in kwargs:
            self['bg'] = "#222222"
        if 'borderwidth' not in kwargs:
            self['borderwidth'] = 2
        self.config(fg='gray',
                    activebackground=brighten(hover_color),
                    activeforeground='white',
                    relief='groove')
        self.org_color = self.cget('bg')
        self.hover_color = hover_color
        self.bind('<Enter>', self.enter)
        self.bind('<Leave>', self.leave)

    def enter(self, event):
        self['bg'] = self.hover_color
        self['fg'] = 'white'

    def leave(self, event):
        self['bg'] = self.org_color
        self['fg'] = 'gray'


def brighten(color):
    # color is a hex value
    h = color[1:]
    # hex -> rgb
    R = int(h[0:2], 16)
    G = int(h[2:4], 16)
    B = int(h[4:6], 16)

    # rgb -> hex + whitening
    return rgb2hex(min(int(1.2 * (R + 20)), 255),
                   min(int(1.2 * (G + 20)), 255),
                   min(int(1.2 * (B + 20)), 255))
