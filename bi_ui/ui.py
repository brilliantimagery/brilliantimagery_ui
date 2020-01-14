from tkinter import Tk, Canvas, mainloop, SE, ttk

from PIL import Image
from PIL.ImageTk import PhotoImage


class UI:
    box_colors = {'fill': 'red', 'outline': 'red'}
    line_color = 'red'
    corner_radius = 2

    def __init__(self):
        # set up window
        self.root = Tk()
        self.root.geometry('500x500')
        self.root.title('Brilliant Imagery')

        #set up tabs
        self.tab_control = ttk.Notebook(self.root)

        self.tab_ramp_stabilize = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_ramp_stabilize, text='Ramp & Stabilize')
        self.tab_control.pack(expand=1, fill='both')

        self.tab_renderer = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_renderer, text='Renderer')
        self.tab_control.pack(expand=1, fill='both')

        # set up image canvas
        self.point1 = ()
        self.point2 = ()

        self.img = None
        self.canvas = None

        # img = Image.open('ppm_F-18.ppm')
        # size = (255, int(255 * img.width / img.height))
        # img.thumbnail(size, Image.ANTIALIAS)
        # self.img = PhotoImage(img)
        # self.canvas = Canvas(self.tab_ramp_stabilize,
        #                      width=self.img.width(),
        #                      height=self.img.height()
        #                      )
        self.canvas = Canvas(self.tab_ramp_stabilize,
                             width=255,
                             height=255
                             )
        self.canvas.grid(row=0, column=0)

        self.canvas.bind('<Button-1>', self.get_point)

    def draw_image(self):
        img = Image.open('ppm_F-18.ppm')
        size = (255, int(255 * img.width / img.height))
        img.thumbnail(size, Image.ANTIALIAS)
        self.img = PhotoImage(img)

        self.canvas.create_image(self.img.width(), self.img.height(), image=self.img, anchor=SE)

    def get_point(self, click):
        if not self.point1:
            self.point1 = (click.x, click.y)
        elif not self.point2:
            self.point2 = (click.x, click.y)
        else:
            self.point1 = ()
            self.point2 = ()
            self.draw_image()

        self.draw_square()

    def draw_square(self):
        if self.point1:
            self.draw_corner(self.point1)
        if self.point2:
            self.draw_corner(self.point2)
        if self.point1 and self.point2:
            self.canvas.create_rectangle(*self.point1, *self.point2, outline=UI.line_color)

    def draw_corner(self, point):
        _point1 = (max(0, point[0] - UI.corner_radius),
                   max(0, point[1] - UI.corner_radius))
        _point2 = (min(self.img.width(), point[0] + UI.corner_radius),
                   min(self.img.height(), point[1] + UI.corner_radius))

        self.canvas.create_rectangle(*_point1, *_point2, **UI.box_colors)


ui = UI()
ui.draw_image()

mainloop()
