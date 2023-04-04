import xml.etree.ElementTree as ET
import hashlib
from pathlib import Path
import random

BUILD_DIR = Path("./build/")


class ModinfoXml:
    def __init__(self, mod):
        self.mod = mod

    def build(self, path):
        mod = ET.Element("Mod", {"id": self.generate_id(), "version": "1"})

        mod.append(ET.fromstring("""
            <Properties>
                <Name>Grant's Heathen Religions</Name>
                <Stability>Beta</Stability>
                <Teaser>Adds 32 new religions to the game, nearly all heathen and ancient belief systems which have survived in some form to this day.</Teaser>
                <Description>Adds 32 new religions to the game, nearly all heathen and ancient belief systems which have survived in some form to this day. Compatible with Tomatekh's Historical Religions.</Description>
                <Authors>Grant</Authors>
                <HideSetupGame>0</HideSetupGame>
                <AffectsSavedGames>1</AffectsSavedGames>
                <MinCompatibleSaveVersion>0</MinCompatibleSaveVersion>
                <SupportsSinglePlayer>1</SupportsSinglePlayer>
                <SupportsMultiplayer>1</SupportsMultiplayer>
                <SupportsHotSeat>1</SupportsHotSeat>
                <SupportsMac>1</SupportsMac>
                <ReloadAudioSystem>1</ReloadAudioSystem>
                <ReloadLandmarkSystem>1</ReloadLandmarkSystem>
                <ReloadStrategicViewSystem>1</ReloadStrategicViewSystem>
                <ReloadUnitSystem>1</ReloadUnitSystem>
            </Properties>"""
        ))
        ET.SubElement(mod, "Dependencies")
        ET.SubElement(mod, "References")
        ET.SubElement(mod, "Blocks")
        files = ET.SubElement(mod, "Files")
        for size in self.mod.atlas.thumbnail_sizes:
            atlas_path = f"art/atlas{size}.dds"
            filetag = ET.SubElement(files, "File", {"md5": md5(atlas_path), "import": "1"})
            filetag.text = atlas_path

        for filename in [
                "art/heathenfonticons.dds",
                "art/heathenfonticons.ggxml",
                "core/religionscore.sql",
                "core/en_us.xml",
            ]:
            filetag = ET.SubElement(files, "File", {"md5": md5(filename), "import": "1" if "art" in filename else "0"})
            filetag.text = filename

        mod.append(ET.fromstring("""
            <Actions>
                <OnModActivated>
                <UpdateDatabase>core/religionscore.sql</UpdateDatabase>
                <UpdateDatabase>core/en_us.xml</UpdateDatabase>
                </OnModActivated>
            </Actions>
        """))

        tree = ET.ElementTree(mod)
        ET.indent(tree, space = "  ")
        tree.write(path)

    def generate_id(self):
        return "-".join([randhex(8), randhex(4), randhex(4), randhex(4), randhex(12)])


def randhex(length):
    return "".join(random.choice("0123456789abcdef") for _ in range(length))


def md5(filename):
    with open(BUILD_DIR / filename, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()
