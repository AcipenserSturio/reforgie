from .sql_insert import SqlInsert

class ReligionsSql:
    def __init__(self, religions, atlas):
        self.religions = religions
        self.atlas = atlas

    def build(self, path):
        with open(path, "w") as f:
            f.write("\n\n\n".join((
                self.icon_texture_atlases(),
                self.icon_font_textures(),
                self.icon_font_mapping(),
            )))

    def icon_texture_atlases(self):
        return SqlInsert(
            "IconTextureAtlases",
            {
                "Atlas": "HEATHENS_MASTER_ATLAS",
                "IconSize": lambda size: size,
                "Filename": lambda size: f"atlas{size}.dds",
                "IconsPerRow": self.atlas.cols,
                "IconsPerColumn": self.atlas.rows,
            },
            self.atlas.thumbnail_sizes,
        ).to_str()

    def icon_font_textures(self):
        return SqlInsert(
            "IconFontTextures",
            {
                "IconFontTexture": "ICON_FONT_TEXTURE_HEATHENS_MASTER",
                "IconFontTextureFile": "HeathenFontIcons",
            },
        ).to_str()

    def icon_font_mapping(self):
        return SqlInsert(
            "IconFontMapping",
            {
                "IconName": lambda religion: f"ICON_RELIGION_{religion.key}",
                "IconFontTexture": "ICON_FONT_TEXTURE_HEATHENS_MASTER",
                "IconMapping": lambda religion: religion.index,
            },
            self.religions,
        ).to_str()
