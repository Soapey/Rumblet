import pygame

from rumblet.classes.db.SQLiteConnector import SQLiteConnector
from rumblet.classes.zone.ZonesList import ZonesList
from rumblet.classes.bag.BagItemList import BagItemList
from rumblet.classes.player.PlayerBagItem import PlayerBagItem
from rumblet.classes.lockstone.LockstoneList import LockstoneList
from rumblet.classes.utils import get_grid_index, grid_indexes_are_colliding


class Player:
    def __init__(self, id, name, current_zone_name, grid_cell_x, grid_cell_y, facing_direction=1, money=0, x=None, y=None, width=0, height=0, colour=None):
        self.id = id
        self.name = name
        self.current_zone_name = current_zone_name
        self.grid_cell_x = grid_cell_x
        self.grid_cell_y = grid_cell_y
        self.facing_direction = facing_direction
        self.money = money
        self.x = x or grid_cell_x * width
        self.y = y or grid_cell_y * height
        self.width = width
        self.height = height
        self.colour = colour or (0, 0, 0)
        self.velX = 0
        self.velY = 0
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.speed = 2

    def top_left_x(self):
        return self.x - (self.width // 2)

    def top_left_y(self):
        return self.y - (self.height // 2)

    def get_rect(self):
        return pygame.Rect(self.top_left_x(), self.top_left_y(), self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.get_rect())

    def check_for_on_collision(self):
        for cell in self.zone().area:
            cell_center_x = (cell.x * self.width) + (self.width // 2)
            cell_center_y = (cell.y * self.height) + (self.height // 2)
            if grid_indexes_are_colliding(self.x, self.y, cell_center_x, cell_center_y, self.width, self.height):
                cell.on_collision(self)
                break

    def update_x(self, new_x):
        self.x = new_x
        before_grid_cell = self.grid_cell_x
        after_grid_cell = get_grid_index(self.x, self.width)
        self.grid_cell_x = after_grid_cell
        if before_grid_cell != after_grid_cell:
            self.check_for_on_collision()

    def update_y(self, new_y):
        self.y = new_y
        before_grid_cell = self.grid_cell_y
        after_grid_cell = get_grid_index(self.y, self.height)
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

        if target_x < (self.width // 2):
            zone_left_name = self.zone().zone_left_name
            if zone_left_name:
                self.current_zone_name = zone_left_name
                self.update_x(screen_width - (self.width // 2))
            else:
                self.update_x(self.width // 2)
        elif target_x + (self.width // 2) > screen_width:
            zone_right_name = self.zone().zone_right_name
            if zone_right_name:
                self.current_zone_name = zone_right_name
                self.update_x(self.width // 2)
            else:
                self.update_x(screen_width - (self.width // 2))
        else:
            self.update_x(target_x)

        if target_y < (self.height // 2):
            zone_up_name = self.zone().zone_up_name
            if zone_up_name:
                self.current_zone_name = zone_up_name
                self.update_y(screen_height - (self.height // 2))
            else:
                self.update_y(self.height // 2)
        elif target_y + (self.height // 2) > screen_height:
            zone_down_name = self.zone().zone_down_name
            if zone_down_name:
                self.current_zone_name = zone_down_name
                self.update_y(self.height // 2)
            else:
                self.update_y(screen_height - (self.width // 2))
        else:
            self.update_y(target_y)

    @classmethod
    def create_new_player(cls, name, width, height, max_money=False, max_lockstones=False):
        player = Player(
            id=None,
            name=name,
            current_zone_name=ZonesList.starting_zone.name,
            grid_cell_x=1,
            grid_cell_y=1,
            width=width,
            height=height
        )
        player.insert()
        player.create_bag()
        if max_money:
            player.give_max_money()
        if max_lockstones:
            player.give_max_lockstones()
        return player

    def create_bag(self):
        for bag_item_name, bag_item in BagItemList.items.items():
            player_bag_item = PlayerBagItem(
                id=None,
                player_id=self.id,
                bag_item_name=bag_item_name,
                quantity=0
            )
            player_bag_item.insert()

    def bag(self):
        return PlayerBagItem.get_all_by_player_id(self.id)

    def zone(self):
        return ZonesList.zones.get(self.current_zone_name)

    def give_max_money(self):
        self.money = 999_999
        self.update()

    def give_max_lockstones(self):
        bag = self.bag()
        if not bag:
            return
        for lockstone_name in LockstoneList.lockstones.keys():
            bag.get(lockstone_name).set_item_quantity(999)

    def insert(self):
        with SQLiteConnector() as cur:
            query = '''
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
