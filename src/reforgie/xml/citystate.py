from pathlib import Path

from .gamedata import gamedata
from .text import text
from .color import color
from .artstyle import ARTSTYLES

FLAVORS_COMMON = {
    "FLAVOR_EXPANSION": 0,
    "FLAVOR_NUKE": 0,
    "FLAVOR_WONDER": 0,
}

FLAVORS = {
    "Cultured": {
        "FLAVOR_CULTURE": 10,
    },
    "Maritime": {
        "FLAVOR_NAVAL": 8,
        "FLAVOR_GROWTH": 8,
    },
    "Mercantile":  {
        "FLAVOR_GOLD": 10,
    },
    "Militaristic":  {
        "FLAVOR_CITY_DEFENSE": 7,
        "FLAVOR_DEFENSE": 7,
        "FLAVOR_OFFENSE": 7,
        "FLAVOR_MILITARY_TRAINING": 7,
    },
    "Religious":  {
        "FLAVOR_RELIGION": 10,
    },
}

"""

"""

def citystate(
    path: Path,
    data: dict,
):
    key = path.stem.replace("-", "_").upper() # e.g. REJKJAVIK

    name = text(f"TXT_KEY_CITYSTATE_{key}", data["name"])
    adj = text(f"TXT_KEY_CITYSTATE_{key}_ADJ", data["adj"])
    capital = text(f"TXT_KEY_CITYSTATE_CITY_{key}", data["capital"])
    pedia = text(f"TXT_KEY_CITYSTATE_{key}_PEDIA", data["pedia"])

    suffix, prefix, artstyle = ARTSTYLES[data["artstyle"]]

    gamedata.add(
        "MinorCivilizations",
        {
            "Type": f"MINOR_CIV_{key}",
            "Description": name,
            "ShortDescription": name,
            "Adjective": adj,
            "Civilopedia": pedia,
            "DefaultPlayerColor": color(data["color"], f"MINOR_COLOR_{key}"),
            "ArtDefineTag": "ART_DEF_CIVILIZATION_MINOR",
            "ArtStyleType": artstyle,
            "ArtStyleSuffix": suffix,
            "ArtStylePrefix": prefix,
            "MinorCivTrait": f"MINOR_TRAIT_{data['trait'].upper()}",
        }
    )

    gamedata.add(
        "MinorCivilization_CityNames",
        {
            "MinorCivType": f"MINOR_CIV_{key}",
            "CityName": capital,
        }
    )

    for flavor_type, flavor in [*FLAVORS_COMMON.items(),
                                *FLAVORS[data["trait"]].items()]:

        gamedata.add(
            "MinorCivilization_Flavors",
            {
                "MinorCivType": f"MINOR_CIV_{key}",
                "FlavorType": flavor_type,
                "Flavor": flavor,
            }
        )
