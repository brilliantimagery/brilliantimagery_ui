import json
import multiprocessing
from pathlib import Path
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

from brilliantimagery_ui.ui_utils import files_last_updated, resource_path
from brilliantimagery_ui.renderer import render


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
        self.root.iconbitmap(resource_path() / 'brilliantimagery_ui' / 'logo.ico')

        self.sequence = None

        self.canvas = None
        self.image = None
        self.point1 = ()
        self.point2 = ()
        self.last_points = ((), ())
        self.files_last_parsed = None

        self._make_menu_bar()

        # set up tabs
        self.tab_control = ttk.Notebook(self.root)
        self._make_ramp_stabilize_tab()
        self._make_video_render_tab()
        self._make_renderer_tab()

    def _make_video_render_tab(self):
        tab_video_renderer = ttk.Frame(self.tab_control)
        self.tab_control.add(tab_video_renderer, text='Video Renderer')
        self.tab_control.pack(expand=1, fill='both')

        self.render_video_button = Button(tab_video_renderer, text='Render Video',
                                          command=render)
        self.render_video_button.pack()

    def _make_renderer_tab(self):
        tab_image_renderer = ttk.Frame(self.tab_control)
        self.tab_control.add(tab_image_renderer, text='Image Renderer')
        self.tab_control.pack(expand=1, fill='both')

        interface_frame = Frame(tab_image_renderer)
        interface_frame.pack(side=TOP, anchor=W)
        Label(interface_frame, text='Image Path:').grid(row=0, column=0, padx=10, pady=10)
        file_entry = Entry(interface_frame, width=70)
        file_entry.grid(row=0, column=1)
        folder_button = Button(interface_frame, text='File',
                               command=lambda: self._open_image(file_entry))
        folder_button.grid(row=0, column=2, padx=10)

        image_frame = Frame(tab_image_renderer)
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
        # set up tab
        tab_ramp_stabilize = ttk.Frame(self.tab_control)
        self.tab_control.add(tab_ramp_stabilize, text='Ramp & Stabilize')
        self.tab_control.pack(expand=1, fill='both')
        # self.tab_control.grid(row=0, column=0)

        # make image canvas
        self.canvas = Canvas(tab_ramp_stabilize, width=255, height=255)
        self.canvas.grid(row=0, column=0, columnspan=2, rowspan=4)
        self.canvas.bind('<Button-1>', self._process_canvas_click)

        # make function checkboxes
        procedures_frame = LabelFrame(tab_ramp_stabilize, text='Operations To Perform')
        procedures_frame.grid(row=0, column=2, padx=5, pady=5, sticky=NW)

        self.ramp = IntVar()
        self.ramp_checkbutton = Checkbutton(procedures_frame, text="Ramp Linear Properties",
                                            variable=self.ramp)
        self.ramp_checkbutton.grid(row=0, column=0, sticky=W)

        self.exposure = IntVar()
        self.exposure_checkbutton = Checkbutton(procedures_frame, text="Ramp Exposure",
                                                variable=self.exposure)
        self.exposure_checkbutton.grid(row=1, column=0, sticky=W)

        self.stabilize = IntVar()
        self.stabilize_checkbutton = Checkbutton(procedures_frame, text="Stabilize",
                                                 variable=self.stabilize)
        self.stabilize_checkbutton.grid(row=2, column=0, sticky=W)

        # Reload and reuse
        reuse_frame = LabelFrame(tab_ramp_stabilize, text='Data Reuse')
        reuse_frame.grid(row=1, column=2, padx=5, pady=5, sticky=NW)
        self.reuse_misalignment = IntVar()
        self.reuse_mis_checkbutton = Checkbutton(reuse_frame,
                                                 text='Use Previously Calculated Misalignments',
                                                 variable=self.reuse_misalignment)
        self.reuse_mis_checkbutton.grid(row=0, column=0, sticky=NW)
        self.reuse_brightness = IntVar()
        self.reuse_bright_checkbutton = Checkbutton(reuse_frame,
                                                    text='Use Previously Calculated Brightnesses',
                                                    variable=self.reuse_brightness)
        self.reuse_bright_checkbutton.grid(row=1, column=0, sticky=NW)

        Button(reuse_frame, text='Reload Image', command=lambda: (self._load_sequence(
            self.folder_entry.get()))).grid(row=2, column=0, sticky=NW, padx=5, pady=5)

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
        self.folder_entry.bind('<FocusOut>', lambda e: self._load_sequence(self.folder_entry.get()))
        folder_button = Button(tab_ramp_stabilize,
                               text='Folder',
                               command=self._open_sequence)
        folder_button.grid(row=folder_selector_row,
                           column=folder_selector_column + 3,
                           sticky=W, padx=10)

        process_button = Button(tab_ramp_stabilize, text='Process',
                                command=lambda: self._process_sequence(message_finished.get()))
        process_button.grid(row=folder_selector_row + 1, column=0, sticky=W, padx=10, pady=10)

        message_finished = IntVar()
        Checkbutton(tab_ramp_stabilize,
                    text="Show MessageBox when done.",
                    variable=message_finished).grid(row=folder_selector_row + 1, column=1, sticky=W)

    def _process_sequence(self, show_finished):
        if not self._validate_selections():
            return

        self._maybe_reset_misalignment_brightness()

        rectangle = (min(self.point1[0], self.point2[0]), min(self.point1[1], self.point2[1]),
                     max(self.point1[0], self.point2[0]), max(self.point1[1], self.point2[1]))
        rectangle = [rectangle[0] / self.image.width(), rectangle[1] / self.image.height(),
                     rectangle[2] / self.image.width(), rectangle[3] / self.image.height()]

        last_modified = files_last_updated(self.sequence.path)
        if last_modified > self.files_last_parsed:
            self.sequence.parse_sequence()
            self.files_last_parsed = time.time()

        if self.ramp.get() and not self.exposure.get() and not self.stabilize.get():
            self.sequence.ramp_minus_exmpsure()
        elif not self.ramp.get() and self.exposure.get() and not self.stabilize.get():
            self.sequence.ramp_exposure(rectangle)
        elif not self.ramp.get() and not self.exposure.get() and self.stabilize.get():
            self.sequence.stabilize(rectangle)
        elif self.ramp.get() and self.exposure.get() and not self.stabilize.get():
            self.sequence.ramp(rectangle)
        elif not self.ramp.get() and self.exposure.get() and self.stabilize.get():
            self.sequence.ramp_exposure_and_stabilize(rectangle)
        elif self.ramp.get() and not self.exposure.get() and self.stabilize.get():
            self.sequence.ramp_minus_exposure_and_stabilize(rectangle)
        elif self.ramp.get() and self.exposure.get() and self.stabilize.get():
            self.sequence.ramp_and_stabilize(rectangle)

        self.sequence.save()

        if self.exposure.get():
            self.reuse_bright_checkbutton.select()
        if self.stabilize.get():
            self.reuse_mis_checkbutton.select()

        self.last_points = (self.point1, self.point2)

        if show_finished:
            messagebox.showinfo('Done', 'All done!')

        print('Done Processing!')

    def _maybe_reset_misalignment_brightness(self):
        folder = Path(self.folder_entry.get())
        files = [f.name for f in folder.iterdir() if
                 (folder / f).is_file() and f.suffix.lower() == '.dng']

        if (self.point1, self.point2) != self.last_points:
            self.sequence.set_misalignments({f: None for f in files})
            self.sequence.set_brightnesses({f: None for f in files})
        else:
            if not self.reuse_misalignment.get():
                self.sequence.set_misalignments({f: None for f in files})
            if not self.reuse_brightness.get():
                self.sequence.set_brightnesses({f: None for f in files})

    def _open_sequence(self):
        folder = self._open_folder(self.folder_entry)
        if folder:
            self._load_sequence(folder)

    def _load_sequence(self, folder):
        if not Path(folder).is_dir():
            return
        if not self.sequence or folder != self.sequence.path:
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
        self.renderer_canvas.create_image(self.image_rendered.width(), self.image_rendered.height(),
                                          image=self.image_rendered, anchor=SE)
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

    def _process_canvas_click(self, click=None):
        if not self.image:
            return
        self._get_point(click)
        self._draw_image()
        if not self.point2:
            self.reuse_mis_checkbutton.deselect()
            self.reuse_bright_checkbutton.deselect()

    def _draw_image(self):
        if not self.image:
            return

        self.canvas.create_image(self.image.width(), self.image.height(),
                                 image=self.image, anchor=SE)

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
                  'exposure': self.exposure.get(),
                  'stabilize': self.stabilize.get(),
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
        self.last_points = (self.point1, self.point2)

        if params.get('ramp'):
            self.ramp_checkbutton.select()
        else:
            self.ramp_checkbutton.deselect()
        if params.get('exposure'):
            self.exposure_checkbutton.select()
        else:
            self.exposure_checkbutton.deselect()
        if params.get('stabilize'):
            self.stabilize_checkbutton.select()
        else:
            self.stabilize_checkbutton.deselect()

        folder = params.get('folder')
        self._set_text(self.folder_entry, folder)
        self._load_sequence(folder)

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

        if not self.folder_entry.get():
            messagebox.showerror('Oops!', 'You need to specify a Sequence Folder.')
            return False

        if rectangle and (self.exposure.get() or self.stabilize.get()):
            return True
        elif self.reuse_brightness.get() and self.exposure.get():
            return True
        elif self.reuse_misalignment.get() and self.stabilize.get():
            return True
        elif self.ramp.get() and not (self.exposure.get() or self.stabilize.get()):
            return True

        messagebox.showerror('Oops!',
                             "You need to specify what to do (in the Operations to Perform box) "
                             "and what information to use (either highlight a rectangle or select "
                             "what info to reuse)")

        return False

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


if __name__ == '__main__':
    multiprocessing.freeze_support()
    ui = UI(Tk())
    ui.root.mainloop()
