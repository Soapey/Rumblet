import pygame

from rumblet.classes.bag.BagItemList import BagItemList
from rumblet.classes.db.SQLiteConnector import SQLiteConnector
from rumblet.classes.db.SQLiteSchema import SQLiteSchema
from rumblet.classes.game.Constants import CELL_WIDTH, CELL_HEIGHT, MAX_PARTY_SIZE
from rumblet.classes.lockstone.LockstoneList import LockstoneList
from rumblet.classes.pet.Pet import Pet
from rumblet.classes.pet.SpeciesName import SpeciesName
from rumblet.classes.player.PlayerBagItem import PlayerBagItem
from rumblet.classes.player.PlayerPartyPet import PlayerPartyPet
from rumblet.classes.utils import get_grid_index
from rumblet.classes.zone.Zones import Zones


class Player:
    table = SQLiteSchema.table_player

    def __init__(
            self,
            game,
            id,
            name,
            current_zone_name,
            grid_cell_x,
            grid_cell_y,
            facing_direction=1,
            money=0,
            x=None,
            y=None,
            colour=None,
    ):
        self.game = game
        self.id = id
        self.name = name
        self.current_zone_name = current_zone_name
        self.grid_cell_x = grid_cell_x
        self.grid_cell_y = grid_cell_y
        self.facing_direction = facing_direction
        self.money = money
        self.x = x or (grid_cell_x * CELL_WIDTH) + (CELL_WIDTH // 2)
        self.y = y or (grid_cell_y * CELL_HEIGHT) + (CELL_HEIGHT // 2)
        self.colour = colour or (0, 0, 0)
        self.velX = 0
        self.velY = 0
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.speed = 2

    def top_left_x(self):
        return self.x - (CELL_WIDTH // 2)

    def top_left_y(self):
        return self.y - (CELL_HEIGHT // 2)

    def get_rect(self):
        return pygame.Rect(self.top_left_x(), self.top_left_y(), CELL_WIDTH, CELL_HEIGHT)

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.get_rect())

    def check_for_on_collision(self):
        zones = Zones(self.game)
        for cell in zones.list.get(self.current_zone_name).area:
            player_coords = (self.grid_cell_x, self.grid_cell_y)
            cell_coords = (cell.grid_cell_x, cell.grid_cell_y)
            if player_coords == cell_coords:
                cell.on_collision(self, zones.list.get(self.current_zone_name))
                break

    def update_x(self, new_x):
        self.x = new_x
        before_grid_cell = self.grid_cell_x
        after_grid_cell = get_grid_index(self.x, CELL_WIDTH)
        self.grid_cell_x = after_grid_cell
        if before_grid_cell != after_grid_cell:
            self.check_for_on_collision()

    def update_y(self, new_y):
        self.y = new_y
        before_grid_cell = self.grid_cell_y
        after_grid_cell = get_grid_index(self.y, CELL_HEIGHT)
        self.grid_cell_y = after_grid_cell
        if before_grid_cell != after_grid_cell:
            self.check_for_on_collision()

    def update_loc(self, screen_width, screen_height):
        self.velX = 0
        self.velY = 0
        if self.left_pressed and not self.right_pressed:
            self.velX = -self.speed
            self.facing_direction = 4
        if self.right_pressed and not self.left_pressed:
            self.velX = self.speed
            self.facing_direction = 2
        if self.up_pressed and not self.down_pressed:
            self.velY = -self.speed
            self.facing_direction = 1
        if self.down_pressed and not self.up_pressed:
            self.velY = self.speed
            self.facing_direction = 3

        target_x = self.x + self.velX
        target_y = self.y + self.velY

        player_zone = Zones().list.get(self.current_zone_name)

        if target_x < (CELL_WIDTH // 2):
            zone_left_name = player_zone.zone_left_name
            if zone_left_name:
                self.update_x(target_x)
                if self.x <= 0:
                    self.current_zone_name = zone_left_name
                    self.update_x(screen_width)
            else:
                self.update_x(CELL_WIDTH // 2)
        elif target_x + (CELL_WIDTH // 2) > screen_width:
            zone_right_name = player_zone.zone_right_name
            if zone_right_name:
                self.update_x(target_x)
                if self.x >= screen_width:
                    self.current_zone_name = zone_right_name
                    self.update_x(0)
            else:
                self.update_x(screen_width - (CELL_WIDTH // 2))
        else:
            self.update_x(target_x)

        if target_y < (CELL_HEIGHT // 2):
            zone_up_name = player_zone.zone_up_name
            if zone_up_name:
                self.update_y(target_y)
                if self.y <= 0:
                    self.current_zone_name = zone_up_name
                    self.update_y(screen_height)
            else:
                self.update_y(CELL_HEIGHT // 2)
        elif target_y + (CELL_HEIGHT // 2) > screen_height:
            zone_down_name = player_zone.zone_down_name
            if zone_down_name:
                self.update_y(target_y)
                if self.y >= screen_width:
                    self.current_zone_name = zone_down_name
                    self.update_y(0)
            else:
                self.update_y(screen_height - (CELL_WIDTH // 2))
        else:
            self.update_y(target_y)

    @classmethod
    def create_new_player(cls, game, name, max_money=False, max_lockstones=False):
        player = Player(
            game=game,
            id=None,
            name=name,
            current_zone_name=Zones().starting_zone.name,
            grid_cell_x=1,
            grid_cell_y=1
        )
        player.insert()
        player.create_bag()
        player.create_party()
        player.create_starter_pet()
        if max_money:
            player.give_max_money()
        if max_lockstones:
            player.give_max_lockstones()
        return player

    def create_starter_pet(self):
        pet = Pet(
            obj_id=None,
            player_id=self.id,
            species_name=SpeciesName.DEWLEAF.value,
            level=3,
            experience=0,
            nickname="Grant's Starter Pet",
        )
        pet.insert()
        pet.learn("Hydrostream Rush", 1)
        pet.update()

        next_available_slot_number = PlayerPartyPet.next_available_party_slot_by_player_id(player_id=self.id)

        playerpartypet = PlayerPartyPet.get_by_player_id_and_slot_number(player_id=self.id, slot_number=next_available_slot_number)
        playerpartypet.pet_id = pet.id
        playerpartypet.update()

    def create_bag(self):
        for bag_item_name, bag_item in BagItemList.items.items():
            player_bag_item = PlayerBagItem(
                id=None,
                player_id=self.id,
                bag_item_name=bag_item_name,
                quantity=0
            )
            player_bag_item.insert()

    def create_party(self):
        for slot_number in range(1, MAX_PARTY_SIZE+1):
            playerpartypet = PlayerPartyPet(
                id=None,
                player_id=self.id,
                pet_id=None,
                slot_number=slot_number
            )
            playerpartypet.insert()

    def bag(self):
        return PlayerBagItem.get_all_by_player_id(self.id)

    def party(self):
        return PlayerPartyPet.get_party_by_player_id(self.id)

    def next_available_party_slot(self):
        return PlayerPartyPet.next_available_party_slot_by_player_id(self.id)

    def give_max_money(self):
        self.money = 999_999
        self.update()

    def give_max_lockstones(self):
        bag = self.bag()
        if not bag:
            return
        for lockstone_name in LockstoneList.lockstones.keys():
            bag.get(lockstone_name).set_item_quantity(999)

    @classmethod
    def get_by_id(cls, game, id):
        with SQLiteConnector() as cur:
            query = f"SELECT * FROM player WHERE id = ?"
            values = (id,)
            cur.execute(query, values)
            row = cur.fetchone()
            return Player(
                game=game,
                id=row[cls.table.get_column_index_by_name("id")],
                name=row[cls.table.get_column_index_by_name("name")],
                current_zone_name=row[cls.table.get_column_index_by_name("current_zone_name")],
                grid_cell_x=row[cls.table.get_column_index_by_name("grid_cell_x")],
                grid_cell_y=row[cls.table.get_column_index_by_name("grid_cell_y")],
                facing_direction=row[cls.table.get_column_index_by_name("facing_direction")],
                money=row[cls.table.get_column_index_by_name("money")]
            )

    def insert(self):
        with SQLiteConnector() as cur:
            query = f'''
                INSERT INTO player (name, current_zone_name, grid_cell_x, grid_cell_y, facing_direction, money)
                VALUES (?, ?, ?, ?, ?, ?)
            '''
            values = (
                self.name,
                self.current_zone_name,
                self.grid_cell_x,
                self.grid_cell_y,
                self.facing_direction,
                self.money
            )
            cur.execute(query, values)
            self.id = cur.lastrowid

    def update(self):
        with SQLiteConnector() as cur:
            query = '''
                UPDATE player
                SET name = ?, current_zone_name = ?, grid_cell_x = ?, grid_cell_y = ?, facing_direction = ?, money = ?
                WHERE id = ?
            '''
            values = (
                self.name,
                self.current_zone_name,
                self.grid_cell_x,
                self.grid_cell_y,
                self.facing_direction,
                self.money,
                self.id
            )
            cur.execute(query, values)

    @classmethod
    def delete(cls, id):
        with SQLiteConnector() as cur:
            query = f"DELETE FROM player WHERE id = ?"
            values = (id,)
            cur.execute(query, values)
