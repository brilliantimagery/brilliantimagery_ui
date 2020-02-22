from pathlib import Path

import numpy as np
import skvideo
from skvideo.io import FFmpegWriter
from PIL import Image


def render():
    skvideo.setFFmpegPath('C:\\Program Files\\misc')

    folder = Path("E:\\Downloads\\photos")
    files = [folder / f for f in folder.iterdir() if
             (folder / f).is_file() and f.suffix.lower() == '.jpg']

    writer = FFmpegWriter("E:\\Downloads\\photos\\video.mp4",
    # writer = FFmpegWriter("E:\\Downloads\\photos\\video.webm",
    # writer = FFmpegWriter("E:\\Downloads\\photos\\video.mov",
    #                                  inputdict={
    #                                      '-s': '4951x2785'
    #                                  },
                                     outputdict={
                                         '-vcodec': 'libx264',
                                         '-r': '24',
                                         '-s': '1920x1080',
                                         '-colorspace': 'bt709',
                                         '-pix_fmt': 'yuv420p',
                                         # '-crf': '0',
                                         # '-qp': '0',
                                     })
                                     # outputdict={
                                     #     '-vcodec': 'libx265',
                                     #     '-r': '24',
                                     #     '-s': '1920x1080',
                                     #     '-pix_fmt': 'yuv420p',
                                     #     # '-pix_fmt': 'yuv422p',
                                     #     # '-pix_fmt': 'yuv444p',
                                     #     # '-x265-params': 'lossless=1',
                                     # })
                                     # outputdict={
                                     #     '-vcodec': 'prores_ks',
                                     #     '-s': '1920x1080',
                                     #     '-pix_fmt': 'yuv422p10le',
                                     #     '-profile': '3'
                                     # })
                                     # outputdict={
                                     #     '-vcodec': 'libvpx-vp9',
                                     #     '-s': '1920x1080',
                                     #     '-pix_fmt': 'yuv420p',
                                     #     # '-pix_fmt': 'yuv444p',
                                     #     # '-pix_fmt': 'yuva420p'
                                     #     '-lossless': '1'
                                     # })
    for file in files:
        # pic = Image.open(str(folder / file)).convert('RGB')
        # pic = np.array(pic, dtype=np.uint8)
        # skvideo.io.vread()
        pic = skvideo.io.vread(str(file))
        # writer.writeFrame(str(file))
        writer.writeFrame(pic)
    writer.close()


if __name__ == "__main__":
    render()
