from pathlib import Path
from PIL import Image

class Icon:
    """
    Specific icon. May be in multiple Atlases.
    """
    def __init__ (self, path: Path, key: str = None):
        self.path = path
        self.key = key
        self.indices = {} # Atlas: int
        # self.indices is needed because
        # the same icon may have a different index in any atlas.

    def img(self):
        return Image.open(self.path)
