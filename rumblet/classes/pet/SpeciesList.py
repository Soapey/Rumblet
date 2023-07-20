from rumblet.classes.pet.PetTypeChart import PetTypeChart
from rumblet.classes.pet.Species import Species
from rumblet.classes.pet.SpeciesName import SpeciesName
from rumblet.classes.move.MoveList import MoveList

class SpeciesList:
    species = {
        SpeciesName.DEWLEAF.value: Species(
            dex_no=1,
            name=SpeciesName.DEWLEAF.value,
            sprite_path=None,
            type=PetTypeChart.water,
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
            evolution_name=SpeciesName.AQUALILY.value,
            evolution_level=16,
            learnable_moves={
                1: MoveList.aquamist_veil.name,
                8: MoveList.hydrostream_rush.name
            }
        ),
        SpeciesName.AQUALILY.value: Species(
            dex_no=2,
            name=SpeciesName.AQUALILY.value,
            sprite_path=None,
            type=PetTypeChart.water,
            health=140,
            defense=40,
            attack=80,
            speed=150,
            end_health=None,
            end_defense=None,
            end_attack=None,
            end_speed=None,
            leveling_speed=40,
            previous_evolution_name=SpeciesName.DEWLEAF.value,
            evolution_name=SpeciesName.TIDALAUREL.value,
            evolution_level=40,
            learnable_moves={}
        ),
        SpeciesName.TIDALAUREL.value: Species(
            dex_no=3,
            name=SpeciesName.TIDALAUREL.value,
            sprite_path=None,
            type=PetTypeChart.water,
            health=210,
            defense=60,
            attack=120,
            speed=250,
            end_health=460,
            end_defense=270,
            end_attack=580,
            end_speed=350,
            leveling_speed=35,
            previous_evolution_name=SpeciesName.AQUALILY.value,
            evolution_name=None,
            evolution_level=None,
            learnable_moves={}
        ),
        SpeciesName.SEEDLETTO.value: Species(
            dex_no=1,
            name=SpeciesName.SEEDLETTO.value,
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
            previous_evolution_name=SpeciesName.SEEDLETTO.value,
            evolution_name=SpeciesName.FLORABUD.value,
            evolution_level=16,
            learnable_moves={}
        ),
        SpeciesName.FLORABUD.value: Species(
            dex_no=2,
            name=SpeciesName.FLORABUD.value,
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
            previous_evolution_name=SpeciesName.SEEDLETTO.value,
            evolution_name=SpeciesName.SYLVAGROVE.value,
            evolution_level=40,
            learnable_moves={}
        ),
        SpeciesName.SYLVAGROVE.value: Species(
            dex_no=3,
            name=SpeciesName.SYLVAGROVE.value,
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
            previous_evolution_name=SpeciesName.FLORABUD.value,
            evolution_name=None,
            evolution_level=None,
            learnable_moves={}
        ),
    }
    dewleaf = species.get(SpeciesName.DEWLEAF.value)
    aqualily = species.get(SpeciesName.AQUALILY.value)
    tidalaurel = species.get(SpeciesName.TIDALAUREL.value)
    seedletto = species.get(SpeciesName.SEEDLETTO.value)
    florabud = species.get(SpeciesName.FLORABUD.value)
    sylvagrove = species.get(SpeciesName.SYLVAGROVE.value)

    @classmethod
    def previous_evolution(cls, current_evolution):
        return cls.species.get(current_evolution.previous_evolution_name)

    @classmethod
    def next_evolution(cls, current_evolution):
        return cls.species.get(current_evolution.evolution_name)
