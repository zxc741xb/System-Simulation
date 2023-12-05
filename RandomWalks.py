import math
import random
from matplotlib import pylab as plt

class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def move(self, deltaX, deltaY):
        # retunn location which after moving
        return Location(self.x + deltaX, self.y + deltaY)
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def distFrom(self, other):
        # calculate distance from other location
        ox = other.x
        oy = other.y
        xDist = self.x - ox
        yDist = self.y - oy
        return math.sqrt(xDist**2 + yDist**2)
    
    def __str__(self):
        return '<' + str(self.x) + ',' + str(self.y) + '>'
    
class Field:
    # record drunks moving space
    def __init__(self):
        self.drunks = {}

    def addDrunk(self, drunk, loc):
        if drunk in self.drunks:
            raise ValueError('Duplicate drunk')
        self.drunks[drunk] = loc
        
    def getLoc(self, drunk):
        if drunk not in self.drunks:
            raise ValueError('Drunk is not in the field')
        return self.drunks[drunk]
        
    def moveDrunk(self, drunk):
        if drunk not in self.drunks:
            raise ValueError('Drunk is not in the field')
        xDist, yDist = drunk.takeStep()
        currentLocation = self.drunks[drunk]
        self.drunks[drunk] = currentLocation.move(xDist, yDist)
        
class Drunk:
    def __init__(self, name = None):
        self.name = name
    def __str__(self):
        return 'This drunk is named ' + self.name

class UsualDrunk(Drunk):
    def takeStep(self):
        stepChoices = [(0.0, 1.0), (0.0, -1.0), (1.0, 0.0), (-1.0, 0.0)]
        return random.choice(stepChoices)
    
class ColdDrunk(Drunk):
    def takeStep(self):
        stepChoices = [(0.0, 0.9), (0.0, -1.1), (1.0, 0.0), (-1.0, 0.0)]
        return random.choice(stepChoices)

def walk(field, drunk, numSteps):
    """return the distance between final and beginning location"""
    start = field.getLoc(drunk)
    for s in range(numSteps):
        field.moveDrunk(drunk)
    return start.distFrom(field.getLoc(drunk))

def simWalks(numSteps, numTrials, dClass):
    """dclass is a subclass of Drunks, simulating numTrials walks of numSteps each.
       Returns a list of final distance of each trial"""
    Homer = dClass()
    start = Location(0 ,0)
    distances = []
    for t in range(numTrials):
        f = Field()
        f.addDrunk(Homer, start)
        distances.append(round(walk(f, Homer, numSteps), 1))
    return distances

def drunkTest(walkLengths, numTrials, dClass):
    """For each number of steps in walkLengths, runs simWalks with numTrials walks and print result"""
    for numSteps in walkLengths:
        distances = simWalks(numSteps, numTrials, dClass)
        print(dClass.__name__, 'random walk of', numSteps, 'steps')
        print(' Mean =', round(sum(distances)/len(distances), 4))
        print(' Max =', max(distances), ' Min =', min(distances))


# random.seed(0)
# drunkTest((10,100,1000,10000), 100, UsualDrunk)

# Sanity check
# drunkTest((0,1,2), 100, UsualDrunk)

def simAll(drunkKinds, walkLenghs, numTrials):
    for dClass in drunkKinds:
        drunkTest(walkLenghs, numTrials, dClass)

# simAll((UsualDrunk, ColdDrunk), (1,10,100,1000,10000), 100)

# Visualization
class styleIterator(object):
    def __init__(self, styles):
        self.index = 0
        self.styles = styles
    
    def nextStyle(self):
        # encoding style index of drunk
        result = self.styles[self.index]
        if self.index == len(self.styles)-1:
            self.index = 0
        else:
            self.index += 1
        return result
    
def simDrunk(numTrials, dClass, walkLengths):
    meanDistance = []
    for numSteps in walkLengths:
        print('Starting sumulation of', numSteps, 'steps')
        trials = simWalks(numSteps, numTrials, dClass)
        mean = sum(trials)/len(trials)
        meanDistance.append(mean)
    return meanDistance
    
def simAll2(drunkKinds, walkLengths, numTrials):
    styleChoices = styleIterator(('m--', 'b--', 'g-.'))
    for dClass in drunkKinds:
        curStyle = styleChoices.nextStyle()
        print('Starting simulation of', dClass.__name__)
        means = simDrunk(numTrials, dClass, walkLengths)
        plt.plot(walkLengths, means, curStyle, label = dClass.__name__)
    plt.title('Mean Distance from Origin (' + str(numTrials) + ' trials)')
    plt.xlabel('Number of steps')
    plt.ylabel('Distance from origin')
    plt.legend(loc = 'best')

# numSteps = (10,100,1000,10000)
# simAll2((UsualDrunk, ColdDrunk), numSteps, 100)


def getFinalLocs(numSteps, numTrials, dClass):
    locs = []
    d = dClass()
    for t in range(numTrials):
        f = Field()
        f.addDrunk(d, Location(0,0))
        for s in range(numSteps):
            f.moveDrunk(d)
        locs.append(f.getLoc(d))
    return locs

def plotLocs(drunkKinds, numSteps, numTrials):
    styleChoices = styleIterator(('k+', 'r^', 'mo'))
    for dClass in drunkKinds:
        locs = getFinalLocs(numSteps, numTrials, dClass)
        xVals, yVals = [], []
        for l in locs:
            xVals.append(l.getX())
            yVals.append(l.getY())
        xVals = plt.array(xVals)
        yVals = plt.array(yVals)
        meanX = sum(abs(xVals))/float(len(xVals))
        meanY = sum(abs(yVals))/float(len(yVals))
        curStyle = styleChoices.nextStyle()
        plt.plot(xVals, yVals, curStyle, label = dClass.__name__ + ' mean abs dist = <' + str(meanX) + ', ' + str(meanY) + '>')
    plt.title('Location at end of walks (' + str(numSteps) + ' steps)')
    plt.xlabel('Steps East/West of origin')
    plt.ylabel('Steps North/South of origin')
    plt.legend(loc = 'best')

plotLocs((UsualDrunk, ColdDrunk), 10000, 100)

