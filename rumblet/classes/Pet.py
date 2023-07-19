from functools import reduce
from rumblet.classes.SpeciesList import SpeciesList
from rumblet.classes.db.SQLiteConnector import SQLiteConnector
from rumblet.classes.PetMove import PetMove
from rumblet.classes.MoveList import MoveList
import random

MAX_LEVEL = 100
LEVEL_1_EXPERIENCE_REQUIRED = 100


class Pet:
    def __init__(
            self,
            id: int, player_id: int, species_name: str, level: int, experience: int, nickname: str = None,
            health: int = None, defense: int = None, attack: int = None, speed: int = None,
            current_health: int = None, current_defense: int = None, current_attack: int = None,
            current_speed: int = None,
            move_1_name: str = None, move_2_name: str = None, move_3_name: str = None, move_4_name: str = None,
            status_effects: list = None
    ):
        self.id = id
        self.player_id = player_id
        self.species = SpeciesList.species.get(species_name)
        self.name = species_name
        self.nickname = nickname or species_name
        self.level: int = level if self.id else 1
        self.experience: int = experience

        self.health = health or self.species.health
        self.defense = defense or self.species.defense
        self.attack = attack or self.species.attack
        self.speed = speed or self.species.speed

        self.current_health = current_health or self.health
        self.current_defense = current_defense or self.defense
        self.current_attack = current_attack or self.attack
        self.current_speed = current_speed or self.speed

        self.move_1_name = move_1_name
        self.move_2_name = move_2_name
        self.move_3_name = move_3_name
        self.move_4_name = move_4_name

        if not status_effects:
            self.status_effects = list()

        if level > 1 and not self.id:
            self.give_level(levels=level-1, provide_summary=False)

    # How the class will appear to players in a string
    def __str__(self):
        return f"{self.name} ({self.level})"

    # How the class will appear to developers in the console
    def __repr__(self):
        attributes_string = ', '.join(f'{k}={v}' for k, v in vars(self).items())
        return f"{self.__class__.__name__}-{self.name}({attributes_string})"

    def level_attribute(self, attribute):
        return self.get_attribute_increase_amount(goal_level=self.level, attribute=attribute)

    def catch_successful(self, lockstone):
        if self.player_id:
            return False

        lockstone_rate = lockstone.base_capture_rate
        level_rate_increase = (0.01 * min(0, (MAX_LEVEL // 2) - self.level)) - (
                    0.01 * min(0, self.level - (MAX_LEVEL // 2)))
        status_effect_rate_increase = 0.1 * len(self.status_effects)
        health_rate_increase = 0.5 * ((self.health - self.current_health) / self.health)

        total_rate = lockstone_rate + level_rate_increase + status_effect_rate_increase + health_rate_increase

        squished_total_rate = max(0, min(100, total_rate * 100))

        return random.randint(0, 100) <= squished_total_rate

    def attempt_catch(self, player, lockstone):
        catch_is_successful = self.catch_successful(lockstone)
        if not catch_is_successful:
            print(f"{self.nickname} resisted the Lockstone!")
            return

        pet = Pet(
            id=None,
            player_id=player.id,
            species_name=self.species.name,
            level=self.level,
            experience=self.experience,
            nickname=self.nickname
        )

        pet.insert()

        print(f"{player.name} has locked {self.nickname}!")

    def learn(self, move_key, move_slot_number):
        if move_slot_number == 1:
            move_to_replace_name = self.move_1_name
        elif move_slot_number == 2:
            move_to_replace_name = self.move_2_name
        elif move_slot_number == 3:
            move_to_replace_name = self.move_3_name
        else:
            move_to_replace_name = self.move_4_name

        new_move_max_fuel = MoveList.moves.get(move_key).max_fuel
        if move_to_replace_name:
            move_to_replace = PetMove.get_by_pet_id_and_move_name(self.id, move_to_replace_name)
            new_move = PetMove(id=move_to_replace.id, pet_id=self.id, move_name=move_key,
                               current_fuel=new_move_max_fuel)
            new_move.update()
        else:
            new_move = PetMove(id=None, pet_id=self.id, move_name=move_key, current_fuel=new_move_max_fuel)
            new_move.insert()

        if move_slot_number == 1:
            self.move_1_name = new_move.move_name
        elif move_slot_number == 2:
            self.move_2_name = new_move.move_name
        elif move_slot_number == 3:
            self.move_3_name = new_move.move_name
        else:
            self.move_4_name = new_move.move_name

    def use_move(self, move_slot_number, target_pet):
        if move_slot_number == 1:
            move_name = self.move_1_name
        elif move_slot_number == 2:
            move_name = self.move_2_name
        elif move_slot_number == 3:
            move_name = self.move_3_name
        else:
            move_name = self.move_4_name

        if not move_name:
            return

        pet_move = PetMove.get_by_pet_id_and_move_name(self.id, move_name)

        if pet_move.current_fuel < 1:
            print(f"{pet_move.move_name} is out of fuel!")
            return

        pet_move.use(self, target_pet)

    def speed_adjust_experience(self, experience):
        return experience * (self.species.leveling_speed / 100)

    def give_experience(self, experience_to_add):
        loop_level = self.level
        experience_required = 0
        while (experience_to_add - self.experience) >= level_max_experience(loop_level):
            loop_level += 1
            experience_required = level_max_experience(loop_level)
        loop_level = min(loop_level, MAX_LEVEL)
        for level in range(self.level, loop_level):
            self.give_level(1)
        self.experience = experience_required if loop_level == MAX_LEVEL and experience_required < experience_to_add \
            else (experience_to_add - experience_required)

    def evolve(self, provide_summary, cancelled=False):
        if cancelled:
            self.update_stat_levels()

        evolution_name = self.species.evolution_name

        if evolution_name:
            evolve_summary = list()
            evolve_summary.append(f'{self.nickname} HAS EVOLVED INTO A {evolution_name}!')

            self.species = SpeciesList.species.get(evolution_name)
            self.nickname = self.nickname if self.nickname != self.name else self.species.name
            self.name = self.species.name

            health_increase = self.species.health - self.health
            self.health = self.species.health
            evolve_summary.append(f"HEALTH: +{health_increase} ({self.health})")

            defense_increase = self.species.defense - self.defense
            self.defense = self.species.defense
            evolve_summary.append(f"DEFENSE: +{defense_increase} ({self.defense})")

            attack_increase = self.species.attack - self.attack
            self.attack = self.species.attack
            evolve_summary.append(f"ATTACK: +{attack_increase} ({self.attack})")

            speed_increase = self.species.speed - self.speed
            self.speed = self.species.speed
            evolve_summary.append(f"SPEED: +{speed_increase} ({self.speed})")

            self.reset_all_current_stats()

            if provide_summary:
                print('\n'.join(evolve_summary))

    def reset_all_current_stats(self):
        self.current_health = self.health
        self.current_defense = self.defense
        self.current_attack = self.attack
        self.current_speed = self.speed

    def update_stat_levels(self, provide_summary):
        level_up_summary = list()
        level_up_summary.append(f'{self.nickname} IS NOW LEVEL {self.level}')

        health_increase = self.get_attribute_increase_amount("health")
        self.health += health_increase
        level_up_summary.append(f"HEALTH: +{health_increase} ({self.health})")

        defense_increase = self.get_attribute_increase_amount("defense")
        self.defense += defense_increase
        level_up_summary.append(f"DEFENSE: +{defense_increase} ({self.defense})")

        attack_increase = self.get_attribute_increase_amount("attack")
        self.attack += attack_increase
        level_up_summary.append(f"ATTACK: +{attack_increase} ({self.attack})")

        speed_increase = self.get_attribute_increase_amount("speed")
        self.speed += speed_increase
        level_up_summary.append(f"SPEED: +{speed_increase} ({self.speed})")

        self.reset_all_current_stats()

        if provide_summary:
            print('\n'.join(level_up_summary))

    def give_level(self, levels, provide_summary=True):
        if levels < 1:
            return

        for level in range(levels):
            self.level += 1
            evolution_level = self.species.evolution_level or MAX_LEVEL

            if MAX_LEVEL > self.level >= evolution_level:
                self.evolve(provide_summary=provide_summary)
            else:
                self.update_stat_levels(provide_summary=provide_summary)

    def get_first_evolution(self):
        previous_evolution = SpeciesList.species.get(self.species.previous_evolution_name)
        if not previous_evolution:
            return self.species

        loop_evolution = previous_evolution
        while loop_evolution:
            loop_evolution = SpeciesList.species.get(loop_evolution.previous_evolution_name)
            if loop_evolution:
                previous_evolution = loop_evolution

        return previous_evolution

    def get_attribute_increase_amount(self, attribute):

        attr_start = getattr(self.species, attribute) or 0

        attr_end = getattr(self.species, f"end_{attribute}") \
              or getattr(SpeciesList.species.get(self.species.evolution_name), attribute)

        attr_range = attr_end - attr_start

        level_start = 1
        prev_evol = SpeciesList.species.get(self.species.previous_evolution_name)
        if prev_evol:
            level_start = prev_evol.evolution_level

        level_end = self.species.evolution_level or MAX_LEVEL

        level_range = level_end - level_start

        attr_per_level = int(round(attr_range / level_range, 0))

        return attr_per_level

    def insert(self):
        with SQLiteConnector() as cur:
            query = '''
                INSERT INTO pet (player_id, species_name, level, experience, nickname, health, defense, attack, speed, current_health, current_defense, current_attack, current_speed, move_1_name, move_2_name, move_3_name, move_4_name)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            values = (
            self.player_id, self.species.name, self.level, self.experience, self.nickname, self.health, self.defense,
            self.attack, self.speed, self.current_health, self.current_defense, self.current_attack, self.current_speed,
            self.move_1_name, self.move_2_name, self.move_3_name, self.move_4_name)
            cur.execute(query, values)
            self.id = cur.lastrowid

    def update(self):
        with SQLiteConnector() as cur:
            query = '''
                UPDATE pet
                SET player_id = ?, species_name = ?, level = ?, experience = ?, nickname = ?, health = ?, defense = ?, attack = ?, speed = ?, current_health = ?, current_defense = ?, current_attack = ?, current_speed = ?, move_1_name = ?, move_2_name = ?, move_3_name = ?, move_4_name = ?
                WHERE id = ?
            '''
            values = (
            self.player_id, self.species.name, self.level, self.experience, self.nickname, self.health, self.defense,
            self.attack, self.speed, self.current_health, self.current_defense, self.current_attack, self.current_speed,
            self.move_1_name, self.move_2_name, self.move_3_name, self.move_4_name, self.id)
            cur.execute(query, values)

    @classmethod
    def delete(cls, id):
        with SQLiteConnector() as cur:
            query = f"DELETE FROM pet WHERE id = ?"
            values = (id,)
            cur.execute(query, values)

    @classmethod
    def get_by_id(cls, id):
        with SQLiteConnector() as cur:
            query = '''
                SELECT * FROM pet
                WHERE id = ?
            '''
            values = (id,)
            cur.execute(query, values)
            row = cur.fetchone()
            return Pet(*row)


def level_max_experience(level: int):
    exp_add = lambda a: LEVEL_1_EXPERIENCE_REQUIRED * a
    add = lambda a, b: a + b
    levels = [exp_add(level) for level in range(1, level + 1)]
    return reduce(add, levels)
