import random

from rumblet.classes.pet.Pet import Pet


class Zone:
    def __init__(self, name, species):
        self.name = name
        self.species = species

    def get_random_native_pet(self):
        species_names = list(self.species.keys())
        portions = [self.species[species_name]["portions"] for species_name in species_names]

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
