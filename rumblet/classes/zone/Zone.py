import random

from rumblet.classes.pet.Pet import Pet
from rumblet.classes.pet.SpeciesList import SpeciesList


class Zone:
    def __init__(self, name, species, area, zone_up_name=None, zone_down_name=None, zone_left_name=None,
                 zone_right_name=None):
        self.name = name
        self.species = species
        self.area = area
        self.zone_up_name = zone_up_name
        self.zone_down_name = zone_down_name
        self.zone_left_name = zone_left_name
        self.zone_right_name = zone_right_name

    def get_random_native_pet(self, terrains=None):

        if terrains:
            species_names = [
                species_name
                for species_name
                in self.species.keys()
                if any(
                    [
                        (terrain_name in SpeciesList.species.get(species_name).terrains)
                        for terrain_name
                        in terrains
                    ]
                )
            ]
        else:
            species_names = list(self.species.keys())

        if not species_names:
            return None

        portions = [self.species.get(species_name).get("portions") for species_name in species_names]

        species_name = random.choices(species_names, weights=portions)[0]
        min_level = self.species[species_name].get("min_level", 1)
        max_level = self.species[species_name].get("max_level", 1)
        level = random.randint(min_level, max_level)

        temp_pet = Pet(
            obj_id=None,
            player_id=None,
            species_name=species_name,
            level=level,
            experience=0
        )

        learnable_move_names_at_level = list(temp_pet.learnable_moves_at_level().keys())
        if learnable_move_names_at_level:
            number_of_moves = random.randint(1, min(4, len(learnable_move_names_at_level)))

            selected_moves = random.sample(learnable_move_names_at_level, number_of_moves)
            for move_slot, move_name in enumerate(selected_moves, start=1):
                setattr(temp_pet, f"move_{move_slot}_name", move_name)

        return temp_pet
