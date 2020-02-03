# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path
import sys

block_cipher = None

wkdir = Path.cwd()


a = Analysis([str(wkdir / 'brilliantimagery_ui' / 'ui.py')],
             pathex=[str(wkdir)],
             binaries=[],
             datas=[(str(wkdir / 'brilliantimagery_ui' / 'logo.ico'), str(Path('brilliantimagery_ui'))),
                    (str(Path(sys.exec_prefix) / 'Lib' / 'site-packages' / 'brilliantimagery'), 'brilliantimagery/')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='ui',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True ,
          icon=str(wkdir / 'brilliantimagery_ui' / 'logo.ico'))

# pyinstaller -y -F -i "E:/Documents/Python/brilliantimagery_ui/brilliantimagery_ui/logo.ico" --add-data "E:/Documents/Python/brilliantimagery_ui/brilliantimagery_ui/logo.ico";"." --add-data "C:\Users\chadd\AppData\Local\pypoetry\Cache\virtualenvs\brilliantimagery-ui-ks1vM-kE-py3.8\Lib\site-packages\brilliantimagery";"brilliantimagery/"  "E:/Documents/Python/brilliantimagery_ui/brilliantimagery_ui/ui.py"
