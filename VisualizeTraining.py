
import time

isHeadless = False
if (not isHeadless):
    import pg_widgets as pw

from NeuralNetworkPython import PythonToCPP, CPPToPython, TrainingLib

def getPythonToCPP():
    pythonToCPP = PythonToCPP()
    pythonToCPP.projectName = "MNIST"

    pythonToCPP.hiddenLayerSize = [128, 128]
    pythonToCPP.activationFunctions = [2, 2, 5]

    pythonToCPP.networksPerIter = 200
    pythonToCPP.numSimulations = 1
    pythonToCPP.simTime = 50.0

    pythonToCPP.percentNetworksKept = 0.06
    pythonToCPP.percentNetworksNew = 0.2
    pythonToCPP.percentNetworksModifiable = 0.3

    pythonToCPP.percentChangeFunction = 0.0
    pythonToCPP.percentChangeBias = 0.01
    pythonToCPP.percentChangeWeight = 0.99

    pythonToCPP.numChanges = 1
    pythonToCPP.temperature = 1.0
    pythonToCPP.constValues = [1.0, 0.0, 0.0, 0.0]

    return pythonToCPP

def getControlManager():

    controlManager = pw.ControlManager()

    left = pw.UIGroup((0, 0), (0.6, 1.0))
    left["plotValidation"] = pw.Plot.inBorder((0.0, 0.0), (1.0, 0.3))
    left["plotValidation"].setTitle("Validation Score")
    left["plotValidation"].setXLabel("Iteration")
    left["plotValidation"].setYLabel("Score")

    left["plotBest"] = pw.Plot.inBorder((0.0, 0.3), (1.0, 0.3))
    left["plotBest"].setTitle("Best Score")
    left["plotBest"].setXLabel("Iteration")
    left["plotBest"].setYLabel("Score")

    left["plotAvg"] = pw.Plot.inBorder((0.0, 0.6), (1.0, 0.3))
    left["plotAvg"].setTitle("Average Score")
    left["plotAvg"].setXLabel("Iteration")
    left["plotAvg"].setYLabel("Score")

    left["progressBar"] = pw.ProgressBar.inBorder((0.0, 0.9), (1.0, 0.1))

    right = pw.UIGroup((0.6, 0), (0.4, 1.0))
    right["iterationText"] = pw.TextBox.inBorder((0.0, 0.0), (0.8, 0.1))
    right["iterationText"].setText("Iteration: xx")

    right["fpsText"] = pw.TextBox.inBorder((0.8, 0.0), (0.2, 0.1))
    right["fpsText"].setText("FPS: xx")

    right["totalTrainingTime"] = pw.TextBox.inBorder((0.0, 0.1), (1.0, 0.1))
    right["totalTrainingTime"].setText("Total Training Time: xx")

    right["textNumChanges"] = pw.TextBox.inBorder((0.0, 0.2), (0.5, 0.1))
    right["textTemperature"] = pw.TextBox.inBorder((0.5, 0.2), (0.5, 0.1))
    right["sliderNumChanges"] = pw.Slider.inBorder((0.0, 0.3), (0.5, 0.7))
    right["sliderTemperature"] = pw.Slider.inBorder((0.5, 0.3), (0.5, 0.7))
    right["sliderNumChanges"].changeValues(1, 10000, 5000)
    right["sliderTemperature"].changeValues(0.0, 1.0, 0.1)

    tab1 = pw.UIGroup((0, 0), (1.0, 1.0))
    tab1["left"] = left
    tab1["right"] = right

    # controlManager["tabs"] = pw.Tab((0, 0), uiElements = [tab1])
    controlManager["left"] = left
    controlManager["right"] = right

    return controlManager

def step():
    pass

def format_time(seconds: float) -> str:
    """
    Formats a time value (in seconds) into a human-readable string.
    - < 1 ms: shows in µs
    - < 1 s: shows in ms
    - < 60 s: shows in seconds with 2 decimals
    - >= 60 s: shows as minutes:seconds
    """
    if seconds < 0:
        raise ValueError("Time cannot be negative")

    if seconds < 0.001:  # less than 1 ms → microseconds
        return f"{seconds * 1e6:.1f} µs"
    elif seconds < 1:  # less than 1 second → milliseconds
        return f"{seconds * 1000:.1f} ms"
    elif seconds < 60:  # less than 1 minute → seconds
        return f"{seconds:.2f} s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        sec = int(seconds % 60)
        return f"{minutes}:{sec:02d}"

    else:
        hours = int(seconds // 3600)
        minutes = int(seconds % 3600) // 60
        sec = int(seconds % 3600) % 60
        return f"{hours}:{minutes:02d}:{sec:02d}"

def runProgram():

    pythonToCPP = getPythonToCPP()
    trainingLib = TrainingLib(pythonToCPP)
    trainingStartTime = time.perf_counter()

    if (not isHeadless):
        controlManager = getControlManager()

    prevNetworkIteration = 0
    while True:
        if (not isHeadless):
            if (not controlManager.isRunning()): break
            controlManager.update()
        trainingInfo = trainingLib.getInfo()

        numChanges = 5000
        temperature = 0.1
        if (not isHeadless):
            y_valuesAvg = trainingInfo.avgScores
            y_valuesBest = trainingInfo.bestScores
            y_valuesValidation = trainingInfo.validationScores
            x_values = [x for x in range(len(y_valuesBest))]

            controlManager["plotValidation"].setValue(x_values, y_valuesValidation, maxLength = 1000)
            controlManager["plotBest"].setValue(x_values, y_valuesBest, maxLength = 1000)
            controlManager["plotAvg"].setValue(x_values, y_valuesAvg, maxLength = 1000)
            controlManager["progressBar"].setValue(trainingInfo.finishedNetworksThisIter / pythonToCPP.networksPerIter)

            controlManager["iterationText"].setText(f"Iteration: {trainingInfo.finishedIterations}")
            controlManager["fpsText"].setText(f"FPS: {1.0 / controlManager.getRenderTime():.2f}")
            controlManager["totalTrainingTime"].setText(f"Total Training Time: {format_time(time.perf_counter() - trainingStartTime)}")

            numChanges = int(controlManager["sliderNumChanges"].getValue())
            temperature = controlManager["sliderTemperature"].getValue()
            controlManager["textNumChanges"].setText(f"Num changes: {numChanges}")
            controlManager["textTemperature"].setText(f"Temperature: {temperature:.5f}")

            if (trainingInfo.finishedIterations > prevNetworkIteration):
                prevNetworkIteration = trainingInfo.finishedIterations
                controlManager["sliderTemperature"].changeValues(-5, 5, temperature * 0.9999)

        pythonToCPP.numChanges = numChanges
        pythonToCPP.temperature = temperature
        trainingLib.setInfo(pythonToCPP)

        if (isHeadless):
            time.sleep(1.0)


    trainingLib.stop()

if __name__ == "__main__":
    runProgram()