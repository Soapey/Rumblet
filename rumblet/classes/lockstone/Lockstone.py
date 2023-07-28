from random import randint

from rumblet.classes.bag.BagItem import BagItem
from rumblet.classes.pet.Pet import MAX_LEVEL
from rumblet.classes.player.PlayerPartyPet import PlayerPartyPet


class Lockstone(BagItem):
    def __init__(
            self,
            name,
            description,
            sprite_path,
            max_quantity,
            base_capture_rate
    ):
        super().__init__(
            name=name,
            description=description,
            sprite_path=sprite_path,
            max_quantity=max_quantity
        )
        self.base_capture_rate = base_capture_rate

    def catch_successful(self, target_pet):
        if target_pet.player_id:
            return False

        level_rate_increase = (0.01 * min(0, (MAX_LEVEL // 2) - target_pet.level)) - (
                0.01 * min(0, target_pet.level - (MAX_LEVEL // 2)))
        status_effect_rate_increase = 0.1 * len(target_pet.status_effects)
        health_rate_increase = 0.5 * ((target_pet.health - target_pet.current_health) / target_pet.health)

        total_rate = self.base_capture_rate + level_rate_increase + status_effect_rate_increase + health_rate_increase

        squished_total_rate = max(0, min(100, total_rate * 100))

        return randint(0, 100) <= squished_total_rate

    def attempt_catch(self, player, target_pet):
        catch_is_successful = self.catch_successful(target_pet)
        if not catch_is_successful:
            print(f"{target_pet.nickname} resisted the Lockstone!")
            return

        target_pet.player_id = player.id
        target_pet.insert()

        next_available_party_slot = player.next_available_party_slot()
        if next_available_party_slot:
            playerpartypet = PlayerPartyPet.get_by_player_id_and_slot_number(player.id, next_available_party_slot)
            playerpartypet.pet_id = target_pet.id
            playerpartypet.update()
            print(f"{player.name} has locked {target_pet.nickname}!", f"{target_pet.nickname} has been added to party slot {next_available_party_slot}.", sep="\n")
        else:
            print(f"{player.name} has locked {target_pet.nickname}!", f"{target_pet.nickname} has been sent to the PC.", sep="\n")

    def use(self, player, target_pet):
        self.attempt_catch(player, target_pet)
