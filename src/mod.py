from pathlib import Path

from .atlas import Atlas
from .font_icons import FontIcons
from .modinfo import ModinfoXml
from .religion import Religion
from .religions_sql import ReligionsSql
from .text import TextXml

MOD_DIR = Path("./mods/religions/")
BUILD_DIR = Path("./build/")

class Mod:
    def __init__(self):

        self.religions = [
            Religion(index, path.stem)
            for index, path in enumerate(sorted(MOD_DIR.glob("*.toml")))
        ]
        self.atlas = Atlas(self.religions)
        self.text = TextXml(self.religions)
        self.sql = ReligionsSql(self.religions, self.atlas)
        self.font_icons = FontIcons(self.atlas)
        self.modinfo = ModinfoXml(self)

        (BUILD_DIR).mkdir(exist_ok=True)
        (BUILD_DIR / "art").mkdir(exist_ok=True)
        (BUILD_DIR / "core").mkdir(exist_ok=True)

        self.atlas.save(BUILD_DIR / "art")
        self.text.build(BUILD_DIR / "core" / "en_us.xml")
        self.sql.build(BUILD_DIR / "core" / "religionscore.sql")
        self.font_icons.build(BUILD_DIR / "art" / "heathenfonticons.ggxml")
        self.modinfo.build(BUILD_DIR / "grant's heathen religions (v 1).modinfo")
