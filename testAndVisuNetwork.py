

from NeuralNetwork.NeuralNetwork import NeuralNetwork, loadNetwork
from NeuralNetwork.Visualizer import Visualizer as NetworkVisualizer

import pygame as pg
import pygame.freetype as freetype
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, K_LEFT, K_RIGHT, K_UP, K_DOWN
from dataclasses import dataclass
from SelfMadeLibraries.Timer import Stopwatch

from SelfMadeLibraries.Plot import renderPlot

testProject = "PendelumCart"
match testProject:
    case "PendelumCart":
        from PendelumCart.Visualizer import Visualizer as SystemVisualizer
        from PendelumCart.test import testControlAlgorithm
        pathString = "PendelumCart"

pg.init()
freetype.init()


@dataclass
class Args:
    tester: testControlAlgorithm
    stopWatch: Stopwatch
    clock: pg.time.Clock
    nn: NeuralNetwork
    visualizerNetwork: NetworkVisualizer
    visualizerSystem: SystemVisualizer

    iters: int = 0
    simulationSpeed: float = 1.0
    force: float = 0.0
    forceConstant: float = 1.0
    externalForce: float = 0.0

    sumReward = 0
    sumTime = 0

    fps: float = 60.0
    controller: bool = False

    timeSteps = []
    angleSteps = []
    positionSteps = []

    myFont = freetype.SysFont('Comic Sans MS', 20)
    screenShotNum : int = 0

def init_args(networkPath):
    args = Args

    args.tester = testControlAlgorithm()

    args.stopWatch = Stopwatch()
    args.clock = pg.time.Clock()

    args.nn = loadNetwork(networkPath)
    
    args.visualizerNetwork = NetworkVisualizer()
    args.visualizerSystem = SystemVisualizer()

    return args

def renderPlotLocal(screen, args: Args):
    
    if len(args.timeSteps) < 5:
        return

    while args.timeSteps[-1] - args.timeSteps[0] > 10:
        args.timeSteps.pop(0)
        args.angleSteps.pop(0)
        args.positionSteps.pop(0)

    plotArgs = {}
    plotArgs["x_values"] = args.timeSteps[::3]
    plotArgs["y_values"] = args.angleSteps[::3]
    plotArgs["fontSize"] = 10

    surf = renderPlot((400, 200), plotArgs)
    screen.blit(surf, (10, 10))
    args.myFont.render_to(screen, (175, 10), "Angle data", (255, 255, 255))


    plotArgs = {}
    plotArgs["x_values"] = args.timeSteps[::3]
    plotArgs["y_values"] = args.positionSteps[::3]
    plotArgs["fontSize"] = 10

    surf = renderPlot((400, 200), plotArgs)
    screen.blit(surf, (10, 210))
    args.myFont.render_to(screen, (175, 210), "Position data", (255, 255, 255))
    
    
    return

def getNumberAndUnit(value):

    abV = abs(value)
    if abV < 0.001:
        err = value * 1_000_000.0
        prefix = "u"

    elif abV < 1:
        err = value * 1_000.0
        prefix = "m"
    
    elif abV < 1000:
        err = value
        prefix = ""
    
    elif abV < 1_000_000:
        err = value / 1_000.0
        prefix = "k"

    else:
        err = value / 1_000_000.0
        prefix = "M"

    return err, prefix

def writeStats(screen, args: Args):
    WHITE = (255, 255, 255)

    stats = []

    stats.append(f"Frame: {args.iters}")
    stats.append(f"FPS: {round(args.clock.get_fps(), 3)}")

    err, prefix = getNumberAndUnit(args.externalForce)
    stats.append(f"External force: {round(err, 3)} {prefix + "N"}")

    err, prefix = getNumberAndUnit(args.tester.system.rotationPos)
    stats.append(f"Error: {round(err, 3)} {prefix + "θ"}")

    err, prefix = getNumberAndUnit(args.tester.system.cartPos)
    stats.append(f"Cart pos: {round(err, 3)} {prefix + "m"}")

    err, prefix = getNumberAndUnit(args.tester.system.cartVel)
    stats.append(f"Cart vel: {round(err, 3)} {prefix + "m/s"}")
    stats.append(f"Reward: {round(args.sumReward, 3)}")
    stats.append(f"Sumtime: {round(args.sumTime, 3)}")
    
    for ix, stat in enumerate(stats):
        args.myFont.render_to(screen, (30, 500 + 25 * ix), stat, WHITE)

def renderSimulation(screen, args):
    surf = args.visualizerSystem.get_surf(args.tester.system, (800, 400))
    screen.blit(surf, (400, 400))

def render_network(screen: pg.Surface, args: Args):
    surf = args.visualizerNetwork.get_rect(args.nn, (400, 300))
    screen.blit(surf, (800, 0))

def render_func(screen, args: Args):
    screen.fill((0, 0, 0))

    renderSimulation(screen, args)
    render_network(screen, args)
    
    renderPlotLocal(screen, args)
    writeStats(screen, args)

    pg.display.flip()

    # pg.image.save(screen, rf"screenshots\screenshotVisualization{args.screenShotNum}.png")
    # args.screenShotNum += 1

def step(args: Args):
    
    if args.controller:
        keys = pg.key.get_pressed()
        
        kl = keys[K_LEFT]
        kr = keys[K_RIGHT]
        
        if (kl and kr): args.force = 0
        elif kl: args.force = -0.8
        elif kr: args.force = 0.8
        else: args.force = 0

        externalForce = [args.force * args.forceConstant]
    else:
        info = args.tester.getInfo()
        outputSignals = args.nn.compute(info)
        externalForce = outputSignals

    args.externalForce = externalForce[0]
    _, reward, _ = args.tester.update(externalForce, [1.0, 0.0, 0.0, 0.0])

    args.positionSteps.append(args.tester.system.cartPos)
    args.angleSteps.append(args.tester.system.rotationPos)
    args.timeSteps.append(args.stopWatch.getTime())

    args.sumReward = reward
    args.sumTime += 1 / 60.0

def runProgram():
    width, height = 1600, 800
    screen = pg.display.set_mode((width, height), pg.RESIZABLE)
    pg.display.set_caption("Pendelum Simulation")

    running = True

    networkName = 65
    pathString = rf"PendelumCart\models\{networkName}.txt"
    args = init_args(pathString)
    while running:
        args.iters += 1
        args.clock.tick(args.fps)
        for event in pg.event.get():
            if event.type == QUIT: running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE: running = False
                
                elif event.key == K_UP:
                    args.fps += 10
                
                elif event.key == K_DOWN:
                    args.fps -= 10
                
                elif event.key == pg.K_p:
                    args.controller = not args.controller
                
                elif event.key == pg.K_s:
                    pg.image.save(screen, rf"screenshots\screenshotVisualization{args.screenShotNum}.png")
                    args.screenShotNum += 1


        if args.iters > 100:
            step(args)

        render_func(screen, args)

if __name__ == "__main__":
    runProgram()