from pathlib import Path
from PIL import Image
import xml.etree.ElementTree as ET

from ..xml.gamedata import gamedata
from .atlas import Atlas
from .icon import Icon

FONT_SIZE = 22
DEFAULT_SIZES = [16, 24, 32, 45, 48, 64, 80, 128, 214, 256]

class IconHandler:
    def __init__(self):
        self.atlases = {}
        self.font = Atlas(
            "font_icons",
            "ICON_FONT_TEXTURE_AUTOCOMPOSED_MAIN",
            [FONT_SIZE],
            updates_IconTextureAtlases=False
        )

    def get_atlas(self, name: str):
        if name in self.atlases:
            return self.atlases[name]
        atlas = Atlas(name, f"ATLAS_AUTOCOMPOSED_{name.upper()}", DEFAULT_SIZES)
        self.atlases[name] = atlas
        return atlas

    def add_icon(self, icon: Icon, atlas="main") -> (str, int):
        atlas = self.get_atlas(atlas)
        return (atlas.key, atlas.add(icon))

    def add_fonticon(self, icon: Icon):
        self.font.add(icon)

    def build(self, directory: Path):
        for atlas in self.atlases.values():
            atlas.build(directory)
        self.font.build(directory)
        self.update_iconfonts()
        self.ggxml(directory / "font_icons.ggxml")

    def update_iconfonts(self):
        if not self.font.icons:
            return

        filename = self.font.filename(FONT_SIZE).replace(".dds", "")
        gamedata.add(
            "IconFontTextures",
            {
                "IconFontTexture": self.font.key,
                "IconFontTextureFile": filename,
            }
        )

        for index, icon in enumerate(self.font.icons):
            gamedata.add(
                "IconFontMapping",
                {
                    "IconName": icon.key,
                    "IconFontTexture": self.font.key,
                    "IconMapping": index,
                }
            )

    def ggxml(self, path: Path):
        if not self.font.icons:
            return

        glyphgen = ET.Element("glyphgen")

        glyphgen.append(ET.fromstring(f"""
            <textures width="{self.font.cols * FONT_SIZE}" height="{self.font.rows * FONT_SIZE}">
                <texture name="" src="{self.font.filename(FONT_SIZE)}" allowcolor="1" alloweffects="1" inuse="1" />
            </textures>
        """))
        glyphgen.append(ET.fromstring("""
            <styles count="1">
                <style name="">
                    <layers count="1">
                        <layer tex="" />
                    </layers>
                </style>
            </styles>
        """))

        glyphs = ET.SubElement(
            glyphgen,
            "glyphs",
            {
                "fudgeadv": "0",
                "ascadj": "-6",
                "spacing": "0",
                "count": "16",
                "height": "0",
                "ascent": "0",
                "descent": "0",
            }
        )
        for index, icon in enumerate(self.font.icons):
            col, row, w, h = self.font.get_position(icon)
            ET.SubElement(
                glyphs,
                "glyph",
                {
                    "ch": str(index),
                    "u": str(col * FONT_SIZE),
                    "v": str(row * FONT_SIZE),
                    "width": "22",
                    "height": "22",
                    "a": "0",
                    "b": "22",
                    "c": "0",
                    "originx": "0",
                    "originy": "22",
                }
            )

        imports = ET.SubElement(glyphgen, "imports")
        toolonly = glyphgen.append(ET.fromstring("""
            <toolonly>
                <metainfo pt="0.000000" width="256" height="256" alphabias="64" maxsize="256" bestfit="0" pow2="1" freetype="2" fontsrc="" />
                <glyphsets>
                    <set name="GlyphSetAscii" />
                </glyphsets>
            </toolonly>
        """))

        tree = ET.ElementTree(glyphgen)
        ET.indent(tree, space = "    ")
        tree.write(path)


icon_handler = IconHandler()
