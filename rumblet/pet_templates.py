from rumblet.classes.PetTypeChart import PetTypeChart

# LEVELING SPEEDS ARE A RANGE FROM 1 TO 100

def pet_templates():
    return {
        "Pichu": {
            "name": "Pichu",
            "sprite": None,
            "type": PetTypeChart.grass,
            "health": 70,
            "defense": 20,
            "attack": 30,
            "speed": 100,
            "end_health": None,
            "end_defense": None,
            "end_attack": None,
            "end_speed": None,
            "leveling_speed": 50,
            "evolution_key": "Pikachu",
            "evolution_level": 16
            },
        "Pikachu": {
            "name": "Pikachu",
            "sprite": None,
            "type": PetTypeChart.grass,
            "health": 250,
            "defense": 160,
            "attack": 200,
            "speed": 300,
            "end_health": 650,
            "end_defense": 330,
            "end_attack": 425,
            "end_speed": 700,
            "leveling_speed": 30,
            "evolution_key": None,
            "evolution_level": None
        }
    }


def read_pet_template(key: str):
    return pet_templates().get(key)
