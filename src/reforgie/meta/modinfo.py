import xml.etree.ElementTree as ET
from pathlib import Path
import random

from .modfile import Modfile

BUILD_DIR = Path("./build/")


class ModinfoXml:
    def __init__(self, directory: Path):
        self.directory = directory
        self.modfiles = [Modfile(path) for path in (Path(".") / directory).glob("**/*") if path.is_file()]

    def build(self, path: Path):
        mod = ET.Element("Mod", {"id": self.generate_id(), "version": "1"})

        mod.append(ET.fromstring("""
            <Properties>
                <Name>(Reforged) Religion Pack</Name>
                <Stability>Beta</Stability>
                <Teaser>Very modular pack, adding (1) new religions to the game.</Teaser>
                <Description>Very modular pack, adding (1) new religions to the game.</Description>
                <Authors>AcipenserSturio</Authors>
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

        for modfile in self.modfiles:
            tag = modfile.build_import()
            files.append(tag)

        actions = ET.SubElement(mod, "Actions")
        onmod = ET.SubElement(actions, "OnModActivated")

        for modfile in self.modfiles:
            tag = modfile.build_update()
            if tag is not None: # Unbelievably, ET.Element() is Falsy
                onmod.append(tag)

        tree = ET.ElementTree(mod)
        ET.indent(tree, space = "  ")
        tree.write(path)

    def generate_id(self):
        return "-".join([randhex(8), randhex(4), randhex(4), randhex(4), randhex(12)])


def randhex(length):
    return "".join(random.choice("0123456789abcdef") for _ in range(length))
