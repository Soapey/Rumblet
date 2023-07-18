def splash(target_pet):
    print(f"SPLASHED {target_pet.nickname}")
    target_pet.current_health -= 1


def move_templates():
    return {
        "Splash": {
            "name": "Splash",
            "ability": splash
        }
    }


def read_move_template(key: str):
    return move_templates().get(key)
