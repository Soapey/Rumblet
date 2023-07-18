from functools import reduce
from rumblet.pet_templates import read_pet_template
from rumblet.move_templates import read_move_template


MAX_LEVEL = 100
LEVEL_1_EXPERIENCE_REQUIRED = 100


class Pet:
    def __init__(
            self,
            id: int, template_key: str, level: int, experience: int, nickname: str = None,
            health: int = None, defense: int = None, attack: int = None, speed: int = None,
            current_health: int = None, current_defense: int = None, current_attack: int = None,
            current_speed: int = None,
            move_1_key: str = None, move_2_key: str = None, move_3_key: str = None, move_4_key: str = None
    ):
        self.id = id
        self.pet_template = read_pet_template(template_key)
        self.name = template_key
        self.nickname = nickname or template_key
        self.level: int = level
        self.experience: int = experience

        self.health = health or self.pet_template.get("health")
        self.defense = defense or self.pet_template.get("defense")
        self.attack = attack or self.pet_template.get("attack")
        self.speed = speed or self.pet_template.get("speed")

        self.current_health = current_health or self.health
        self.current_defense = current_defense or self.defense
        self.current_attack = current_attack or self.attack
        self.current_speed = current_speed or self.speed

        self.moves: dict = dict()
        self.moves[1] = read_move_template(move_1_key)
        self.moves[2] = read_move_template(move_2_key)
        self.moves[3] = read_move_template(move_3_key)
        self.moves[4] = read_move_template(move_4_key)

    # How the class will appear to players in a string
    def __str__(self):
        return f"{self.name} ({self.level})"

    # How the class will appear to developers in the console
    def __repr__(self):
        attributes_string = ', '.join(f'{k}={v}' for k, v in vars(self).items())
        return f"{self.__class__.__name__}-{self.name}({attributes_string})"

    def speed_adjust_experience(self, experience):
        return experience * (self.pet_template.get("leveling_speed") / 100)

    def give_experience(self, experience_to_add):
        loop_level = self.level
        experience_required = 0
        while (experience_to_add - self.experience) >= level_max_experience(loop_level):
            loop_level += 1
            experience_required = level_max_experience(loop_level)
        loop_level = min(loop_level, MAX_LEVEL)
        for level in range(self.level, loop_level):
            self.level_up()
        self.experience = experience_required if loop_level == MAX_LEVEL and experience_required < experience_to_add \
            else (experience_to_add - experience_required)

    def evolve(self):
        evolution_key = self.pet_template.get("evolution_key")

        evolve_summary = list()
        evolve_summary.append(f'{self.nickname} HAS EVOLVED INTO A {evolution_key}!')

        if evolution_key:
            self.pet_template = read_pet_template(evolution_key)
            self.nickname = self.nickname if self.nickname != self.name else self.pet_template.get("name")
            self.name = self.pet_template.get("name")

            health_increase = self.pet_template.get("health") - self.health
            self.health = self.pet_template.get("health")
            evolve_summary.append(f"HEALTH: +{health_increase}")

            defense_increase = self.pet_template.get("defense") - self.defense
            self.defense = self.pet_template.get("defense")
            evolve_summary.append(f"DEFENSE: +{defense_increase}")

            attack_increase = self.pet_template.get("attack") - self.attack
            self.attack = self.pet_template.get("attack")
            evolve_summary.append(f"ATTACK: +{attack_increase}")

            speed_increase = self.pet_template.get("speed") - self.speed
            self.speed = self.pet_template.get("speed")
            evolve_summary.append(f"SPEED: +{speed_increase}")

        print('\n'.join(evolve_summary))

    def update_stat_levels(self):
        level_up_summary = list()
        level_up_summary.append(f'{self.nickname} IS NOW LEVEL {self.level}')

        evolution_level = self.pet_template.get("evolution_level") or MAX_LEVEL

        evolution_key = self.pet_template.get("evolution_key")
        evolution_template = read_pet_template(evolution_key)

        end_health = self.pet_template.get("end_health") or evolution_template.get("health")
        end_defense = self.pet_template.get("end_defense") or evolution_template.get("defense")
        end_attack = self.pet_template.get("end_attack") or evolution_template.get("attack")
        end_speed = self.pet_template.get("end_speed") or evolution_template.get("speed")

        health_increase = int(round((end_health - self.health) / max(evolution_level - self.level + 1, 1), 0))
        self.health += health_increase
        level_up_summary.append(f"HEALTH: +{health_increase}")

        defense_increase = int(round((end_defense - self.defense) / max(evolution_level - self.level + 1, 1), 0))
        self.defense += defense_increase
        level_up_summary.append(f"DEFENSE: +{defense_increase}")

        attack_increase = int(round((end_attack - self.attack) / max(evolution_level - self.level + 1, 1), 0))
        self.attack += attack_increase
        level_up_summary.append(f"ATTACK: +{attack_increase}")

        speed_increase = int(round((end_speed - self.speed) / max(evolution_level - self.level + 1, 1), 0))
        self.speed += speed_increase
        level_up_summary.append(f"SPEED: +{speed_increase}")

        print('\n'.join(level_up_summary))

    def level_up(self):
        self.level += 1
        evolution_level = self.pet_template.get("evolution_level") or MAX_LEVEL

        if MAX_LEVEL > self.level >= evolution_level:
            self.evolve()
            return

        self.update_stat_levels()


def level_max_experience(level: int):
    exp_add = lambda a: LEVEL_1_EXPERIENCE_REQUIRED * a
    add = lambda a, b: a+b
    levels = [exp_add(level) for level in range(1, level + 1)]
    return reduce(add, levels)
