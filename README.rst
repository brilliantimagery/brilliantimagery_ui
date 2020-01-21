BrilliantImagery UI
===================

A basic user interface for the `BrilliantImagery <http://brilliantimagery.org>`_ Python package. It can do things such as render images to ensure that they're properly processed by the underlying engine, and smooth lighting and color transitions in DNG image sequences processed with Adobe Lightroom.


Running from Instillation from Source
-------------------------------------
The app is laid out and managed in a way so as to be easily packaged and distributed to humans who don't want to deal with installing Python and using it's tools. As a result, running it from the command line is mildly atypical. In order to do so, from the top level ``/brilliantimagery_ui`` folder, start the poetry shell:

::

$ poetry shell

Change the working directory into the inner ``/brilliantimagery_ui`` folder:

::

$ cd brilliantimagery_ui

Start the BrilliantImagery_UI app:

::

$ python ui.py


Instillation from Source
------------------------

BrilliantImagery_UI relys on `Python 3.8 <https://www.python.org/downloads/>`_ and the `Poetry <https://python-poetry.org/>`_ package and dependency manager. Install them both if you don't already have them.

Clone the `git repo <https://github.com/brilliantimagery/brilliantimagery_ui.git>`_.

From within the top ``/brilliantimagery_ui`` folder, the one that contains the ``pyproject.toml`` file, install BrilliantImagery_UI:

::

$ poetry install

Package Into A Single Executable
--------------------------------

Once BrilliantImagery_UI is installed, open a poetry shell from within the top level ``/brilliantimagery_ui`` folder.

::

$ poetry shell

Now either a custom configuration can by generated with the ``auto-py-to-exe`` tool by running:

::

$ python auto-py-to-exe

... or the standard configuration can be used by running:

::

$ pyinstaller ui.spec

Depending on the method that you use, the output will either be put into a ``/output`` or ``/dist`` folder.
