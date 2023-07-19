from rumblet.classes.Zone import Zone


class ZonesList:
    zones = {
        "Brawley": Zone(
            name="Brawley",
            species={
                "Grasschu": {
                    "portions": 5,
                    "min_level": 1,
                    "max_level": 8
                },
                "Grasskachu": {
                    "portions": 1,
                    "min_level": 16,
                    "max_level": 18
                },
            }
        )
    }
    brawley = zones.get("Brawley")
