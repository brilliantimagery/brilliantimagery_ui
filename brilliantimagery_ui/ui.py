import multiprocessing
import os
import sys
from tkinter import Tk, Canvas, SE, ttk, Label, Entry, Button, filedialog, END, \
    messagebox, Menu, IntVar, Scrollbar, Checkbutton, W, LabelFrame, NW, HORIZONTAL, \
    VERTICAL, Frame, LEFT, BOTH, Y, RIGHT, BOTTOM, X, TOP

import numpy as np
import PIL
from PIL import Image
from PIL.ImageTk import PhotoImage
import brilliantimagery
from brilliantimagery.dng import DNG
from brilliantimagery.sequence import Sequence

from brilliantimagery_ui.default_settings import DefaultSettings


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class UI:
    box_colors = {'fill': 'red', 'outline': 'red'}
    line_color = 'red'
    corner_radius = 2

    def __init__(self, root):
        # toolbar stuff
        # https://www.youtube.com/watch?v=AYOs78NjYfc

        # set up window
        self.root = root
        self.root.geometry('600x400')
        # self.root.resizable(width=False, height=False)
        self.root.title('Brilliant Imagery')
        # self.root.iconbitmap(Path('.') / 'logo.ico')
        self.root.iconbitmap(os.path.join(resource_path(""), 'logo.ico'))

        self.sequence = None

        self.canvas = None
        self.image = None
        self.point1 = None
        self.point2 = None
        # self.tab_renderer = None

        self._make_menu_bar()

        # get default values
        # self.default_settings = DefaultSettings()

        # set up tabs
        self.tab_control = ttk.Notebook(self.root)
        self._make_ramp_stabilize_tab()
        self._make_renderer_tab()

    def _make_menu_bar(self):
        def quite_app():
            self.root.quit()

        self.menu = Menu(self.root)

        # ------ File Menu ------
        file_menu = Menu(self.menu, tearoff=0)
        # file_menu.add_command(label='Open')
        # file_menu.add_command(label='Save',
        #                       accelerator='Ctrl+S',
        #                       command=lambda: print('Not Saved'))
        # file_menu.add_separator()
        file_menu.add_command(label='Exit', command=quite_app)
        self.menu.add_cascade(label='File', menu=file_menu)

        # ------ Font Menu ------
        # text_font = StringVar()
        # text_font.set('Times')
        #
        # def change_font(event=None):
        #     print(f'Font Picked: {text_font.get()}')
        #
        # font_menu = Menu(self.menu, tearoff=0)
        # font_menu.add_radiobutton(label='Times', variable=text_font, command=change_font)
        #
        # font_menu.add_radiobutton(label='Courier', variable=text_font, command=change_font)
        #
        # font_menu.add_radiobutton(label='Ariel', variable=text_font, command=change_font)
        #
        # # ------ View Menu ------
        # view_menu = Menu(self.menu, tearoff=0)
        #
        # line_numbers = IntVar()
        # line_numbers.set(1)
        #
        # view_menu.add_checkbutton(label='Show Numbers', variable=line_numbers)
        # view_menu.add_cascade(label='Fonts', menu=font_menu)
        # self.menu.add_cascade(label='View', menu=view_menu)

        # --------- Help Menu --------
        help_menu = Menu(self.menu, tearoff=0)
        help_menu.add_command(label='About',
                              command=lambda: messagebox.showinfo('About',
                                                                  f"BrilliantImagery UI\n\n"
                                                                  f"Version: "
                                                                  f"{brilliantimagery.__version__}"
                                                                  f"\nGo to brilliantimagery.org "
                                                                  f"for more info."))
        self.menu.add_cascade(label='Help', menu=help_menu)

        self.root.config(menu=self.menu)

    def _make_renderer_tab(self):
        tab_renderer = ttk.Frame(self.tab_control)
        self.tab_control.add(tab_renderer, text='Renderer')
        self.tab_control.pack(expand=1, fill='both')

        interface_frame = Frame(tab_renderer)
        interface_frame.pack(side=TOP, anchor=W)
        Label(interface_frame, text='Image Path:').grid(row=0, column=0, padx=10, pady=10)
        file_entry = Entry(interface_frame, width=70)
        file_entry.grid(row=0, column=1)
        folder_button = Button(interface_frame, text='File',
                               command=lambda: self._open_image(file_entry))
        folder_button.grid(row=0, column=2, padx=10)

        image_frame = Frame(tab_renderer)
        image_frame.pack(expand=1, fill='both')
        self.renderer_canvas = Canvas(image_frame, width=500, height=350,
                                      scrollregion=(0, 0, 500, 350))
        horizontal_scroll_bar = Scrollbar(image_frame, orient=HORIZONTAL)
        vertical_scroll_bar = Scrollbar(image_frame, orient=VERTICAL)
        horizontal_scroll_bar.pack(side=BOTTOM, fill=X)
        vertical_scroll_bar.pack(side=RIGHT, fill=Y)
        horizontal_scroll_bar.config(command=self.renderer_canvas.xview)
        vertical_scroll_bar.config(command=self.renderer_canvas.yview)

        self.renderer_canvas.pack(side=LEFT, expand=True, fill=BOTH)
        self.renderer_canvas.config(xscrollcommand=horizontal_scroll_bar.set,
                                    yscrollcommand=vertical_scroll_bar.set)

    def _make_ramp_stabilize_tab(self):
        self.point1 = ()
        self.point2 = ()

        # set up tab
        tab_ramp_stabilize = ttk.Frame(self.tab_control)
        self.tab_control.add(tab_ramp_stabilize, text='Ramp & Stabilize')
        self.tab_control.pack(expand=1, fill='both')
        # self.tab_control.grid(row=0, column=0)

        # make image canvas
        self.canvas = Canvas(tab_ramp_stabilize,
                             width=255,
                             height=255
                             )
        self.canvas.grid(row=0, column=0, columnspan=2)
        self.canvas.bind('<Button-1>', self._draw_image)

        # make function stuff
        procedures_frame = LabelFrame(tab_ramp_stabilize, text='Operations To Perform')
        procedures_frame.grid(row=0, column=2, padx=5, pady=5, sticky=NW)
        ramp = IntVar()
        Checkbutton(procedures_frame, text="Ramp Linear Properties",
                    variable=ramp).grid(row=0, column=0, sticky=W)
        exp = IntVar()
        Checkbutton(procedures_frame, text="Ramp Exposure",
                    variable=exp).grid(row=1, column=0, sticky=W)
        stab = IntVar()
        Checkbutton(procedures_frame, text="Stabilize",
                    variable=stab).grid(row=2, column=0, sticky=W)

        # set up folder selector
        folder_selector_row = 2
        folder_sslector_column = 0
        Label(tab_ramp_stabilize,
              text='Image folder:').grid(row=folder_selector_row,
                                         column=folder_sslector_column,
                                         padx=10)
        folder_entry = Entry(tab_ramp_stabilize, width=70)
        folder_entry.grid(row=folder_selector_row,
                          column=folder_sslector_column + 1,
                          columnspan=2)
        folder_button = Button(tab_ramp_stabilize,
                               text='Folder',
                               command=lambda: self._open_sequence(folder_entry))
        folder_button.grid(row=folder_selector_row,
                           column=folder_sslector_column + 3,
                           sticky=W, padx=10)

        process_button = Button(tab_ramp_stabilize,
                                text='Process',
                                command=lambda: self._process(ramp.get(), exp.get(),
                                                              stab.get(), msg.get()))
        process_button.grid(row=folder_selector_row + 1, column=0, sticky=W, padx=10, pady=10)

        msg = IntVar()
        Checkbutton(tab_ramp_stabilize,
                    text="Show MessageBox when done.",
                    variable=msg).grid(row=folder_selector_row + 1,
                                       column=1,
                                       sticky=W)

    def _process(self, ramp, exposure, stabilize, show_finished):
        if not self.point1 or not self.point2 or not self.sequence or not \
                (ramp or exposure or stabilize):
            messagebox.showerror('Oops!', "You didn't select 2 points, enter an "
                                          "image, and select actions to perform")
            return None

        rectangle = (min(self.point1[0], self.point2[0]), min(self.point1[1], self.point2[1]),
                     max(self.point1[0], self.point2[0]), max(self.point1[1], self.point2[1]))
        rectangle = [rectangle[0] / self.image.width(), rectangle[1] / self.image.height(),
                     rectangle[2] / self.image.width(), rectangle[3] / self.image.height()]

        if ramp and not exposure and not stabilize:
            self.sequence.ramp_minus_exmpsure()
        elif not ramp and exposure and not stabilize:
            self.sequence.ramp_exposure(rectangle)
        elif not ramp and not exposure and stabilize:
            self.sequence.stabilize(rectangle)
        elif ramp and exposure and not stabilize:
            self.sequence.ramp(rectangle)
        elif not ramp and exposure and stabilize:
            self.sequence.ramp_exposure_and_stabilize(rectangle)
        elif ramp and not exposure and stabilize:
            self.sequence.ramp_minus_exposure_plus_stabilize(rectangle)
        elif ramp and exposure and stabilize:
            self.sequence.ramp_and_stabilize(rectangle)

        self.sequence.save()

        self._draw_image()

        if show_finished:
            messagebox.showinfo('Done', 'All done!')

    def _open_sequence(self, entry):
        folder = self._open_folder(entry)

        self.sequence = Sequence(folder)
        image = self.sequence.get_reference_image(index_order='yxc')

        image = PIL.Image.fromarray(image.astype('uint8'), mode='RGB')
        size = (255, int(255 * image.width / image.height))
        image.thumbnail(size, Image.ANTIALIAS)

        self.image = PhotoImage(image)

        self._draw_image()

    def _open_folder(self, entry):
        # folder = filedialog.askdirectory(initialdir=self.default_settings.get('open_folder_dialog'),
        #                                  title='Select A Sequence Folder')
        folder = filedialog.askdirectory(title='Select A Sequence Folder')
        if not folder:
            return

        self._set_text(entry, folder)
        return folder

    def _open_image(self, entry):
        file = self._open_file(entry)

        if not file:
            return
        dng = DNG(file)
        image_array = dng.get_image() * 255

        shape = image_array.shape
        image_array = np.reshape(image_array, image_array.size, 'C')
        image_array = np.reshape(image_array, (shape[2], shape[1], shape[0]), 'F')

        image = PIL.Image.fromarray(image_array.astype('uint8'), mode='RGB')

        self.image_rendered = PhotoImage(image)
        self.renderer_canvas.create_image(self.image_rendered.width(),
                                          self.image_rendered.height(),
                                          image=self.image_rendered,
                                          anchor=SE)
        self.renderer_canvas.config(scrollregion=(0, 0, image.width, image.height))

    def _open_file(self, entry):
        # file = filedialog.askopenfilename(
        # initialdir=self.default_settings.get('open_folder_dialog'),
        # title='Select an Image to Render',
        # filetypes=(('dng files', '*.dng'),
        #            ('all files', '*.*')))
        file = filedialog.askopenfilename(
            title='Select an Image to Render',
            filetypes=(('dng files', '*.dng'),
                       ('all files', '*.*')))
        if not file:
            return

        self._set_text(entry, file)
        return file

    def _set_text(self, entry, text):
        entry.delete(0, END)
        entry.insert(0, text)
        return

    def _draw_image(self, click=None):
        self.canvas.create_image(self.image.width(), self.image.height(), image=self.image,
                                 anchor=SE)

        self._get_point(click)
        if self.point1:
            self._draw_corner(self.point1)
        if self.point2:
            self._draw_corner(self.point2)
            self.canvas.create_rectangle(*self.point1, *self.point2, outline=UI.line_color)

    def _get_point(self, click):
        if not click:
            self.point1 = ()
            self.point2 = ()
        elif not self.point1:
            self.point1 = (click.x, click.y)
        elif not self.point2:
            self.point2 = (click.x, click.y)
        else:
            self.point1 = ()
            self.point2 = ()

    def _draw_corner(self, point):
        _point1 = (max(0, point[0] - UI.corner_radius),
                   max(0, point[1] - UI.corner_radius))
        _point2 = (min(self.image.width(), point[0] + UI.corner_radius),
                   min(self.image.height(), point[1] + UI.corner_radius))

        self.canvas.create_rectangle(*_point1, *_point2, **UI.box_colors)


if __name__ == '__main__':
    multiprocessing.freeze_support()
    ui = UI(Tk())
    ui.root.mainloop()
