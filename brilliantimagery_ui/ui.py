import json
import multiprocessing
import os
from pathlib import Path
import sys
import time
from tkinter import Tk, Canvas, SE, ttk, Label, Entry, Button, filedialog, END, \
    messagebox, Menu, IntVar, Scrollbar, Checkbutton, W, LabelFrame, NW, HORIZONTAL, \
    VERTICAL, Frame, LEFT, BOTH, Y, RIGHT, BOTTOM, X, TOP

import brilliantimagery
from brilliantimagery.dng import DNG
from brilliantimagery.sequence import Sequence
import numpy as np
import PIL
from PIL import Image
from PIL.ImageTk import PhotoImage


# from brilliantimagery_ui import ui_utils

# from brilliantimagery_ui.default_settings import DefaultSettings


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = Path(sys._MEIPASS)
    except Exception:
        base_path = Path('.')

    return base_path / relative_path


class UI:
    box_colors = {'fill': 'red', 'outline': 'red'}
    line_color = 'red'
    corner_radius = 2

    def __init__(self, root):
        # toolbar stuff
        # https://www.youtube.com/watch?v=AYOs78NjYfc

        # set up window
        self.root = root
        self.root.geometry('650x400')
        # self.root.resizable(width=False, height=False)
        self.root.title('BrilliantImagery')
        # self.root.iconbitmap(resource_path("") / 'logo.ico')

        self.sequence = None

        self.canvas = None
        self.image = None
        self.point1 = None
        self.point2 = None
        self.files_last_parsed = None
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
        file_menu.add_command(label='Open Project',
                              accelerator='Ctrl+O',
                              command=self._open_project)
        file_menu.add_command(label='Save Project',
                              accelerator='Ctrl+S',
                              command=self._save_project)
        file_menu.add_separator()
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
        self.canvas.grid(row=0, column=0, columnspan=2, rowspan=4)
        self.canvas.bind('<Button-1>', self._draw_image)

        # make function checkboxes
        procedures_frame = LabelFrame(tab_ramp_stabilize, text='Operations To Perform')
        procedures_frame.grid(row=0, column=2, padx=5, pady=5, sticky=NW)
        self.ramp = IntVar()
        self.ramp_checkbutton = Checkbutton(procedures_frame, text="Ramp Linear Properties",
                                            variable=self.ramp)
        self.ramp_checkbutton.grid(row=0, column=0, sticky=W)
        self.exp = IntVar()
        self.exp_checkbutton = Checkbutton(procedures_frame, text="Ramp Exposure",
                                           variable=self.exp)
        self.exp_checkbutton.grid(row=1, column=0, sticky=W)
        self.stab = IntVar()
        self.stab_checkbutton = Checkbutton(procedures_frame, text="Stabilize",
                                            variable=self.stab)
        self.stab_checkbutton.grid(row=2, column=0, sticky=W)

        # Reload and reuse
        reuse_frame = LabelFrame(tab_ramp_stabilize, text='Data Reuse')
        reuse_frame.grid(row=1, column=2, padx=5, pady=5, sticky=NW)
        self.reuse_mis = IntVar()
        self.reuse_mis_checkbutton = Checkbutton(reuse_frame,
                                                 text='Use Previously Calculated Misalignments',
                                                 variable=self.reuse_mis)
        self.reuse_mis_checkbutton.grid(row=0, column=0, sticky=NW)
        self.reuse_bright = IntVar()
        self.reuse_bright_checkbutton = Checkbutton(reuse_frame,
                                                    text='Use Previously Calculated Brightnesses',
                                                    variable=self.reuse_bright)
        self.reuse_bright_checkbutton.grid(row=1, column=0, sticky=NW)

        Button(reuse_frame,
               text='Reload Image',
               command=lambda: self._load_image(self.folder_entry.get())).grid(row=2,
                                                                               column=0,
                                                                               sticky=NW,
                                                                               padx=5,
                                                                               pady=5)

        # set up folder selector
        folder_selector_row = 4
        folder_selector_column = 0
        Label(tab_ramp_stabilize,
              text='Sequence Folder:').grid(row=folder_selector_row,
                                            column=folder_selector_column,
                                            padx=10)
        self.folder_entry = Entry(tab_ramp_stabilize, width=70)
        self.folder_entry.grid(row=folder_selector_row,
                               column=folder_selector_column + 1,
                               columnspan=2)
        self.folder_entry.bind('<FocusOut>', lambda e: self._load_image(self.folder_entry.get()))
        folder_button = Button(tab_ramp_stabilize,
                               text='Folder',
                               command=self._open_sequence)
        folder_button.grid(row=folder_selector_row,
                           column=folder_selector_column + 3,
                           sticky=W, padx=10)

        process_button = Button(tab_ramp_stabilize,
                                text='Process',
                                command=lambda: self._process(msg.get()))
        process_button.grid(row=folder_selector_row + 1, column=0, sticky=W, padx=10, pady=10)

        msg = IntVar()
        Checkbutton(tab_ramp_stabilize,
                    text="Show MessageBox when done.",
                    variable=msg).grid(row=folder_selector_row + 1,
                                       column=1,
                                       sticky=W)

    def _process(self, show_finished):
        if not self._validate_selections():
            return

        if not self.reuse_mis.get() and not self.reuse_bright.get():
            folder = Path(self.folder_entry.get())
            files = [f for f in folder.iterdir() if
                     (folder / f).is_file() and f.suffix.lower() == '.dng']

            if not self.reuse_mis.get():
                self.sequence.set_misalignments({f: None for f in files})

            if not self.reuse_bright.get():
                self.sequence.set_brightnesses({f: None for f in files})

        rectangle = (min(self.point1[0], self.point2[0]), min(self.point1[1], self.point2[1]),
                     max(self.point1[0], self.point2[0]), max(self.point1[1], self.point2[1]))
        rectangle = [rectangle[0] / self.image.width(), rectangle[1] / self.image.height(),
                     rectangle[2] / self.image.width(), rectangle[3] / self.image.height()]

        last_modified = files_last_updated(self.sequence.path)
        if last_modified > self.files_last_parsed:
            self.sequence.parse_sequence()
            self.files_last_parsed = time.time()

        if self.ramp.get() and not self.exp.get() and not self.stab.get():
            self.sequence.ramp_minus_exmpsure()
        elif not self.ramp.get() and self.exp.get() and not self.stab.get():
            self.sequence.ramp_exposure(rectangle)
        elif not self.ramp.get() and not self.exp.get() and self.stab.get():
            self.sequence.stabilize(rectangle)
        elif self.ramp.get() and self.exp.get() and not self.stab.get():
            self.sequence.ramp(rectangle)
        elif not self.ramp.get() and self.exp.get() and self.stab.get():
            self.sequence.ramp_exposure_and_stabilize(rectangle)
        elif self.ramp.get() and not self.exp.get() and self.stab.get():
            self.sequence.ramp_minus_exposure_and_stabilize(rectangle)
        elif self.ramp.get() and self.exp.get() and self.stab.get():
            self.sequence.ramp_and_stabilize(rectangle)

        self.sequence.save()

        self._draw_image()

        if self.exp.get():
            self.reuse_bright_checkbutton.select()
        if self.stab.get():
            self.reuse_mis_checkbutton.select()

        if show_finished:
            messagebox.showinfo('Done', 'All done!')

        print('Done!')

    def _open_sequence(self):
        folder = self._open_folder(self.folder_entry)
        if folder:
            self._load_image(folder)

    def _load_image(self, folder):
        if not Path(folder).is_dir():
            return
        if not self.sequence:
            self.sequence = Sequence(folder)
            self.files_last_parsed = time.time()

        image = self.sequence.get_reference_image(index_order='yxc')

        image = PIL.Image.fromarray(image.astype('uint8'), mode='RGB')
        size = (255, int(255 * image.width / image.height))
        image.thumbnail(size, Image.ANTIALIAS)

        self.image = PhotoImage(image)

        self._draw_image()

    def _open_folder(self, entry):
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
        if not self.image:
            return

        self.canvas.create_image(self.image.width(), self.image.height(),
                                 image=self.image, anchor=SE)

        self._get_point(click)
        if self.point1:
            self._draw_corner(self.point1)
        if self.point2:
            self._draw_corner(self.point2)
            self.canvas.create_rectangle(*self.point1, *self.point2, outline=UI.line_color)

    def _get_point(self, click):
        if not click:
            return
        if not self.point1:
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

    def _save_project(self):
        if self.sequence:
            misalignments = self.sequence.get_misalignments()
            brightnesses = self.sequence.get_brightnesses()
        else:
            misalignments = None
            brightnesses = None
        params = {'point1': self.point1,
                  'point2': self.point2,
                  'ramp': self.ramp.get(),
                  'exposure': self.exp.get(),
                  'stabilize': self.stab.get(),
                  'folder': self.folder_entry.get(),
                  'misalignments': misalignments,
                  'brightnesses': brightnesses,
                  }
        params = json.dumps(params)

        file = filedialog.asksaveasfile(title='Save Project',
                                        mode='w',
                                        defaultextension='.bi',
                                        filetypes=[('BrilliantImagery Project', '.bi'),
                                                   ("All Files", ".*")])
        if not file:
            return

        file.write(params)
        file.close()

    def _open_project(self):
        file = filedialog.askopenfile(title='Open Project',
                                      mode='r',
                                      defaultextension='.bi',
                                      filetypes=[('BrilliantImagery Project', '.bi'),
                                                 ("All Files", ".*")])
        if not file:
            return
        params = file.read()
        file.close()
        params = json.loads(params)

        self.point1 = params.get('point1')
        self.point2 = params.get('point2')

        if params.get('ramp'):
            self.ramp_checkbutton.select()
        else:
            self.ramp_checkbutton.deselect()
        if params.get('exposure'):
            self.exp_checkbutton.select()
        else:
            self.exp_checkbutton.deselect()
        if params.get('stabilize'):
            self.stab_checkbutton.select()
        else:
            self.stab_checkbutton.deselect()

        folder = params.get('folder')
        self._set_text(self.folder_entry, folder)
        self._load_image(folder)

        misalignments = params.get('misalignments')
        brightnesses = params.get('brightnesses')

        if misalignments:
            self.sequence.set_misalignments(misalignments)
            if list(misalignments.values())[0] != None:
                self.reuse_mis_checkbutton.select()
        if brightnesses:
            self.sequence.set_brightnesses(brightnesses)
            if list(brightnesses.values())[0] != None:
                self.reuse_bright_checkbutton.select()

    def _validate_selections(self):
        if self.point1 and self.point2:
            rectangle = True
        else:
            rectangle = False

        ramp = self.ramp.get()
        exp = self.exp.get()
        stab = self.stab.get()

        bright = self.reuse_bright.get()
        mis = self.reuse_mis.get()

        if not self.folder_entry.get():
            messagebox.showerror('Oops!', 'You need to specify a Sequence Folder.')
            return False

        if rectangle and (exp or stab):
            return True
        elif bright and exp:
            return True
        elif mis and stab:
            return True
        elif ramp:
            return True

        messagebox.showerror('Oops!',
                             "You need to specify what to do (in the Operations to Perform box) "
                             "and what information to use (either highlight a rectangle or select "
                             "what info to reuse)")

        return False

        # if not self.point1 or not self.point2 or not self.sequence or not \
        #         (self.ramp.get() or self.exp.get() or self.stab.get()):
        #     messagebox.showerror('Oops!', "You didn't select 2 points, enter an "
        #                                   "image, and select actions to perform")
        #     return False


def files_last_updated(folder):
    folder = Path(folder)
    files = [folder / f for f in folder.iterdir() if
             (folder / f).is_file() and f.suffix.lower() == '.dng']
    return max([os.stat(f).st_mtime for f in files])


if __name__ == '__main__':
    multiprocessing.freeze_support()
    ui = UI(Tk())
    ui.root.mainloop()
