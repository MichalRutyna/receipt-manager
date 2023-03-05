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


class Window(tkinter.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        w, h = master.winfo_screenwidth(), master.winfo_screenheight()

        self.overrideredirect(True)
        self.geometry(f'{int(w/2)}x{int(h/2)}+100+100')
        self.config(background='#121212')
        self.title("Budget manager")
        self.iconbitmap(default="resources/icon.ico")
        self.ikona = ImageTk.PhotoImage(Image.open('resources/icon.png').resize((17, 17)))
        self.update()

        # toplevel follows root taskbar events (minimize, restore)
        master.bind("<Unmap>", self.onRootIconify)
        master.bind("<Map>", self.onRootDeiconify)
        master.bind("<FocusIn>", self.onRootLift)

    def onRootIconify(self, event):
        for child in self.master.winfo_children():
            child.withdraw()

    def onRootDeiconify(self, event):
        for child in self.master.winfo_children():
            child.deiconify()

    def onRootLift(self, event):
        for child in self.master.winfo_children():
            child.lift()

    def resize(self, event):
        w = event.width - self.winfo_width()
        h = event.height - self.winfo_height()
        self.geometry(f"{w}x{h}")

    def malize(self):
        if self.wm_state() == 'zoomed':
            self.state('normal')
        else:
            self.state('zoomed')


class Title_bar(tkinter.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.startY = None
        self.startX = None
        self['bg'] = 'black'
        self['height'] = 30

        self.bind('<Button-1>', self.drag_start)
        self.bind('<B1-Motion>', self.drag_motion)

    def drag_start(self, event):
        self.startX = self.master.winfo_x() - event.x_root
        self.startY = self.master.winfo_y() - event.y_root

    def drag_motion(self, event):
        x = event.x_root + self.startX
        y = event.y_root + self.startY
        self.master.geometry(f'+{x}+{y}')


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
