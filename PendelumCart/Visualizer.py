
from math import sin, cos

import pygame as pg
import pygame.freetype as freetype

from .PendelSimulation import PendelSimulation

class Visualizer:
    def __init__(self):
        
        if not pg.get_init(): pg.init()
        if not freetype.get_init(): freetype.init()
        self.font = freetype.SysFont('Comic Sans MS', 15)
    
    def renderBackgroundDots(self, xOffset):
        y_pos = [(50 * x) % (self.rect_size[1] * 2) for x in range(0, 11)]
        x_pos = [(50 * x - xOffset) % (self.rect_size[0] * 2) for x in range(-20, 20)]

        for y in y_pos:
            for x in x_pos:
                off = 300
                if (79900 + off) < abs(x + xOffset) < (80000 + off):
                    col = (0, 255, 0)
                
                elif abs(x + xOffset) > (79950 + off):
                    col = (255, 0, 0)

                else:
                    col = (100, 100, 100)

                off = -1000
                if (79900 + off) < abs(x + xOffset) < (80000 + off):
                    col = (0, 255, 0)

                elif abs(x + xOffset) < (79950 + off):
                    col = (255, 0, 0)


                off = -350
                if (79900 + off) < abs(x + xOffset) < (80000 + off):
                    col = (0, 0, 255)

                pg.draw.circle(self.surf, col, (x, y), 5)

    def renderCart(self):
        cartPos = self.rect_size[0] / 2
        cartWidth = self.rect_size[0] / 16
        cartHeight = self.rect_size[1] / 16

        c0 = (cartPos - cartWidth, self.rect_size[1] / 2 - cartHeight)
        c1 = (cartPos + cartWidth, self.rect_size[1] / 2 - cartHeight)
        c2 = (cartPos + cartWidth, self.rect_size[1] / 2 + cartHeight)
        c3 = (cartPos - cartWidth, self.rect_size[1] / 2 + cartHeight)

        pg.draw.lines(self.surf, (255, 255, 255), True, [c0, c1, c2, c3], width=5)

    def renderPendel(self, xOffset):
        px = -200.0 * sin(self.sys.rotationPos)
        py = -200.0 * cos(self.sys.rotationPos)

        pendelPos = (px + self.rect_size[0] / 2, py + self.rect_size[1] / 2)

        pg.draw.aaline(self.surf, (255, 255, 255), (self.rect_size[0] / 2, self.rect_size[1] / 2), pendelPos)

        pg.draw.circle(self.surf, (255, 255, 255), pendelPos, 4)

    def get_surf(self, system: PendelSimulation, rect_size: tuple):
        self.sys = system
        self.rect_size = rect_size

        self.surf = pg.surface.Surface(rect_size)
        self.surf.set_colorkey((0, 0, 0))

        xOffset = (self.sys.cartPos - self.rect_size[0] / 2) * 200.0
        
        self.renderBackgroundDots(xOffset)
        self.renderCart()
        self.renderPendel(xOffset)

        return self.surf