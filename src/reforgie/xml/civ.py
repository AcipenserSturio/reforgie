from pathlib import Path

from .gamedata import gamedata
from .text import text
from .color import color
from .artstyle import ARTSTYLES

from ..img.icons import icon_handler
from ..img.icon import Icon
from ..img.dds_converter import to_dds

AUTHOR = "ACI" # TODO: include this in the pipeline somehow
ART_PATH = Path("./build/art/")

def civ(
    path: Path,
    data: dict,
):
    # e.g. ACI_PERM_ESTATE. Has to be unique.
    key = f"""{AUTHOR}_{path.stem.replace("-", "_").upper()}"""

    suffix, prefix, artstyle = ARTSTYLES[data["civ"]["artstyle"]]

    icon_civ = Icon(path / data["art"]["civ"])
    icon_alpha = Icon(path / data["art"]["alpha"])

    atlas_civs, icon_id = icon_handler.add_icon(icon_civ, "civs")
    atlas_alpha, _ = icon_handler.add_icon(icon_alpha, "alphas")

    gamedata.add(
        "Civilizations",
        {
            "Type":               f"MINOR_CIV_{key}",

            "Description":        text(f"TXT_KEY_{key}_DESC",       data["civ"]["desc"]),
            "ShortDescription":   text(f"TXT_KEY_{key}_SHORT_DESC", data["civ"]["short_desc"]),
            "Adjective":          text(f"TXT_KEY_{key}_ADJ",        data["civ"]["adj"]),
            "CivilopediaTag":     text(f"TXT_KEY_{key}_PEDIA",      data["civ"]["pedia"]),

            "DefaultPlayerColor": color(data["civ"]["color"], f"PLAYERCOLOR_{key}"),

            "ArtDefineTag":       f"ART_DEF_CIVILIZATION_{data['civ']['artdefine'].upper()}",
            "ArtStyleType":       artstyle,
            "ArtStyleSuffix":     suffix,
            "ArtStylePrefix":     prefix,

            "PortraitIndex":      icon_id,
            "IconAtlas":          atlas_civs,
            "AlphaIconAtlas":     atlas_alpha,

            "DawnOfManQuote":     text(f"TXT_KEY_{key}_DOM",        data["civ"]["dom"]),
            "MapImage":           to_dds(path / data["art"]["map"], ART_PATH, f"{key.lower()}_map.dds"),
            "DawnOfManImage":     to_dds(path / data["art"]["dom"], ART_PATH, f"{key.lower()}_dom.dds"),
        }
    )
