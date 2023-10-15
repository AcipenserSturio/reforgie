from PIL import Image

ATLAS_COLS = 8
ICON_SIZE = 256

class Icon:
    def __init__ (self, index, path):
        self.path = path
        self.col = index % ATLAS_COLS
        self.row = index // ATLAS_COLS
        self.w = self.col * ICON_SIZE
        self.h = self.row * ICON_SIZE

    def img(self):
        return Image.open(self.path)
