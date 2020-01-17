from tkinter import Tk, Canvas, mainloop, SE, ttk, Label, Entry, Button, filedialog, END, \
    messagebox, Menu, IntVar, StringVar

from PIL import Image
from PIL.ImageTk import PhotoImage

from bi_ui.default_settings import DefaultSettings


class UI:
    box_colors = {'fill': 'red', 'outline': 'red'}
    line_color = 'red'
    corner_radius = 2

    def __init__(self):
        # set up window
        self.root = Tk()
        self.root.geometry('800x500')
        self.root.resizable(width=False, height=False)
        self.root.title('Brilliant Imagery')

        self.canvas = None
        self.img = None
        self.point1 = None
        self.point2 = None
        self.tab_ramp_stabilize = None
        self.tab_renderer = None

        self._make_menu_bar()

        # get default values
        self.default_settings = DefaultSettings()

        # set up tabs
        self.tab_control = ttk.Notebook(self.root)
        self._make_ramper_tab()
        self._make_renderer_tab()

    def _make_menu_bar(self):
        def quite_app():
            self.root.quit()

        def show_about(event=None):
            messagebox.showinfo('About', "I'm working on it!")

        self.menu = Menu(self.root)

        # ------ File Menu ------
        file_menu = Menu(self.menu, tearoff=0)
        file_menu.add_command(label='Open')
        file_menu.add_command(label='Save',
                              accelerator='Ctrl+S',
                            command=lambda: print('Not Saved'))
        file_menu.add_separator()
        file_menu.add_command(label='Quit', command=quite_app)
        self.menu.add_cascade(label='File', menu=file_menu)

        # ------ Font Menu ------
        text_font = StringVar()
        text_font.set('Times')

        def change_font(event=None):
            print(f'Font Picked: {text_font.get()}')

        font_menu = Menu(self.menu, tearoff=0)
        font_menu.add_radiobutton(label='Times', variable=text_font, command=change_font)

        font_menu.add_radiobutton(label='Courier', variable=text_font, command=change_font)

        font_menu.add_radiobutton(label='Ariel', variable=text_font, command=change_font)

        # ------ View Menu ------
        view_menu = Menu(self.menu, tearoff=0)

        line_numbers = IntVar()
        line_numbers.set(1)

        view_menu.add_checkbutton(label='Show Numbers', variable=line_numbers)
        view_menu.add_cascade(label='Fonts', menu=font_menu)
        self.menu.add_cascade(label='View', menu=view_menu)

        self.root.config(menu=self.menu)


    def _make_renderer_tab(self):
        self.tab_renderer = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_renderer, text='Renderer')
        self.tab_control.pack(expand=1, fill='both')

    def _make_ramper_tab(self):
        self.point1 = ()
        self.point2 = ()

        self.tab_ramp_stabilize = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_ramp_stabilize, text='Ramp & Stabilize')
        self.tab_control.pack(expand=1, fill='both')

        self.canvas = Canvas(self.tab_ramp_stabilize,
                             width=255,
                             height=255
                             )
        self.canvas.grid(row=0, column=0, columnspan=2)

        folder_selecter_row = 1
        folder_sslecter_column = 0
        Label(self.tab_ramp_stabilize, text='Image folder:').grid(row=folder_selecter_row,
                                                                  column=folder_sslecter_column)
        self.folder_entry = Entry(self.tab_ramp_stabilize, width=70)
        self.folder_entry.grid(row=folder_selecter_row, column=folder_sslecter_column+1)
        folder_button = Button(self.tab_ramp_stabilize, text='Folder',
                               command=lambda: self.select_folder(self.folder_entry))
        folder_button.grid(row=folder_selecter_row, column=folder_sslecter_column+2)

        self.canvas.bind('<Button-1>', self.get_point)

    def select_folder(self, entry):
        folder = filedialog.askdirectory(initialdir=self.default_settings.get('open_folder_dialog'),
                                         title='Select A Sequence Folder')
        self.set_text(entry, folder)

    def set_text(self, entry, text):
        entry.delete(0, END)
        entry.insert(0, text)
        return

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


if __name__ == '__main__':
    ui = UI()
    ui.draw_image()

    mainloop()
