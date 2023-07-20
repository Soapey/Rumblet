from rumblet.classes.pet.PetTypeChart import PetTypeChart
from rumblet.classes.pet.Species import Species
from rumblet.classes.pet.PetName import PetName
from rumblet.classes.move.MoveName import MoveName

class SpeciesList:
    species = {
        PetName.DEWLEAF.value: Species(
            dex_no=1,
            name=PetName.DEWLEAF.value,
            sprite_path=None,
            type=PetTypeChart.grass,
            health=70,
            defense=20,
            attack=40,
            speed=50,
            end_health=None,
            end_defense=None,
            end_attack=None,
            end_speed=None,
            leveling_speed=50,
            previous_evolution_name=None,
            evolution_name=PetName.AQUALILY.value,
            evolution_level=16,
            learnable_moves={
                4: MoveName.AQUAMIST_VEIL.value,
                8: MoveName.HYDROSTREAM_RUSH.value
            }
        ),
        PetName.AQUALILY.value: Species(
            dex_no=2,
            name=PetName.AQUALILY.value,
            sprite_path=None,
            type=PetTypeChart.grass,
            health=140,
            defense=40,
            attack=80,
            speed=150,
            end_health=None,
            end_defense=None,
            end_attack=None,
            end_speed=None,
            leveling_speed=40,
            previous_evolution_name=PetName.DEWLEAF.value,
            evolution_name=PetName.TIDALAUREL.value,
            evolution_level=40,
            learnable_moves={}
        ),
        PetName.TIDALAUREL.value: Species(
            dex_no=3,
            name=PetName.TIDALAUREL.value,
            sprite_path=None,
            type=PetTypeChart.grass,
            health=210,
            defense=60,
            attack=120,
            speed=250,
            end_health=460,
            end_defense=270,
            end_attack=580,
            end_speed=350,
            leveling_speed=35,
            previous_evolution_name=PetName.AQUALILY.value,
            evolution_name=None,
            evolution_level=None,
            learnable_moves={}
        ),
    }

    @classmethod
    def previous_evolution(cls, current_evolution):
        return cls.species.get(current_evolution.previous_evolution_name)

    @classmethod
    def next_evolution(cls, current_evolution):
        return cls.species.get(current_evolution.evolution_name)
