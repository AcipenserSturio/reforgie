from pathlib import Path
from PIL import Image

from .icon import Icon
from ..xml.gamedata import gamedata

ATLAS_COLS = 8
ICON_SIZE = 256

class Atlas:
    def __init__(
            self,
            name: str,
            key: str,
            sizes: list,
            updates_IconTextureAtlases: bool = True,
        ):
        self.name = name
        self.key = key
        self.sizes = sizes
        self.updates_IconTextureAtlases = updates_IconTextureAtlases

        self.atlas = None
        self.icons = []

    def add(self, icon: Icon) -> int:
        self.icons.append(icon)
        index = len(self.icons) - 1
        self.set_index(icon, index)
        return index

    def start(self):
        """
        Create Image of appropriate size
        based on number of queued icons.
        Unfortunately, can't be known in advance.
        """
        self.cols = min(len(self.icons), ATLAS_COLS)
        self.rows = len(self.icons) // ATLAS_COLS + 1
        self.width = self.cols * ICON_SIZE
        self.height = self.rows * ICON_SIZE
        self.atlas = Image.new("RGBA", (self.width, self.height))

    def paste(self):
        """
        Paste each icon onto the atlas.
        """
        for index, icon in enumerate(self.icons):
            col, row, w, h = self.get_position(icon)
            self.atlas.paste(icon.img(), (w, h))

    def build(self, directory: Path):
        if not self.icons: # empty atlas
            return

        self.start()
        self.paste()

        for size in self.sizes:
            filename = self.filename(size)
            self.thumbnail(size, directory / filename)

            if self.updates_IconTextureAtlases:
                gamedata.add(
                    "IconTextureAtlases",
                    {
                        # placeholder name obviously
                        "Atlas": self.key,
                        "IconSize": size,
                        "Filename": filename,
                        "IconsPerRow": self.cols,
                        "IconsPerColumn": self.rows,
                    }
                )

    def filename(self, size: int):
        return f"{self.name}_{size}.dds"

    def thumbnail(self, size: int, path: Path):
        return self.atlas.resize((self.cols * size, self.rows * size)).save(path)

    def set_index(self, icon: Icon, index: int):
        icon.indices[self] = index

    def get_position(self, icon: Icon) -> tuple:
        index = icon.indices[self]
        col = index % ATLAS_COLS
        row = index // ATLAS_COLS
        w = col * ICON_SIZE
        h = row * ICON_SIZE
        return (col, row, w, h)
