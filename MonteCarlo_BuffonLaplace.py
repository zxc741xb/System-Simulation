import random, numpy, math
def throwNeedles(numNeedles):
    inCircle = 0
    for needles in range(1, numNeedles+1, 1):
        x = random.random()
        y = random.random()
        if math.sqrt(x*x + y*y) <= 1.0:
            inCircle += 1
    return 4*(inCircle/float(numNeedles)) # 4 is the area of the square

def getEst(numNeedles, numTrials):
    estimates = []
    for t in range(numTrials):
        piGuess = throwNeedles(numNeedles)
        estimates.append(piGuess)
    sDev = numpy.std(estimates) # deviation of estimation
    curEst = sum(estimates) / len(estimates) # average of estimation
    print('Est. = ' + str(curEst) + ', standard dev. = ' + str(round(sDev, 6)) + ', Needles = ' + str(numNeedles))
    return (curEst, sDev)

def estPi(precision, numTrials):
    '''precision is the acceptable bias, we set the confidence level for 95%'''
    numNeedles = 1000
    sDev = precision
    while sDev >= precision/1.96:
        curEst, sDev = getEst(numNeedles, numTrials)
        numNeedles *= 2
    return curEst

estPi(0.95, 1000)
estPi(0.95, 2000)
estPi(0.95, 10000) 