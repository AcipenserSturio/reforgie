from .gamedata import gamedata

def text(key: str, value: str) -> str:
    gamedata.add(
        "Language_en_US",
        {"Text": value.replace("\n", "[NEWLINE]")},
        {"Tag": key},
    )
    return key
