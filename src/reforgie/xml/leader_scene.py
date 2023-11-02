from pathlib import Path
import xml.etree.ElementTree as ET

def leader_scene(out_dir, scene_name, image_name):
    root = ET.Element("LeaderScene", attrib={"FallbackImage": image_name})
    tree = ET.ElementTree(root)

    tree.write(
        out_dir / scene_name,
        encoding="utf-8",
        xml_declaration=True,
    )
    return scene_name
