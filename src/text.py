import xml.etree.ElementTree as ET

from .modfile import Modfile

class TextXml:
    def __init__(self, religions):
        self.religions = religions

    def build(self, path):
        gamedata = ET.Element("GameData")
        language = ET.SubElement(gamedata, "Language_en_US")
        for religion in self.religions:
            language.extend(religion.to_xml())

        tree = ET.ElementTree(gamedata)
        ET.indent(tree, space = "    ")

        tree.write(path)
        return Modfile(path)
