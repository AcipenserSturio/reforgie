from pathlib import Path

from .icons import icon_handler
from .gamedata import gamedata
from .text import text
from .icon import Icon

def religion(
    index: int,
    path: Path,
    icon_path: Path,
    data: dict,
):
    key = path.stem.replace("-", "_").upper()
    fonticon_name = f"ICON_RELIGION_{key}"

    icon = Icon(icon_path, fonticon_name)
    atlas_name, icon_id = icon_handler.add_icon(icon)
    icon_handler.add_fonticon(icon)

    name = text(f"TXT_KEY_{key}", data["name"])
    adj = text(f"TXT_KEY_{key}_ADJ", data["adj"])
    pedia = text(f"TXT_KEY_{key}_PEDIA", data["pedia"])

    # adj unused? investigate later
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
