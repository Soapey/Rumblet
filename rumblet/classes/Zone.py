import random

from rumblet.classes.Pet import Pet


class Zone:
    def __init__(self, name, species):
        self.name = name
        self.species = species

    def get_random_native_pet(self):
        spawn_list = list()
        for species_name in self.species.keys():
            portions = self.species.get(species_name).get("portions")
            spawn_list += [species_name] * portions
        species_name = spawn_list[random.randint(0, len(spawn_list)-1)]
        min_level = self.species.get(species_name).get("min_level") or 1
        max_level = self.species.get(species_name).get("max_level") or 1
        return Pet(
            id=None,
            player_id=None,
            species_name=species_name,
            level=random.randint(min_level, max_level),
            experience=0
        )
