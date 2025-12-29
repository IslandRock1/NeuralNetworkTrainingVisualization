
import time

import pygame as pg
import pygame.freetype as freetype
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, K_LEFT, K_RIGHT, K_UP, K_DOWN
from dataclasses import dataclass

from Pygame.Slider import Slider, SliderArgs
from Pygame.ToggleButton import ToggleButton, ToggleButtonArgs
from Pygame.TextBox import TextBox, TextBoxArgs
from Pygame.ColorPicker import ColorPicker, ColorPickerArgs
from Pygame.Plot import Plot, PlotArgs

from TrainingLib import TrainingLib, ProjectType

pg.init()
freetype.init()

@dataclass
class Args:
    clock: pg.time.Clock = None
    cpu_time: list[float] = None
    iters: int = 0
    fps: float = 60.0
    screenShotNum : int = 0
    running : bool = True

    bgColor : tuple = (50, 30, 60)

    trainingLib: TrainingLib = None
    screen: pg.Surface = None

def init_args():
    args = Args()
    args.clock = pg.time.Clock()
    args.cpu_time = []
    args.trainingLib = TrainingLib(ProjectType.PendelumCart)

    width, height = 1600, 800
    args.screen = pg.display.set_mode((width, height), pg.RESIZABLE)
    pg.display.set_caption("Title")

    third = 0.33333
    args.testConsts = [1.0, 1.0, 1.0, 1.0]
    args.UIElements = [
        Plot(PlotArgs(pg.Rect(0, 0, int(width * 0.8), int(height * third) - 3), id="plotBest", y_label="Reward", title="Best score")),
        Plot(PlotArgs(pg.Rect(0, int(height * third) + 3, int(width * 0.8), int(height * third) - 3), id="plotAvg", y_label="Reward", title="Average score")),
        Plot(PlotArgs(pg.Rect(0, int(2 * height * third) + 3, int(width * 0.8), int(height * third) - 3), id="plotIterTime", y_label="Time (ms)", title="Iteration Time")),

        TextBox(TextBoxArgs(pg.Rect(int(width * 0.85), int(height * 0.03), 200, 50), id="textBox0",
                            text=str(args.testConsts))),
        Slider(SliderArgs(pg.Rect(int(width * 0.85), int(height * 0.1), 200, 50), id="slider0", minVal=0.0, maxVal=10.0,
                          currentVal=1.0)),
        Slider(SliderArgs(pg.Rect(int(width * 0.85), int(height * 0.17), 200, 50), id="slider1", minVal=-10.0, maxVal=0.0,
                          currentVal=-1.0)),
        Slider(SliderArgs(pg.Rect(int(width * 0.85), int(height * 0.24), 200, 50), id="slider2", minVal=-10.0, maxVal=0.0,
                          currentVal=-1.0)),
        Slider(SliderArgs(pg.Rect(int(width * 0.85), int(height * 0.31), 200, 50), id="slider3", minVal=-10.0, maxVal=0.0,
                          currentVal=-1.0)),

        TextBox(TextBoxArgs(pg.Rect(int(width * 0.94), int(height * 0.97), 90, 20), id="textBoxFPS",
                            text=str(args.testConsts)))
    ]

    for i in range(10):
        rect = pg.Rect(int(width * 0.81), int(height * (0.4 + 0.05 * i)), 300, 30)
        txBox = TextBox(TextBoxArgs(rect, f"textBox{i + 1}"))
        args.UIElements.append(txBox)

    for uiEl in args.UIElements:
        if (uiEl.getId() == "plotIterTime"):
            uiEl.setBounds(y_low=0.0, y_high=20)

    return args

def render_func(args: Args):
    args.screen.fill(args.bgColor)

    for uiElement in args.UIElements:
        args.screen.blit(uiElement.getSurf(args.bgColor), uiElement.getPos())

        dx, dy = uiElement.getPos()
        secondaries = uiElement.getSecondaryElements()
        for secondary in secondaries:
            x, y = secondary.getPos()
            args.screen.blit(secondary.getSurf(args.bgColor), (x + dx, y + dy))

    pg.display.flip()
    # pg.image.save(screen, rf"screenshots\screenshotVisualization{args.screenShotNum}.png")
    # args.screenShotNum += 1

def step(args: Args):
    if (not args.running): args.trainingLib.stopFlag = True

    trainingOutput = args.trainingLib.getStats()
    trainingInput = {}
    trainingInput["testConsts"] = args.testConsts
    args.trainingLib.setInfo(trainingInput)

    if (len(args.cpu_time) != 0):
        cpuTimeThingy = 1000 * sum(args.cpu_time) / len(args.cpu_time)
    else: cpuTimeThingy = 0.0

    for uiElement in args.UIElements:
        if (uiElement.getId() == "slider0"):
            args.testConsts[0] = uiElement.getValue()

        elif (uiElement.getId() == "slider1"):
            args.testConsts[1] = uiElement.getValue()

        elif (uiElement.getId() == "slider2"):
            args.testConsts[2] = uiElement.getValue()

        elif (uiElement.getId() == "slider3"):
            args.testConsts[3] = uiElement.getValue()

        elif (uiElement.getId() == "textBox0"):
            uiElement.changeText(f"{[round(x, 1) for x in args.testConsts]}")

        elif (uiElement.getId() == "textBoxFPS"):
            uiElement.changeText(f"{cpuTimeThingy:.2f} ms")

        elif (uiElement.getId() == "plotBest"):
            uiElement.setValues([x for x in range(len(trainingOutput["bestScores"]))], trainingOutput["bestScores"])

        elif (uiElement.getId() == "plotAvg"):
            uiElement.setValues([x for x in range(len(trainingOutput["avgScores"]))], trainingOutput["avgScores"])

        elif (uiElement.getId() == "plotIterTime"):
            x_vals = [x for x in range(len(args.cpu_time))]
            y_vals = [1000 * y for y in args.cpu_time]
            uiElement.setValues(x_vals, y_vals, debug=True)

        for i in range(10):
            if (uiElement.getId() == f"textBox{i + 1}"):
                if (len(trainingOutput["avgScores"]) > i):
                    avg = trainingOutput["avgScores"][-(i + 1)]
                    best = trainingOutput["bestScores"][-(i + 1)]
                    uiElement.changeText(f"Best: {best:.3e} | Avg: {avg:.3e}")

def handleMouse(args: Args):
    pressed = pg.mouse.get_pressed()
    pos = pg.mouse.get_pos()

    for uiElement in args.UIElements:
        uiElement.update(pressed, pos)


def handleKeyboard(args: Args):
    for event in pg.event.get():
        if event.type == QUIT:
            args.running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                args.running = False

            elif event.key == pg.K_s:
                pg.image.save(args.screen, rf"screenshots\screenshotVisualization{args.screenShotNum}.png")
                args.screenShotNum += 1

def runProgram():
    args = init_args()
    while args.running:
        args.iters += 1
        args.clock.tick(args.fps)

        t0 = time.perf_counter()
        handleKeyboard(args)
        handleMouse(args)
        step(args)
        render_func(args)
        t1 = time.perf_counter()
        args.cpu_time.append(t1 - t0)
        if (len(args.cpu_time) > 101):
            args.cpu_time.pop(0)

if __name__ == "__main__":
    runProgram()

    # TODO: implement a way to save training (probably every iteration?)
    # Then obviously implement a way to continue training..