from collections import defaultdict
from pathlib import Path
import xml.etree.ElementTree as ET


# dictionary of table names -> table contents
# table contents are a list of rows, each row is an xml node

class Gamedata:
    def __init__(self):
        self.data = {}

    def add(self, tablename: str, children: dict, attrib: dict = {}):
        table = self.get_table(tablename)
        row = ET.SubElement(table, "Row", attrib=attrib)
        for key, value in children.items():
            child = ET.SubElement(row, key)
            child.text = str(value)

    def add_table(self, tablename: str):
        root = ET.Element("GameData")
        table = ET.SubElement(root, tablename)
        self.data[tablename] = ET.ElementTree(root)

    def get_table(self, tablename: str) -> ET.Element:
        if tablename not in self.data:
            self.add_table(tablename)
        return self.data[tablename].find(tablename)

    def build(self, BUILD_DIR: Path):
        for name, tree in self.data.items():
            ET.indent(tree, space = "    ")
            tree.write(BUILD_DIR / f"{name}.xml", encoding="utf-8", xml_declaration=True)

gamedata = Gamedata()
