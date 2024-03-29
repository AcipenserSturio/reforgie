from pathlib import Path

from ..img.icons import icon_handler
from ..img.icon import Icon
from .gamedata import gamedata
from .text import text

def religion(
    index: int,
    path: Path,
    icon_path: Path,
    data: dict,
):
    key = path.stem.replace("-", "_").upper() # e.g. GNOSTICISM
    fonticon_name = f"ICON_RELIGION_{key}"

    icon = Icon(icon_path, fonticon_name)
    atlas_name, icon_id = icon_handler.add_icon(icon)
    icon_handler.add_fonticon(icon)

    name = text(f"TXT_KEY_RELIGION_{key}", data["name"])
    pedia = text(f"TXT_KEY_RELIGION_{key}_PEDIA", data["pedia"])

    gamedata.add(
        "Religions",
        {
            "Type": f"RELIGION_{key}",
            "Description": name,
            "Civilopedia": pedia,
            "IconAtlas": atlas_name,
            "PortraitIndex": icon_id,
            "IconString": f"[{fonticon_name}]",
        }
    )
