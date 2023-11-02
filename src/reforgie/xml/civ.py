from pathlib import Path

from .gamedata import gamedata
from .text import text
from .color import color
from .artstyle import ARTSTYLES
from .leader_scene import leader_scene

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
            "Type":               f"CIVILIZATION_{key}",

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

    gamedata.add(
        "Civilization_Religions",
        {
            "CivilizationType": f"CIVILIZATION_{key}",
            "ReligionType": f"RELIGION_{data['civ']['religion'].replace(' ', '_').upper()}",
        }
    )

    for index, cityname in enumerate(data["civ"]["cities"]):
        gamedata.add(
            "Civilization_CityNames",
            {
                "CivilizationType": f"CIVILIZATION_{key}",
                "CityName": text(f"TXT_KEY_CITY_NAME_{key}_{index}", cityname),
            }
        )

    for index, spyname in enumerate(data["civ"]["spies"]):
        gamedata.add(
            "Civilization_SpyNames",
            {
                "CivilizationType": f"CIVILIZATION_{key}",
                "SpyName": text(f"TXT_KEY_SPY_NAME_{key}_{index}", spyname),
            }
        )
    leader_key = f"""LEADER_{data["leader"]["name"].replace(" ", "_").upper()}"""

    icon_leader = Icon(path / data["art"]["leader"])
    atlas, icon_id = icon_handler.add_icon(icon_leader)

    leaderscene = leader_scene(
        ART_PATH,
        f"""leader_scene_{leader_key.replace(" ", "_").lower()}.xml""",
        to_dds(path / data["art"]["leader_scene"], ART_PATH, f"{key.lower()}_leader_scene.dds"),
    )

    gamedata.add(
        "Leaders",
        {
            "Type":                     leader_key,

            "Description":              text(f"TXT_KEY_{leader_key}",            data["leader"]["name"]),
            "Civilopedia":              text(f"TXT_KEY_{leader_key}_PEDIA_TEXT", data["leader"]["pedia"]),
            # "CivilopediaTag":           ,
            "ArtDefineTag":             leaderscene,

            "VictoryCompetitiveness":   data["leader"]["personality"]["VictoryCompetitiveness"],
            "WonderCompetitiveness":    data["leader"]["personality"]["WonderCompetitiveness"],
            "MinorCivCompetitiveness":  data["leader"]["personality"]["MinorCivCompetitiveness"],
            "Boldness":                 data["leader"]["personality"]["Boldness"],
            "DiploBalance":             data["leader"]["personality"]["DiploBalance"],
            "WarmongerHate":            data["leader"]["personality"]["WarmongerHate"],
            "DenounceWillingness":      data["leader"]["personality"]["DenounceWillingness"],
            "DoFWillingness":           data["leader"]["personality"]["DoFWillingness"],
            "Loyalty":                  data["leader"]["personality"]["Loyalty"],
            "Neediness":                data["leader"]["personality"]["Neediness"],
            "Forgiveness":              data["leader"]["personality"]["Forgiveness"],
            "Chattiness":               data["leader"]["personality"]["Chattiness"],
            "Meanness":                 data["leader"]["personality"]["Meanness"],

            "IconAtlas":                atlas,
            "PortraitIndex":            icon_id,
        }
    )

    gamedata.add(
        "Civilization_Leaders",
        {
            "CivilizationType": f"CIVILIZATION_{key}",
            "LeaderheadType": leader_key,
        }
    )

    for flavor_type, flavor in data["leader"]["flavors"].items():
        gamedata.add(
            "Leader_Flavors",
            {
                "LeaderType": leader_key,
                "FlavorType": f"FLAVOR_{flavor_type.upper()}",
                "Flavor": flavor,
            }
        )

    for bias_type, bias in data["leader"]["biases"]["major"].items():
        gamedata.add(
            "Leader_MajorCivApproachBiases",
            {
                "LeaderType": leader_key,
                "MajorCivApproachType": f"MAJOR_CIV_APPROACH_{bias_type.upper()}",
                "Bias": bias,
            }
        )

    for bias_type, bias in data["leader"]["biases"]["minor"].items():
        gamedata.add(
            "Leader_MinorCivApproachBiases",
            {
                "LeaderType": leader_key,
                "MinorCivApproachType": f"MINOR_CIV_APPROACH_{bias_type.upper()}",
                "Bias": bias,
            }
        )

    gamedata.add(
        "Traits",
        {
            "Type":             f"""TRAIT_{leader_key}""",
            "Description":      text(f"""TXT_KEY_TRAIT_{leader_key}""",       data["leader"]["trait"]),
            "ShortDescription": text(f"""TXT_KEY_TRAIT_{leader_key}_SHORT""", data["leader"]["trait_short"]),
        }
    )

    gamedata.add(
        "Leader_Traits",
        {
            "LeaderType": leader_key,
            "TraitType": f"""TRAIT_{leader_key}""",
        }
    )

    # TODO: genuine unique units
    gamedata.add(
        "Civilization_UnitClassOverrides",
        {
            "CivilizationType": f"CIVILIZATION_{key}",
            "UnitClassType": "UNITCLASS_PIKEMAN",
            "UnitType": "UNIT_ZULU_IMPI",
        }
    )
    gamedata.add(
        "Civilization_UnitClassOverrides",
        {
            "CivilizationType": f"CIVILIZATION_{key}",
            "UnitClassType": "UNITCLASS_MERCHANT",
            "UnitType": "UNIT_VENETIAN_MERCHANT",
        }
    )
