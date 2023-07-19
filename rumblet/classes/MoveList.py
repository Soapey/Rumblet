from rumblet.classes.PetTypeChart import PetTypeChart
from rumblet.classes.Move import Move


def splash(using_pet, target_pet):
    move = MoveList.splash
    damage = calculate_damage(move, using_pet, target_pet)
    target_pet.current_health -= damage
    print(f"{using_pet.nickname} used Splash on {target_pet.nickname} dealing {damage} damage!")


class MoveList:
    moves = {
        "Splash": Move(name="Splash", type=PetTypeChart.water, base_damage=10, ability=splash, max_fuel=10)
    }
    splash = moves.get("Splash")


def calculate_damage(move, using_pet, target_pet):
    base_damage = move.base_damage
    attack_multiplier = 1 + (using_pet.current_attack / 100)
    attack_desired_damage = base_damage * attack_multiplier

    defense_multiplier = 1 - (target_pet.current_defense / 100)
    defense_desired_damage = base_damage * defense_multiplier

    type_multiplier = PetTypeChart.get_multiplier(move.type, target_pet.species.type)

    actual_damage = max(int(round(((attack_desired_damage + defense_desired_damage) / 2) * type_multiplier, 0)), 0)

    return actual_damage
