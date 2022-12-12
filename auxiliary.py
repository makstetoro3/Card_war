from pygame.mouse import get_pos


class Button:
    def __init__(self, rect, function):
        self.rect = rect
        self.func = function

    def pressed(self, *args):
        if self.rect.collidepoint(*get_pos()):
            return self.func(*args)
