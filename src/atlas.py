from PIL import Image

from .modfile import Modfile

ATLAS_COLS = 8
ICON_SIZE = 256
FONT_SIZE = 22

class Atlas:
    def __init__(self, religions):

        self.religions = religions

        self.cols = min(len(religions), ATLAS_COLS)
        self.rows = len(religions) // ATLAS_COLS + 1
        self.w = self.cols * ICON_SIZE
        self.h = self.rows * ICON_SIZE
        self.atlas = Image.new("RGBA", (self.w, self.h))

        # 22 is font size
        self.thumbnail_sizes = [16, 24, 32, 48, 64, 80, 128, 214, 256]

    def draw(self):
        for religion in self.religions:
            self.atlas.paste(religion.icon.img(), (religion.icon.w, religion.icon.h))

    def build(self, directory):
        self.draw()

        files = [
            self.thumbnail(size, directory / f"atlas_{size}.dds")
            for size in self.thumbnail_sizes
        ]
        files.append(
            self.thumbnail(FONT_SIZE, directory / f"font_icons.dds")
        )
        return files

    def thumbnail(self, size, path):
        self.atlas.resize((self.cols * size, self.rows * size)).save(path)
        return Modfile(path)
