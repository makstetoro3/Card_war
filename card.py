import pygame as pg
import sqlite3


class Card(pg.sprite.Sprite):  # класс Карты
    def __init__(self, size, card_id, land=-1):  # получает размер и id карты
        pg.sprite.Sprite.__init__(self)
        self.id = card_id
        self.land = land
        self.image = pg.transform.scale(pg.image.load(f'cards/{card_id}.png').convert_alpha(), size)
        self.pos = (0, 0)
        self.rect = pg.Rect(0, 0, *size)
        con = sqlite3.connect('card_war.db')
        cur = con.cursor()
        info = cur.execute(f'SELECT * FROM cards WHERE id = {card_id}').fetchall()[0]

        self.status = 0  # свойство карты
        self.price = info[2]
        self.type = info[3]
        self.object = info[4]
        if not self.object == 2:
            self.floop = info[5]
            self.floop_price = info[6]
            if not self.object:
                self.atc = info[7]
                self.hp = info[8]

    def zeroing(self) -> None:  # возращает карту на место (pos)
        self.rect.move_ip(self.pos[0] - self.rect.x, self.pos[1] - self.rect.y)

    def dead(self, cemetery) -> None:  # уберает карту в сброс
        self.rect.move_ip(cemetery[0] - self.pos[0], cemetery[1] - self.pos[1])
        self.status = -1
        self.land = -1

    def set_land(self, land) -> None:
        self.rect = land
        self.pos = (self.rect.x, self.rect.y)
        self.status = 2  # устанавливаем новый статус карты

    def location(self, n, hand_pos, indent, slider) -> None:
        self.pos = (
            hand_pos[0] + indent[0] * (n & 1), hand_pos[1] + indent[1] * (n >> 1) - slider * (self.rect.h >> 2))
        self.zeroing()

    def drawing(self, surface: pg.Surface, hand_pos) -> None:
        surface.blit(self.image,
                     pg.Rect(self.rect.x - hand_pos[0], self.rect.y - hand_pos[1], self.rect.w, self.rect.h))

    def scroll(self, n) -> None:
        self.pos = (self.pos[0], self.pos[1] + (self.rect.h >> 2) * n)
        self.zeroing()

    def update(self, pos: tuple, surface: pg.Surface, size: tuple) -> None:
        if self.rect.collidepoint(pg.mouse.get_pos()):
            surface.blit(pg.transform.scale(pg.image.load(f'cards/{self.id}.png'), size),
                         pg.Rect(*pos, *size))
