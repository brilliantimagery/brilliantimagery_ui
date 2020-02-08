from pathlib import Path

import numpy as np
from skvideo.io import FFmpegWriter
from PIL import Image


def render():
    folder = Path("E:\\Downloads\\photos")
    files = [folder / f for f in folder.iterdir() if
             (folder / f).is_file() and f.suffix.lower() == '.jpg']

    writer = FFmpegWriter("E:\\Downloads\\photos\\video.mp4",
                          outputdict={
                              '-vcodec': 'libx264',
                              '-r': '24',
                          })
    for file in files:
        pic = Image.open(str(folder / file))
        pic.thumbnail((1920*2, 1080*2), Image.ANTIALIAS)
        pic = np.array(pic).astype(np.uint8)
        writer.writeFrame(pic)
    writer.close()
