import random
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import LineString

dataPoints = []

def AddToData(time, particles):
    dataPoints.append([time, particles])

def mainLoop(particleCount):
    count = 0
    currentParticles = particleCount
    AddToData(count, currentParticles)
    while currentParticles != 0:
        count += 1
        tempParticleCount = currentParticles
        for i in range(tempParticleCount):
            randVal = random.randint(1,6)
            if (randVal == 1):
                currentParticles = currentParticles - 1
        AddToData(count, currentParticles)

def plot(data):
    xpoints = np.array([])
    ypoints = np.array([])

    for i in range(len(data)):
        xpoints = np.append(xpoints, [data[i][0]])
        ypoints = np.append(ypoints, [data[i][1]])

    plt.plot(xpoints, ypoints, 'g')

    xMax = data[-1][0]
    yMax = data[0][1]

    for i in range(3):
        plt.plot([0, xMax], [yMax/2**(i+1), yMax/2**(i+1)], 'r')

    firstLine = LineString(np.column_stack((xpoints, ypoints)))
    intersectionLines = []
    intersections = []

    for x in range(3):
        intersectionLines.append(LineString(np.column_stack(([0, xMax], [yMax/(2**(x+1)), yMax/(2**(x+1))]))))
        intersections.append(intersectionLines[x].intersection(firstLine))

    intersectionPoints = []
    halfLifeTime = 0

    for x in range(len(intersections)):
        if intersections[x].geom_type == 'Point':
            plt.plot(*intersections[x].xy, 'o')
            intersectionPoints.append([*intersections[x].xy[0], *intersections[x].xy[1]])

    for i in range(len(intersectionPoints)):
        x,y  = intersectionPoints[i][0], intersectionPoints[i][1]
        plt.text(x+1, y+(yMax/100), f"{round(x, 3)}, {int(y)}")
        if ((i - 1) != -1):
            timeBetweenPoints = intersectionPoints[len(intersectionPoints) - i][0] - intersectionPoints[len(intersectionPoints) - i - 1][0]
        else:
            timeBetweenPoints = intersectionPoints[0][0]
        halfLifeTime += timeBetweenPoints

    halfLifeAvg = round((halfLifeTime / (len(intersections))), 3)

    plt.ylabel("Particles Remaining")
    plt.xlabel("Time")

    plt.grid()
    plt.suptitle("Radioactive decay graph")
    plt.title(f"Average half life is: {halfLifeAvg}")
    plt.show()

if __name__ == '__main__':
    particleValue = int(input("How many particles do you want to start with: "))
    mainLoop(particleValue)
    plot(dataPoints)