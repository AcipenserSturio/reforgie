from pathlib import Path
import tomli
import shutil

from .religion import religion
from .modinfo import ModinfoXml
from .gamedata import gamedata
from .icons import icon_handler

MOD_DIR = Path("./mods/")
BUILD_DIR = Path("./build/")
shutil.rmtree(BUILD_DIR)

(BUILD_DIR).mkdir(exist_ok=True)
(BUILD_DIR / "art").mkdir(exist_ok=True)
(BUILD_DIR / "core").mkdir(exist_ok=True)

class Mod:
    def __init__(self):
        for index, path in enumerate(sorted((MOD_DIR / "religions").glob("*.toml"))):
            icon_path = MOD_DIR / "religions" / (path.stem + ".png")
            with open(path, mode="rb") as fp:
                religion(index, path, icon_path, tomli.load(fp))

        icon_handler.build(BUILD_DIR / "art") # responsible for adding some gamedata too
        gamedata.build(BUILD_DIR / "core")

        ModinfoXml(BUILD_DIR).build(BUILD_DIR / "reforged_religion_pack.modinfo")
