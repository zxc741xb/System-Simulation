import random
class FairRoulette():
    def __init__(self):
        self.pockets = []
        for i in range(1,37):
            # put 1~36 into pockets
            self.pockets.append(i)
        self.ball = None
        self.blackOdds, self.redOdds = 1.0, 1.0
        self.pocketsOdds = len(self.pockets) - 1.0
    
    def spin(self):
        self.ball = random.choice(self.pockets)
    
    def isBlack(self):
        if type(self.ball) != int:
            return False
        if((self.ball>0 and self.ball<=10) or (self.ball>18 and self.ball<=28)):
            return self.ball%2==0
        else:
            return self.ball%2==1
    
    def isRed(self):
        return type(self.ball) == int and not self.isBlack()
    
    # 計算獲利
    def betBlack(self, amt):
        if self.isBlack():
            return amt*self.blackOdds
        else: return -amt
    
    def betRed(self, amt):
        if self.isRed():
            return amt*self.redOdds
        else: return -amt
    
    def betPocket(self, pocket, amt):
        if str(pocket) == str(self.ball):
            return amt*self.pocketsOdds
        else: return -amt
    
    def __str__(self):
        return 'Fair Roulette'

class EuRoulette(FairRoulette):
    def __init__(self):
        FairRoulette.__init__(self)
        self.pockets.append('0') # Especially for European roulette
    def __str__(self):
        return 'European Roulette'

class AmRoulette(EuRoulette):
    def __init__(self):
        EuRoulette.__init__(self)
        self.pockets.append('00') # Especially for American roulette
    def __str__(self):
        return 'American Roulette'

def playRoulette(game, numSpins, toPrint=True):
    luckyNumber = '2'
    bet = 1
    # 賭紅/黑/數字的總獲利
    totRed, totBlack, totPocket = 0.0, 0.0, 0.0
    for i in range(numSpins):
        game.spin()
        totRed += game.betRed(bet)
        totBlack += game.betBlack(bet)
        totPocket += game.betPocket(luckyNumber, bet)
    if toPrint:
        print(numSpins, 'spins of', game)
        print('Expected return betting red =', str(totRed/numSpins*100) , '%')
        print('Expected return betting black =', str(totBlack/numSpins*100) , '%')
        print('Expected return betting', luckyNumber, '=', str(totPocket/numSpins*100) , '%\n')
    return (totRed/numSpins, totBlack/numSpins, totPocket/numSpins)

def findPocketReturn(game, numTrials, trialSize, toPrint):
    # trialSize means number of spins in one trial
    pocketReturns = []
    for t in range(numTrials):
        trialVals = playRoulette(game, trialSize, toPrint)
        pocketReturns.append(trialVals[2])
    return pocketReturns


#game1 = FairRoulette()
#playRoulette(game1, 10000000)

def getMeanAndStd(X):
    mean = sum(X)/float(len(X))
    tot = 0.0
    for x in X:
        tot += (x-mean)**2
    std = (tot/len(X))**0.5
    return mean, std

random.seed(0)
numTrials = 20
games = (FairRoulette, EuRoulette, AmRoulette)
for numSpins in (100, 1000, 10000, 100000):
    print('\nSimulate betting a pocker for', numTrials, 'trials of', numSpins, 'spins each')
    for G in games:
        pocketReturns = findPocketReturn(G(), numTrials, numSpins, False)
        mean, std = getMeanAndStd(pocketReturns)
        print('Exp. return for', G(), '= '+ str(round(100*mean, 3)) + '%, ' + '+/- '+ str(round(100*1.96*std, 2)) + '% with 95 percent condidence')
