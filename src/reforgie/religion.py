from pathlib import Path
import xml.etree.ElementTree as ET
import tomli

from .icon import Icon

MOD_DIR = Path("./mods/religions/")

class Religion:
    def __init__(self, index, name):
        with open(MOD_DIR / (name + ".toml"), mode="rb") as fp:
            religion_raw = tomli.load(fp)
        self._short = name
        self.index = index

        self.key = self._short.replace("-", "_").upper()

        self.name = religion_raw["name"]
        self.adj = religion_raw["adj"]
        self.pedia = religion_raw["pedia"]
        self.icon = Icon(index, self.icon_path())

    def icon_path(self):
        return MOD_DIR / (self._short + ".png")

    def to_xml(self):
        return (
            row(self.name, f"TXT_KEY_RELIGION_{self.key}"),
            row(self.adj, f"TXT_KEY_RELIGION_{self.key}_ADJ"),
            row(self.pedia, f"TXT_KEY_RELIGION_{self.key}_PEDIA"),
        )


def row(text, key):
    row = ET.Element("Row", attrib={"Tag": key})
    entry = ET.SubElement(row, "Text")
    entry.text = text
    return row
