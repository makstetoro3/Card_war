import pygame as pg
from card import Card
from land import Land
from player import Player
from random import randint


def pvp(screen: pg.Surface, W: int, H: int, decks: list) -> None:
    size = W, H
    runGame = True
    card_h = H // 3
    card_w = int(card_h * 0.7)  # размеры карт
    sard_h = card_w
    sard_w = int(sard_h * 0.72)
    cemetery = ((W >> 1) - int(card_w * 3.7), (H >> 1))
    deck = ((W >> 1) - int(card_w * 2.85), (H >> 1))
    rect_attack = pg.Rect((W >> 1) - (card_w << 1), (H >> 1) - sard_w, card_w << 2, sard_w)
    rect_floop = pg.Rect((W >> 1) - card_w * 2, (H >> 1) + card_h, card_w * 4, sard_w)
    btn_end = pg.Rect((sard_h >> 2, H - (sard_w >> 1)), (card_h, sard_h >> 2))
    size_rect_x = sard_w // 20 * 4.75 + (W >> 1)
    size_rect_y = sard_h // 7
    PLAYER_1 = Player(decks.pop(randint(-1, 1)))
    [PLAYER_1.land.add(Land(PLAYER_1.land_id[i], ((W >> 1) - card_w * (2 - i), (H >> 1)), (card_w, card_h), 0)) for i in
     range(4)]
    PLAYER_2 = Player(decks.pop(0))
    [PLAYER_2.land.add(
        Land(PLAYER_2.land_id[i], ((W >> 1) - card_w * (2 - i), (H >> 1) - card_h), (card_w, card_h), 180)) for i in
        range(4)]

    hp_pos = ((W >> 1) - int(card_w * 3.15), H - sard_w)
    action_pos = ((W >> 1) - int(card_w * 2.55), H - sard_w)

    bg = pg.transform.scale(pg.image.load("bg.png"), size)  # фон и атрибуты игры
    deck_card = pg.transform.scale(pg.image.load("cards/back.png"), (sard_w, sard_h))
    btn_deck = pg.Rect(*deck, sard_w, sard_h)
    # Расположение существ на полях
    rect_card = ([pg.Rect(size_rect_x + card_w * (1 - i), size_rect_y + (H >> 1), sard_w, sard_h) for i in range(4)],
                 [pg.Rect(size_rect_x + card_w * (1 - i), size_rect_y + sard_h + (H >> 1), sard_w, sard_h) for i in
                  range(4)])
    rect_card_2 = (
        [pg.Rect(size_rect_x + card_w * (1 - i), -size_rect_y + (H >> 1) - sard_h, sard_w, sard_h) for i in range(4)],
        [pg.Rect(size_rect_x + card_w * (1 - i), -size_rect_y - sard_h + (H >> 1) - sard_h, sard_w, sard_h) for i in
         range(4)])
    hand = pg.Surface((int(card_w * 1.6), int(card_h * 2.1)))
    hand_rect = pg.Rect((W >> 1) + int(card_w * 2.1), (H >> 1) - sard_h, *hand.get_size())
    win = None

    while not win and runGame:
        PLAYER_1, PLAYER_2 = PLAYER_2, PLAYER_1
        cards = PLAYER_1.cards
        play = PLAYER_1.active_cards
        cur = None

        cards_on_hand = PLAYER_1.hand
        slider = 0

        PLAYER_1.land = pg.sprite.Group()
        PLAYER_2.land = pg.sprite.Group()
        for i in range(4):
            PLAYER_1.land.add(
                Land(PLAYER_1.land_id[i], ((W >> 1) - card_w * (2 - i), (H >> 1)), (card_w, card_h), 0,
                     PLAYER_1.land_activ[i]))
            if PLAYER_1.active_cards[0][i]: PLAYER_1.active_cards[0][i].viev(rect_card[0][i])
            if PLAYER_1.active_cards[1][i]: PLAYER_1.active_cards[1][i].viev(rect_card[1][i])
            PLAYER_2.land.add(
                Land(PLAYER_2.land_id[i], ((W >> 1) - card_w * (2 - i), (H >> 1) - card_h), (card_w, card_h), 180,
                     PLAYER_2.land_activ[i]))
            if PLAYER_2.active_cards[0][i]: PLAYER_2.active_cards[0][i].viev(rect_card_2[0][i])
            if PLAYER_2.active_cards[1][i]: PLAYER_2.active_cards[1][i].viev(rect_card_2[1][i])
        timeee = True

        [a.location(n,
                    (hand_rect.x + int(sard_w * 0.125),
                     hand_rect.y + int(sard_w * 0.125)),
                    (sard_w, sard_h), slider) for n, a in enumerate(cards_on_hand)]

        for c in cards:
            if c and c.case != 0:
                c.case = 0
                c.status = 2
        for c in PLAYER_2.active_cards[0]:
            if c and c.case == 1:
                c.rect.w, c.rect.h = sard_h, sard_w
                c.image = pg.transform.rotate(c.image, 90)
                c.pos = (c.pos[0] - size_rect_x + (W >> 1), c.pos[1] + size_rect_y + sard_h - sard_w)
                c.zeroing()
            if c and c.case == 2:
                c.rect.w, c.rect.h = sard_h, sard_w
                c.image = pg.transform.rotate(c.image, 90)
                c.pos = (c.pos[0] - size_rect_x + (W >> 1), c.pos[1])
                c.zeroing()

        while runGame and timeee:
            screen.blit(bg, (0, 0))  # отрисововаем фон
            if len(PLAYER_1.pack):
                screen.blit(deck_card, deck)
            PLAYER_1.land.draw(screen)
            PLAYER_2.land.draw(screen)
            hand.fill((50, 0, 0))
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:  # выход из игры
                        runGame = False
                if event.type == pg.MOUSEBUTTONUP:
                    if event.button == 1:
                        if btn_end.collidepoint(pg.mouse.get_pos()):
                            timeee = False
                        if cur:
                            if cur.object < 2:
                                for i in range(4):
                                    if rect_card[cur.object][i].colliderect(cur.rect) and cur.status < 2:
                                        if play[cur.object][i]:
                                            # сброс
                                            play[cur.object][i].dead(cemetery)
                                        cur.set_land(rect_card[cur.object][i].copy())  # перемещаем карту
                                        cards.add(cur)
                                        play[cur.object][i] = cur
                                        cards_on_hand.remove(cur)
                                        [a.location(n,
                                                    (hand_rect.x + int(sard_w * 0.125),
                                                     hand_rect.y + int(sard_w * 0.125)),
                                                    (sard_w, sard_h), slider) for n, a in enumerate(cards_on_hand)]
                            if cur.object == 0 and rect_attack.colliderect(cur.rect):
                                cur.case = 1
                                cur.rect.w, cur.rect.h = sard_h, sard_w
                                cur.image = pg.transform.rotate(cur.image, 90)
                                cur.pos = (cur.pos[0] - size_rect_x + (W >> 1), cur.pos[1] - size_rect_y)
                                cur.status = 1
                            if cur.object == 0 and rect_floop.colliderect(cur.rect):
                                cur.case = 2
                                cur.rect.w, cur.rect.h = sard_h, sard_w
                                cur.image = pg.transform.rotate(cur.image, 90)
                                cur.pos = (cur.pos[0] - size_rect_x + (W >> 1), cur.pos[1] + sard_w * 0.4)
                                cur.status = 1

                            cur.zeroing()  # возращаем карту на место
                            cur = None
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pg.mouse.get_rel()  # обнуляем относительную позицию
                        if btn_deck.collidepoint(pg.mouse.get_pos()) and len(PLAYER_1.pack):
                            cards_on_hand.add((a := Card((sard_w, sard_h), PLAYER_1.pack.pop(0))))
                            a.location(len(cards_on_hand) - 1, (hand_rect.x + int(sard_w * 0.125),
                                                                hand_rect.y + int(sard_w * 0.125)), (sard_w, sard_h),
                                       slider)
                    if hand_rect.collidepoint(event.pos) and not cur:
                        if event.button == 4 and slider > 0:
                            [i.scroll(1) for i in cards_on_hand]
                            slider -= 1
                        if event.button == 5 and slider < (len(cards_on_hand) + 1 >> 1) * 4.1 - 12:
                            [i.scroll(-1) for i in cards_on_hand]
                            slider += 1
                if event.type == pg.MOUSEMOTION:
                    if event.buttons[0]:
                        if pg.Rect(*pg.mouse.get_pos(), 0, 0).collidelist(
                                a := sum([list(cards_on_hand), list(cards)], [])):
                            if not cur:
                                # сохраняем выбранную карту
                                cur = lis[0] if (lis := [c for c in a if c.rect.collidepoint(event.pos) and (
                                        hand_rect.collidepoint(pg.mouse.get_pos()) or c.status >= 2)]) != [] else None
                            if cur:
                                if cur.status == 0 or cur.status == 2:
                                    # перемещение карты
                                    cur.rect.move_ip(event.rel)
                                else:
                                    cur = None

            if cur and cur.status == 0 and cur.object < 2:
                surs = pg.Surface((sard_w, sard_h), pg.SRCALPHA)  # подсветка мест
                surs.fill((255, 255, 0, 127))
                [screen.blit(surs, i) for i in rect_card[cur.object]]
                [pg.draw.rect(screen, (255, 255, 0),
                              ((i.x - sard_w * 0.05, i.y - sard_w * 0.05), (sard_w * 1.1, sard_h + sard_w * 0.1)),
                              int(sard_w * 0.05)) for i in rect_card[cur.object]]

            pg.draw.circle(screen, (200, 0, 0), hp_pos, sard_h >> 2)
            pg.draw.circle(screen, (100, 0, 0), hp_pos, sard_h >> 2, 10)
            pg.draw.circle(screen, (0, 200, 0), action_pos, sard_h >> 2)
            pg.draw.circle(screen, (0, 100, 0), action_pos, sard_h >> 2, 10)
            pg.draw.rect(screen, (100, 0, 0), btn_end)

            cards.draw(screen)  # отрисововаем карты
            PLAYER_2.cards.draw(screen)
            [i.drawing(hand, (hand_rect.x, hand_rect.y)) for i in cards_on_hand]
            screen.blit(hand, hand_rect)
            if cur:
                screen.blit(cur.image, cur.rect)
            if pg.key.get_pressed()[pg.K_LALT]:
                [screen.blit(card.alt(pg.image.load(f'cards/{card.id}.png'), (card_w * 3, H)),
                             pg.Rect((W >> 1) - card_w * 1.5, 0, card_w * 3, H)) for card in cards
                 if card.rect.collidepoint(pg.mouse.get_pos())]
                [screen.blit(card.alt(pg.image.load(f'cards/{card.id}.png'), (card_w * 3, H)),
                             pg.Rect((W >> 1) - card_w * 1.5, 0, card_w * 3, H)) for card in cards_on_hand
                 if card.rect.collidepoint(pg.mouse.get_pos())]
                [screen.blit(card.alt(pg.image.load(f'cards/{card.id}.png'), (card_w * 3, H)),
                             pg.Rect((W >> 1) - card_w * 1.5, 0, card_w * 3, H)) for card in PLAYER_2.cards
                 if card.rect.collidepoint(pg.mouse.get_pos())]
            pg.display.update()
        for c in sum(map(list, (PLAYER_2.active_cards[0], cards)), []):
            if c and c.case != 0:
                c.image = pg.transform.rotate(c.image, -90)
