from PIL import Image

ATLAS_COLS = 8
ICON_SIZE = 256

class Atlas:
    def __init__(self, religions):

        self.religions = religions

        self.cols = min(len(religions) + 1, ATLAS_COLS)
        self.rows = len(religions) // ATLAS_COLS + 1
        self.w = self.cols * ICON_SIZE
        self.h = self.rows * ICON_SIZE
        self.atlas = Image.new("RGBA", (self.w, self.h))

        # 22 is font size
        self.thumbnail_sizes = [16, 24, 32, 48, 64, 80, 128, 214, 256, 22]

    def draw(self):
        for religion in self.religions:
            self.atlas.paste(religion.icon.img(), (religion.icon.w, religion.icon.h))

    def save(self, path):
        self.draw()

        for size in self.thumbnail_sizes:
            thumbnail = self.atlas.resize((self.cols * size, self.rows * size))
            thumbnail.save(path / f"atlas{size}.dds")
