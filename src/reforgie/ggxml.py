import xml.etree.ElementTree as ET

FONT_SIZE = 22

class FontIcons:
    def __init__(self, atlas):
        self.atlas = atlas
        self.width = self.atlas.cols * FONT_SIZE
        self.height = self.atlas.rows * FONT_SIZE

    def build(self, path):
        glyphgen = ET.Element("glyphgen")

        glyphgen.append(ET.fromstring(f"""
            <textures width="{self.width}" height="{self.height}">
                <texture name="" src="heathenfonticons.dds" allowcolor="1" alloweffects="1" inuse="1" />
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
        for religion in self.atlas.religions:
            ET.SubElement(
                glyphs,
                "glyph",
                {
                    "ch": str(religion.index),
                    "u": str(religion.icon.col * FONT_SIZE),
                    "v": str(religion.icon.row * FONT_SIZE),
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
        return Modfile(path)
