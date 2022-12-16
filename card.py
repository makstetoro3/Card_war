import pygame as pg
import sqlite3


class Card(pg.sprite.Sprite):  # класс Карты
    def __init__(self, size: tuple, card_id: int, land=-1):  # получает размер и id карты
        pg.sprite.Sprite.__init__(self)
        self.id = card_id
        self.land = land
        self.image = pg.transform.scale(pg.image.load(f'cards/{card_id}.png').convert_alpha(), size)
        self.pos = (0, 0)
        self.rect = pg.Rect(0, 0, *size)
        self.default: pg.Rect = self.rect
        con = sqlite3.connect('card_war.db')
        cur = con.cursor()
        info = cur.execute(f'SELECT * FROM cards WHERE id = {card_id}').fetchall()[0]
        self.case = 0

        self.status = 0  # свойство карты
        self.price = info[2]
        self.type = info[3]
        self.object = info[4]
        if not self.object == 2:
            self.floop = info[5]
            self.floop_price = info[6]
            if self.object == 0:
                self.atc = info[7]
                self.hp = info[8]
                self.specifications()

    def zeroing(self) -> None:  # возращает карту на место (pos)
        self.rect.move_ip(self.pos[0] - self.rect.x, self.pos[1] - self.rect.y)
        self.default.move_ip(self.pos[0] - self.default.x, self.pos[1] - self.default.y)

    def dead(self, cemetery: tuple) -> None:  # уберает карту в сброс
        self.rect.move_ip(cemetery[0] - self.pos[0], cemetery[1] - self.pos[1])
        self.status = -1
        self.land = -1

    def set_land(self, land: pg.Rect) -> None:
        self.rect = land
        self.default = land
        self.pos = (self.rect.x, self.rect.y)
        self.status = 2  # устанавливаем новый статус карты

    def location(self, n: int, hand_pos: tuple, indent: tuple, slider: int) -> None:
        self.pos = (
            hand_pos[0] + indent[0] * (n & 1), hand_pos[1] + indent[1] * (n >> 1) - slider * (self.rect.h >> 2))
        self.zeroing()

    def drawing(self, surface: pg.Surface, hand_pos: tuple) -> None:
        surface.blit(self.image,
                     pg.Rect(self.rect.x - hand_pos[0], self.rect.y - hand_pos[1], self.rect.w, self.rect.h))

    def scroll(self, n: int) -> None:
        self.pos = (self.pos[0], self.pos[1] + (self.rect.h >> 2) * n)
        self.zeroing()

    def viev(self, new: pg.Rect):
        self.rect = new.copy()
        self.pos = (new.x, new.y)
        self.image = pg.transform.rotate(self.image, 180)

    def alt(self, img, size):
        res = pg.transform.scale(img, size)
        if self.object == 0:
            pg.draw.rect(res, (255, 255, 255),
                         pg.Rect(size[0] * 0.819, size[1] * 0.8625, size[0] * 0.1, size[1] * 0.0721))
            pg.draw.rect(res, (255, 255, 255),
                         pg.Rect(size[0] * 0.101, size[1] * 0.863, size[0] * 0.08, size[1] * 0.0725))
            font = pg.font.Font('base.ttf', 48)
            res.blit(font.render(str(self.hp), True, (0, 0, 0)), (size[0] * 0.819, size[1] * 0.88))
            res.blit(font.render(str(self.hp), True, (0, 0, 0)), (size[0] * 0.101, size[1] * 0.88))
        return res

    def specifications(self):
        pg.draw.rect(self.image, (255, 255, 255),
                     pg.Rect(self.default.w * 0.825, self.default.h * 0.87,
                             self.default.w * 0.095, self.default.h * 0.075))
        pg.draw.rect(self.image, (255, 255, 255),
                     pg.Rect(self.default.w * 0.1, self.default.h * 0.87,
                             self.default.w * 0.095, self.default.h * 0.075))
        font = pg.font.Font('base.ttf', 12)
        self.image.blit(font.render(str(self.hp), True, (0, 0, 0)), (self.default.w * 0.825, self.default.h * 0.88))
        self.image.blit(font.render(str(self.hp), True, (0, 0, 0)), (self.default.w * 0.11, self.default.h * 0.88))
