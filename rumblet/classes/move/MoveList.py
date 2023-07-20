from rumblet.classes.pet.PetTypeChart import PetTypeChart
from rumblet.classes.move.Move import Move
from rumblet.classes.move.MoveName import MoveName
from rumblet.classes.move.MoveType import MoveType


def aquamist_veil(using_pet, target_pet):
    target_pet.current_defense += 30
    print(f"{using_pet.nickname} used {MoveName.AQUAMIST_VEIL.value} on {target_pet.nickname}. DEFENSE +30!")


def hydrostream_rush(using_pet, target_pet):
    move = MoveList.moves.get(MoveName.HYDROSTREAM_RUSH.value)
    damage = calculate_damage(move, using_pet, target_pet)
    target_pet.current_health -= damage
    print(f"{using_pet.nickname} used {MoveName.HYDROSTREAM_RUSH.value} on {target_pet.nickname}. DEALING {damage} DAMAGE!")


class MoveList:
    moves = {
        MoveName.AQUAMIST_VEIL.value: Move(
            name=MoveName.AQUAMIST_VEIL.value,
            type=PetTypeChart.water,
            base_damage=0,
            ability=aquamist_veil,
            max_fuel=10,
            description="The user releases a fine mist that surrounds itself, creating a veil of moisture. This move "
                        "increases the user's evasiveness and provides partial protection against physical attacks.",
            move_type=MoveType.DEFENSE
        ),
        MoveName.HYDROSTREAM_RUSH.value: Move(
            name=MoveName.HYDROSTREAM_RUSH.value,
            type=PetTypeChart.water,
            base_damage=20,
            ability=hydrostream_rush,
            max_fuel=10,
            description="Building on Aquamist Veil, the user unleashes a forceful stream of water towards the target. "
                        "It deals moderate damage and has a high chance of lowering the opponent's accuracy.",
            move_type=MoveType.ATTACK
        ),
    }
    aquamist_veil = moves.get(MoveName.AQUAMIST_VEIL.value)
    hydrostream_rush = moves.get(MoveName.HYDROSTREAM_RUSH.value)


def calculate_damage(move, using_pet, target_pet):
    base_damage = move.base_damage
    attack_multiplier = 1 + (using_pet.current_attack / 100)
    attack_desired_damage = base_damage * attack_multiplier

    defense_multiplier = 1 - (target_pet.current_defense / 100)
    defense_desired_damage = base_damage * defense_multiplier

    type_multiplier = PetTypeChart.get_multiplier(move.type, target_pet.species.type)

    actual_damage = max(int(round(((attack_desired_damage + defense_desired_damage) / 2) * type_multiplier, 0)), 0)

    return actual_damage
