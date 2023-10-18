from pathlib import Path
import tomli
import shutil

from .img.icons import icon_handler
from .xml.gamedata import gamedata
from .xml.religion import religion
from .xml.citystate import citystate
from .meta.modinfo import ModinfoXml

MOD_DIR = Path("./mods/")
BUILD_DIR = Path("./build/")

# Make sure /build is removed
(BUILD_DIR).mkdir(exist_ok=True)
shutil.rmtree(BUILD_DIR)

# Make basic structure
(BUILD_DIR).mkdir(exist_ok=True)
(BUILD_DIR / "art").mkdir(exist_ok=True)
(BUILD_DIR / "core").mkdir(exist_ok=True)

class Mod:
    def __init__(self):
        # for index, path in enumerate(sorted((MOD_DIR / "religions").glob("*.toml"))):
        #     icon_path = MOD_DIR / "religions" / (path.stem + ".png")
        #     with open(path, mode="rb") as fp:
        #         religion(index, path, icon_path, tomli.load(fp))

        for path in sorted((MOD_DIR / "citystates").glob("*.toml")):
            with open(path, mode="rb") as fp:
                citystate(path, tomli.load(fp))

        icon_handler.build(BUILD_DIR / "art") # responsible for adding some gamedata too
        gamedata.build(BUILD_DIR / "core")

        ModinfoXml(BUILD_DIR).build(BUILD_DIR / "reforged_religion_pack.modinfo")
