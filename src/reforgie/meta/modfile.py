import hashlib
import xml.etree.ElementTree as ET
from pathlib import Path


class Modfile:
    def __init__(self, path):
        self.path = path # e.g. "build/core/en_us.xml"

    @property
    def build_path(self):
        # e.g. "core/en_us.xml"
        return str(Path(*self.path.parts[1:]))

    @property
    def file_type(self):
        # e.g. "core" or "art"
        return self.path.parts[1]

    @property
    def md5(self):
        with open(self.path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()

    def build_import(self):
        is_import = "1" if self.file_type == "art" else "0"
        tag = ET.Element("File", {"md5": self.md5, "import": is_import})
        tag.text = self.build_path
        return tag

    def build_update(self):
        if self.file_type == "art":
            return None
        tag = ET.Element("UpdateDatabase")
        tag.text = self.build_path
        return tag
