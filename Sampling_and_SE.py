import random
import numpy as np
import pylab
import matplotlib.pyplot as plt

def getDiffs(population, sampleSizes):
    popstd = np.std(population)
    diffsFracs = []
    for sampleSize in sampleSizes:
        diffs = []
        for t in range(100):
            sample = random.sample(population, sampleSize)
            diffs.append(abs(popstd - np.std(sample)))
        diffMean = sum(diffs)/len(diffs)
        diffsFracs.append(diffMean/popstd)
    return pylab.array(diffsFracs)*100

def plotDiffs(sampleSizes, diffs, title, label):
    pylab.plot(sampleSizes, diffs, label=label)
    pylab.xlabel('Sample size')
    pylab.ylabel('% Difference in SD')
    pylab.title(title)
    pylab.legend()

def makeHist(data, title, xlabel, ylabel, bins=20):
    pylab.hist(data, bins=bins)
    pylab.title(title)
    pylab.xlabel(xlabel)
    pylab.ylabel(ylabel)

def plotDistributions():
    uniform, normal, exp = [], [], []
    for i in range(10000):
        uniform.append(random.random())
        normal.append(random.gauss(0, 1))
        exp.append(random.expovariate(0.5))
    makeHist(uniform, 'Uniform', 'Value', 'Frequency')
    plt.figure()
    makeHist(normal, 'Gaussian', 'Value', 'Frequency')
    plt.figure()
    makeHist(exp, 'Exponential', 'Value', 'Frequency')

def compareDist():
    uniform, normal, exp = [], [], []
    for i in range(10000):
        uniform.append(random.random())
        normal.append(random.gauss(0, 1))
        exp.append(random.expovariate(0.5))
    sampleSizes = range(20, 600, 1)
    udiffs = getDiffs(uniform, sampleSizes)
    ndiffs = getDiffs(normal, sampleSizes)
    ediffs = getDiffs(exp, sampleSizes)
    plotDiffs(sampleSizes, udiffs, 'Sample SD vs Population SD', 'Uniform population')
    plotDiffs(sampleSizes, ndiffs, 'Sample SD vs Population SD', 'Normal population')
    plotDiffs(sampleSizes, ediffs, 'Sample SD vs Population SD', 'Exponential population')

plotDistributions()
compareDist()
# The more skewed it is, the larger the sample is needed to lower different SD between samples and population

popSizes = (10000, 100000, 1000000)
sampleSizes = range(20, 600, 1)
for size in popSizes:
    pop = []
    for i in range(size):
        pop.append(random.expovariate(0.5))
    ediffs = getDiffs(pop, sampleSizes)
    plotDiffs(sampleSizes, ediffs, 'Sample SD vs Population SD, Exponential', 'Population size = ' + str(size))
    # The size of population doesn't affect different SD between samples and population