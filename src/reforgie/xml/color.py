from .gamedata import gamedata

def color_hex_to_tuple(value: str) -> tuple:
    return tuple(map(lambda x: x / 255, bytes.fromhex(value)))

def color(colours: str, key: str) -> str:
    for ground, colour in zip(("PRIMARY", "SECONDARY"), colours):
        red, green, blue = color_hex_to_tuple(colour)
        gamedata.add(
            "Colors",
            {
                "Type": f"{key}_{ground}",
                "Red": red,
                "Green": green,
                "Blue": blue,
                "Alpha": 1,
            }
        )
    gamedata.add(
        "PlayerColors",
        {
            "Type": key,
            "PrimaryColor": f"{key}_PRIMARY",
            "SecondaryColor": f"{key}_SECONDARY",
            "TextColor": "COLOR_PLAYER_WHITE_TEXT",
        }
    )
    return key
