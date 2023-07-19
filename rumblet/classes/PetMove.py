from rumblet.classes.MoveList import MoveList


class PetMove:
    def __init__(self, id: int, pet_id: int, move_key: str, current_fuel: int, pet=None):
        self.id = id
        self.pet_id = pet_id
        self.move_key = move_key
        self.current_fuel = current_fuel

        self.pet = pet

    def get_pet(self):
        if self.pet:
            return self.pet

    def use(self, target_pet):
        using_pet = self.get_pet()
        move = MoveList.moves[self.move_key].ability
        move(using_pet, target_pet)

