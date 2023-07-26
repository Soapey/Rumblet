from rumblet.classes.game.cell import Cells
from rumblet.classes.pet.SpeciesList import SpeciesList
from rumblet.classes.zone.Zone import Zone
from rumblet.classes.zone.ZoneName import ZoneName


class ZonesList:
    zones = {
        ZoneName.BRAWLEY_UPPER.value: Zone(
            name=ZoneName.BRAWLEY_UPPER.value,
            species={
                SpeciesList.dewleaf.name: {
                    "portions": 13,
                    "min_level": 1,
                    "max_level": 8
                },
                SpeciesList.seedletto.name: {
                    "portions": 13,
                    "min_level": 1,
                    "max_level": 8
                }
            },
            area=[
                Cells.GrassCell(3, 1), Cells.GrassCell(4, 1), Cells.GrassCell(16, 19), Cells.WaterCell(1, 5),
                Cells.WaterCell(2, 5), Cells.WaterCell(1, 6), Cells.WaterCell(2, 6)
            ],
            zone_down_name=ZoneName.BRAWLEY_LOWER.value
        ),
        ZoneName.BRAWLEY_LOWER.value: Zone(
            name=ZoneName.BRAWLEY_LOWER.value,
            species={
                SpeciesList.seedletto.name: {
                    "portions": 13,
                    "min_level": 1,
                    "max_level": 8
                }
            },
            area=[Cells.GrassCell(0, 1), Cells.GrassCell(1, 1), Cells.GrassCell(19, 19)],
            zone_up_name=ZoneName.BRAWLEY_UPPER.value
        ),
    }
    brawley_upper = zones.get(ZoneName.BRAWLEY_UPPER.value)
    brawley_lower = zones.get(ZoneName.BRAWLEY_LOWER.value)
    starting_zone = brawley_lower
