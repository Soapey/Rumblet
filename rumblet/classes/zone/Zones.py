from rumblet.classes.game.cell import Cells
from rumblet.classes.pet.SpeciesList import SpeciesList
from rumblet.classes.zone.Zone import Zone
from rumblet.classes.zone.ZoneName import ZoneName


class Zones:
    def __init__(self, game=None):
        self.game = game
        self.list = {
            ZoneName.BRAWLEY_UPPER.value: Zone(
                game=self.game,
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
                    Cells.GrassCell(self.game, 3, 1), Cells.GrassCell(self.game, 4, 1), Cells.GrassCell(self.game, 16, 19), Cells.WaterCell(self.game, 1, 5),
                    Cells.WaterCell(self.game, 2, 5), Cells.WaterCell(self.game, 1, 6), Cells.WaterCell(self.game, 2, 6)
                ],
                zone_down_name=ZoneName.BRAWLEY_LOWER.value
            ),
            ZoneName.BRAWLEY_LOWER.value: Zone(
                game=self.game,
                name=ZoneName.BRAWLEY_LOWER.value,
                species={
                    SpeciesList.seedletto.name: {
                        "portions": 13,
                        "min_level": 1,
                        "max_level": 8
                    }
                },
                area=[Cells.GrassCell(self.game, 0, 1), Cells.GrassCell(self.game, 1, 1), Cells.GrassCell(self.game, 19, 19)],
                zone_up_name=ZoneName.BRAWLEY_UPPER.value
            ),
        }
        self.brawley_upper = self.list.get(ZoneName.BRAWLEY_UPPER.value)
        self.brawley_lower = self.list.get(ZoneName.BRAWLEY_LOWER.value)
        self.starting_zone = self.brawley_lower

    def change_zone(self, direction):
        current_zone = self.list.get(self.game.player.current_zone_name)

        next_zone_name = getattr(current_zone, f"zone_{direction.value.lower()}_name")

        if not next_zone_name:
            return

        self.list.get(next_zone_name).draw()
