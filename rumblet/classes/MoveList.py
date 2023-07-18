from rumblet.classes.PetTypeChart import PetTypeChart
from rumblet.classes.Move import Move


def splash(target_pet):
    print(f"SPLASHED {target_pet.nickname}")
    move = MoveList.splash
    target_pet.current_health -= calculate_damage(move, target_pet)


class MoveList:
    moves = {
        "Splash": Move(name="Splash", type=PetTypeChart.water, base_damage=10, ability=splash)
    }
    splash = moves.get("Splash")

def calculate_damage(move, target_pet):



