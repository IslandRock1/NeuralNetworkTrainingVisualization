
import pygame as pg
import pygame.freetype as freetype

from NeuralNetwork import NeuralNetwork

class Visualizer:
    def __init__(self):
        
        if not pg.get_init(): pg.init()
        if not freetype.get_init(): freetype.init()
        self.font = freetype.SysFont('Comic Sans MS', 15)

    def get_rect(self, neuralNetwork: NeuralNetwork, rect_size: tuple):
        width, height = rect_size

        surf = pg.surface.Surface(rect_size)
        surf.set_colorkey((0, 0, 0))

        textOffset = 5

        numLayers = len(neuralNetwork.layers)

        startX = width * 0.1
        deltaX = (width * 0.8) / (numLayers - 1)

        for ix, layer in enumerate(neuralNetwork.layers):
            numNodes = len(layer.nodes)
            
            startY = height * 0.1

            if numNodes > 1:
                deltaY = (height * 0.8) / (numNodes - 1)
            else:
                deltaY = 0
                startY = height * 0.5

            for ixNodes in range(numNodes):

                xPos = startX + deltaX * ix
                yPos = startY + deltaY * ixNodes

                pg.draw.circle(surf, (0, 128, 0), (xPos, yPos), (height / 50))
                
                text = str(round(neuralNetwork.layers[ix].nodes[ixNodes].value, 3))
                self.font.render_to(surf, (xPos- textOffset, yPos - textOffset), text, (255, 255, 255))
        
        return surf
    
