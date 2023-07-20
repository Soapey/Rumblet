from rumblet.classes.zone.Zone import Zone
from rumblet.classes.pet.PetName import PetName
from rumblet.classes.zone.ZoneName import ZoneName

class ZonesList:
    zones = {
        ZoneName.BRAWLEY.value: Zone(
            name=ZoneName.BRAWLEY.value,
            species={
                PetName.DEWLEAF.value: {
                    "portions": 13,
                    "min_level": 4,
                    "max_level": 16
                },
                PetName.AQUALILY.value: {
                    "portions": 1,
                    "min_level": 16,
                    "max_level": 39
                },
            }
        )
    }
    brawley = zones.get(ZoneName.BRAWLEY.value)


if __name__ == "__main__":
    random_pet = ZonesList.brawley.get_random_native_pet()
    print(random_pet.move_names())
