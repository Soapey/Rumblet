import pygame

from rumblet.classes.db.SQLiteConnector import SQLiteConnector
from rumblet.classes.player.PlayerLockstone import PlayerLockstone
from rumblet.classes.lockstone.LockstoneList import LockstoneList
from rumblet.classes.zone.ZonesList import ZonesList
from rumblet.classes.utils import is_colliding

class Player:
    def __init__(self, id, name, current_zone_name, money=0, x=0, y=0, width=0, height=0, colour=None):
        self.id = id
        self.name = name
        self.current_zone_name = current_zone_name
        self.money = money
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.colour = colour or (0, 0, 0)
        self.velX = 0
        self.velY = 0
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.speed = 2

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect)

    def update_loc(self, screen_width, screen_height):
        self.velX = 0
        self.velY = 0
        if self.left_pressed and not self.right_pressed:
            self.velX = -self.speed
        if self.right_pressed and not self.left_pressed:
            self.velX = self.speed
        if self.up_pressed and not self.down_pressed:
            self.velY = -self.speed
        if self.down_pressed and not self.up_pressed:
            self.velY = self.speed

        target_x = self.x + self.velX
        target_y = self.y + self.velY

        if target_x < 0:
            zone_left_name = self.zone().zone_left_name
            if zone_left_name:
                self.current_zone_name = zone_left_name
                self.x = screen_width - self.width
            else:
                self.x = 0
        elif target_x + self.width > screen_width:
            zone_right_name = self.zone().zone_right_name
            if zone_right_name:
                self.current_zone_name = zone_right_name
                self.x = 0
            else:
                self.x = screen_width - self.width
        else:
            self.x = target_x

        if target_y < 0:
            zone_up_name = self.zone().zone_up_name
            if zone_up_name:
                self.current_zone_name = zone_up_name
                self.y = screen_height - self.height
            else:
                self.y = 0
        elif target_y + self.height > screen_height:
            zone_down_name = self.zone().zone_down_name
            if zone_down_name:
                self.current_zone_name = zone_down_name
                self.y = 0
            else:
                self.y = screen_height - self.width
        else:
            self.y = target_y

        for cell in self.zone().area:
            colliding = is_colliding(self.x, self.y, self.width, self.height, cell.x, cell.y, self.width, self.height) or is_colliding(cell.x, cell.y, self.width, self.height, self.x, self.y, self.width, self.height)

            if colliding:
                cell.on_collision(self)

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


    def zone(self):
        return ZonesList.zones.get(self.current_zone_name)


    def give_max_lockstones(self):
        PlayerLockstone(None, self.id, LockstoneList.basic_lockstone.name, 999).insert()
        PlayerLockstone(None, self.id, LockstoneList.elemental_lockstone.name, 999).insert()
        PlayerLockstone(None, self.id, LockstoneList.celestial_lockstone.name, 999).insert()
        PlayerLockstone(None, self.id, LockstoneList.esoteric_lockstone.name, 999).insert()
        PlayerLockstone(None, self.id, LockstoneList.arcanum_lockstone.name, 999).insert()
        PlayerLockstone(None, self.id, LockstoneList.divine_lockstone.name, 999).insert()

    def get_lockstone_by_name(self, lockstone_name):
        with SQLiteConnector() as cur:
            query = '''
                SELECT * FROM playerlockstone
                WHERE player_id = ? AND lockstone_name = ?
            '''
            values = (self.id, lockstone_name)
            cur.execute(query, values)
            row = cur.fetchone()
            playerlockstone = PlayerLockstone(*row)

            if not playerlockstone.count:
                return None

            return LockstoneList.lockstones.get(playerlockstone.lockstone_name)

    def insert(self):
        with SQLiteConnector() as cur:
            query = '''
                INSERT INTO player (name, money, x, y)
                VALUES (?, ?, ?, ?)
            '''
            values = (self.name, self.money, self.x, self.y)
            cur.execute(query, values)
            self.id = cur.lastrowid

    def update(self):
        with SQLiteConnector() as cur:
            query = '''
                UPDATE player
                SET name = ?, money = ?, x = ?, y = ?
                WHERE id = ?
            '''
            values = (self.name, self.money, self.x, self.y, self.id)
            cur.execute(query, values)

    @classmethod
    def delete(cls, id):
        with SQLiteConnector() as cur:
            query = f"DELETE FROM player WHERE id = ?"
            values = (id,)
            cur.execute(query, values)
