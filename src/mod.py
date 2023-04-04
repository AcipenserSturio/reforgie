from pathlib import Path

from .atlas import Atlas
from .font_icons import FontIcons
from .modfile import Modfile
from .modinfo import ModinfoXml
from .religion import Religion
from .religions_sql import ReligionsSql
from .text import TextXml

MOD_DIR = Path("./mods/religions/")
BUILD_DIR = Path("./build/")

(BUILD_DIR).mkdir(exist_ok=True)
(BUILD_DIR / "art").mkdir(exist_ok=True)
(BUILD_DIR / "core").mkdir(exist_ok=True)

class Mod:
    def __init__(self):

        religions = [
            Religion(index, path.stem)
            for index, path in enumerate(sorted(MOD_DIR.glob("*.toml")))
        ]
        files = []

        atlas = Atlas(religions)
        text = TextXml(religions)
        sql = ReligionsSql(religions, atlas)
        font_icons = FontIcons(atlas)

        files.extend((
            *atlas.build(BUILD_DIR / "art"),
            text.build(BUILD_DIR / "core" / "en_us.xml"),
            sql.build(BUILD_DIR / "core" / "religionscore.sql"),
            font_icons.build(BUILD_DIR / "art" / "heathenfonticons.ggxml"),
        ))

        modinfo = ModinfoXml(files)
        modinfo.build(BUILD_DIR / "grant's heathen religions (v 1).modinfo")
