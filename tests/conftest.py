import os
from pathlib import Path
import shutil

import numpy as np
import pytest
from PySide2.QtCore import QPoint


@pytest.fixture
def path1():
    yield str(Path('/path/to/the/sequence1'))


@pytest.fixture
def path2():
    yield str(Path('/path/to/the/sequence2'))


@pytest.fixture
def dng_folder():
    path = Path('__file__').absolute()
    i = 0
    while path.name != 'brilliantimagery_ui' and i < 5:
        path = path.parent
        i += 1
    yield str(path / 'tests' / 'data' / 'dngs')


@pytest.fixture
def dng_folder_editable(dng_folder, tmpdir):
    for file in Path(dng_folder).iterdir():
        shutil.copy(file, tmpdir / file.name)

    yield str(tmpdir)

    for file in Path(tmpdir).iterdir():
        os.remove(str(file))


@pytest.fixture
def dng_preview():
    yield np.load(str(Path('__file__').absolute().parent / 'tests' / 'data' / 'dng_preview.npy'))


@pytest.fixture
def dng_preview_w_rectangle():
    yield np.load(str(Path('__file__').absolute().parent / 'tests'
                      / 'data' / 'dng_preview_w_rectangle.npy'))


@pytest.fixture
def image_click_locations():
    # the subtracted 2 and 43 are to account for QPoint offsets
    yield QPoint(181-2, 153-43), QPoint(215-2, 173-43)
