from functools import reduce

from rumblet.classes.db.SQLiteConnector import SQLiteConnector
from rumblet.classes.move.MoveList import MoveList
from rumblet.classes.pet.PetMove import PetMove
from rumblet.classes.pet.SpeciesList import SpeciesList

MAX_LEVEL = 100
LEVEL_1_EXPERIENCE_REQUIRED = 100


class Pet:
    def __init__(
            self,
            obj_id,
            player_id,
            species_name,
            level,
            experience,
            nickname=None,
            health=None,
            defense=None,
            attack=None,
            speed=None,
            current_health=None,
            current_defense=None,
            current_attack=None,
            current_speed=None,
            move_1_name=None,
            move_2_name=None,
            move_3_name=None,
            move_4_name=None,
            status_effects=None
    ):
        self.obj_id = obj_id
        self.player_id = player_id
        self.species = SpeciesList.species.get(species_name)
        self.name = species_name
        self.nickname = nickname or species_name
        self.level = level if self.obj_id else 0
        self.experience = experience
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
        self.status_effects = status_effects or list()

        if not self.obj_id:
            self.give_level(levels=level, provide_summary=False)

    def __str__(self):
        return f"{self.name} ({self.level})"

    def __repr__(self):
        attributes_string = ', '.join(f'{k}={v}' for k, v in vars(self).items())
        return f"{self.__class__.__name__}-{self.name}({attributes_string})"

    def move_names(self):
        return {
            1: self.move_1_name,
            2: self.move_2_name,
            3: self.move_3_name,
            4: self.move_4_name,
        }

    def learnable_moves_at_level(self):
        evol = self.get_first_evolution()

        main_learnable_moves = dict()

        calculating = True
        while calculating:
            learnable_moves = evol.learnable_moves
            learnable_moves_below_current_level = {
                move_name
                for learned_at_level, move_name
                in learnable_moves.items()
                if learned_at_level <= self.level
            }

            for move_name in learnable_moves_below_current_level:
                main_learnable_moves[move_name] = MoveList.moves.get(move_name)

            evol = SpeciesList.next_evolution(evol)

            if evol == SpeciesList.next_evolution(self.species):
                calculating = False

        return main_learnable_moves

    def learn(self, move_key, move_slot_number):

        if not self.obj_id:
            print("Pet must be owned to learn a move!")
            return

        move_to_replace_name = getattr(self, f"move_{move_slot_number}_name")

        new_move_max_fuel = MoveList.moves.get(move_key).max_fuel
        if move_to_replace_name:
            move_to_replace = PetMove.get_by_pet_id_and_move_name(self.obj_id, move_to_replace_name)
            new_move = PetMove(id=move_to_replace.obj_id, pet_id=self.obj_id, move_name=move_key,
                               current_fuel=new_move_max_fuel)
            new_move.update()
        else:
            new_move = PetMove(id=None, pet_id=self.obj_id, move_name=move_key, current_fuel=new_move_max_fuel)
            new_move.insert()

        setattr(self, f"move_{move_slot_number}_name", new_move.move_name)

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
            self.update_stat_levels(provide_summary)

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
        evol = self.species

        while SpeciesList.previous_evolution(evol):
            evol = SpeciesList.previous_evolution(evol)

        return evol

    def get_attribute_increase_amount(self, attribute):

        attr_start = getattr(self.species, attribute) or 0

        attr_end = \
            getattr(self.species, f"end_{attribute}") or \
            getattr(SpeciesList.species.get(self.species.evolution_name), attribute)

        attr_range = attr_end - attr_start

        level_start = 1
        prev_evol = SpeciesList.species.get(self.species.previous_evolution_name)
        if prev_evol:
            level_start = prev_evol.evolution_level

        level_end = self.species.evolution_level or MAX_LEVEL

        level_range = level_end - level_start

        if level_range > 0:
            attr_per_level = int(round(attr_range / level_range, 0))
        else:
            attr_per_level = attr_range

        return attr_per_level



    def use_move(self, move_slot_number, target_pet):
        move_name = getattr(self, f"move_{move_slot_number}_name")
        if not move_name:
            return

        pet_move = PetMove.get_by_pet_id_and_move_name(self.obj_id, move_name)

        if pet_move.current_fuel < 1:
            print(f"{pet_move.move_name} is out of fuel!")
            return

        pet_move.use(self, target_pet)

    def insert(self):
        with SQLiteConnector() as cur:
            query = '''
                INSERT INTO 
                    pet (
                        player_id, species_name, level, experience, nickname, 
                        health, defense, attack, speed, 
                        current_health, current_defense, current_attack, current_speed, 
                        move_1_name, move_2_name, move_3_name, move_4_name
                    )
                VALUES 
                    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            values = (
                self.player_id, self.species.name, self.level, self.experience, self.nickname, self.health,
                self.defense,
                self.attack, self.speed, self.current_health, self.current_defense, self.current_attack,
                self.current_speed,
                self.move_1_name, self.move_2_name, self.move_3_name, self.move_4_name)
            cur.execute(query, values)
            self.obj_id = cur.lastrowid

    def update(self):
        with SQLiteConnector() as cur:
            query = '''
                UPDATE 
                    pet
                SET 
                    player_id = ?, species_name = ?, level = ?, experience = ?, nickname = ?, 
                    health = ?, defense = ?, attack = ?, speed = ?, 
                    current_health = ?, current_defense = ?, current_attack = ?, current_speed = ?,
                    move_1_name = ?, move_2_name = ?, move_3_name = ?, move_4_name = ?
                WHERE 
                    id = ?
            '''
            values = (
                self.player_id, self.species.name, self.level, self.experience, self.nickname, self.health,
                self.defense,
                self.attack, self.speed, self.current_health, self.current_defense, self.current_attack,
                self.current_speed,
                self.move_1_name, self.move_2_name, self.move_3_name, self.move_4_name, self.obj_id)
            cur.execute(query, values)

    @classmethod
    def delete(cls, id):
        with SQLiteConnector() as cur:
            query = '''
                DELETE FROM 
                    pet 
                WHERE 
                    id = ?
            '''
            values = (id,)
            cur.execute(query, values)

    @classmethod
    def get_by_id(cls, id):
        with SQLiteConnector() as cur:
            query = '''
                SELECT * FROM 
                    pet
                WHERE 
                    id = ?
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
