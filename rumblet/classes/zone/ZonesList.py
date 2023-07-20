from rumblet.classes.pet.SpeciesList import SpeciesList
from rumblet.classes.zone.Zone import Zone
from rumblet.classes.zone.ZoneName import ZoneName


class ZonesList:
    zones = {
        ZoneName.BRAWLEY.value: Zone(
            name=ZoneName.BRAWLEY.value,
            species={
                SpeciesList.dewleaf.name: {
                    "portions": 13,
                    "min_level": 1,
                    "max_level": 8
                }
            }
        )
    }
    brawley = zones.get(ZoneName.BRAWLEY.value)
