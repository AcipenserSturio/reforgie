from .gamedata import gamedata

def text(key: str, value: str) -> str:
    gamedata.add(
        "Languages_en_US",
        {"Value": value},
        {"Tag": key},
    )
    return key
