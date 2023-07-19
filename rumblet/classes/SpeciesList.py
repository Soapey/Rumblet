from rumblet.classes.PetTypeChart import PetTypeChart
from rumblet.classes.Species import Species

class SpeciesList:
    species = {
        "Grasschu": Species(
            name="Grasschu",
            sprite_path=None,
            type=PetTypeChart.grass,
            health=70,
            defense=20,
            attack=0,
            speed=100,
            end_health=None,
            end_defense=None,
            end_attack=None,
            end_speed=None,
            leveling_speed=50,
            evolution_name="Grasskachu",
            evolution_level=16
        ),
        "Grasskachu": Species(
            name="Grasskachu",
            sprite_path=None,
            type=PetTypeChart.grass,
            health=250,
            defense=160,
            attack=200,
            speed=300,
            end_health=650,
            end_defense=330,
            end_attack=425,
            end_speed=700,
            leveling_speed=50,
            evolution_name=None,
            evolution_level=None
        )
    }
