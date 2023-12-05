from matplotlib import pylab as plt

def findPayment(loan, r, m): #calculate payment
    # rate: r, month: m
    return loan*((r*(1+r)**m)/((1+r)**m-1))

class Mortgage(object):
    # abstract class for buliding different kinds of mortages
    def __init__(self, loan, annRate, months):
        self.loan = loan
        self.rate = annRate/12
        self.months = months
        self.paid = [0.0] # record paid money in every month
        self.outstanding = [loan] # record balance of loan in every month
        self.payment = findPayment(loan, self.rate, months)
        self.legend = None
    
    def makePayment(self):
        self.paid.append(self.payment)
        reduction = self.payment - self.outstanding[-1] * self.rate # total payment - interest
        self.outstanding.append(self.outstanding[-1] - reduction)
    
    def getTotalPaid(self):
        return sum(self.paid)
    
    def __str__(self):
        return self.legend
    
    def plotPayments(self, style):
        plt.plot(self.paid[1:], style, label = self.legend)

    def plotBalance(self, style):
        plt.plot(self.outstanding, style, label = self.legend)
    
    def plotTotalPaid(self, style): # plot accumulative payment
        totalPaid = [self.paid[0]]
        for i in range(1, len(self.paid)):
            totalPaid.append(totalPaid[-1]+self.paid[i])
        plt.plot(totalPaid, style, label = self.legend)
    
    def plotNet(self, style): # plot paid interest
        totalPaid = [self.paid[0]]
        for i in range(1, len(self.paid)):
            totalPaid.append(totalPaid[-1]+self.paid[i])
        equityAcquired = plt.array([self.loan] * len(self.outstanding))
        equityAcquired = equityAcquired - plt.array(self.outstanding)
        net = plt.array(totalPaid) - equityAcquired
        plt.plot(net, style, label = self.legend)
    
class Fixed(Mortgage):
    def __init__(self, loan, r, months):
        Mortgage.__init__(self, loan, r, months)
        self.legend = 'Fixed, ' + str(round(r*100, 2)) + '%'

class FixedWithPts(Mortgage):
    def __init__(self, loan, r, months, pts):
        Mortgage.__init__(self, loan, r, months)
        self.pts = pts
        self.paid = [loan*(pts/100.0)] # prepayments
        self.legend = 'Fixed, ' + str(round(r*100, 2)) + '%, ' + str(pts) + ' points'

class TwoRate(Mortgage):
    def __init__(self, loan, r, months, teaserRate, teaserMonths):
        Mortgage.__init__(self, loan, teaserRate, months)
        self.teaserMonths = teaserMonths
        self.teaserRates = teaserRate
        self.nextRate = r/12.0
        self.legend = str(teaserRate*100) + '% for ' + str(self.teaserMonths) + ' months, then ' + str(round(r*100, 2)) + '%'
    
    def makePayment(self):
        if len(self.paid) == self.teaserMonths + 1:
            self.rate = self.nextRate
            self.payment = findPayment(self.outstanding[-1], self.rate, self.months - self.teaserMonths)
        Mortgage.makePayment(self)

def compareMortgages(amt, years, fixedRate, pts, ptsRate, varRate1, varRate2, varMonths):
    totalMonths = years*12
    fixed1 = Fixed(amt, fixedRate, totalMonths)
    fixed2 = FixedWithPts(amt, ptsRate, totalMonths, pts)
    twoRate = TwoRate(amt, varRate2, totalMonths, varRate1, varMonths)
    morts = [fixed1, fixed2, twoRate]
    for m in range(totalMonths): # Calculate payment of 3 methods in total months
        for mort in morts:
            mort.makePayment()
    for m in morts:
        print(m)
        print(' Total payments = $' + str(int(m.getTotalPaid())))

def plotMortgages(morts, amt):
    def labelPlot(figure, title, xLabel, yLabel):
        plt.figure(figure)
        plt.title(title)
        plt.xlabel(xLabel)
        plt.ylabel(yLabel)
        plt.legend(loc = 'best')
    styles = ['k-', 'k-.', 'k:']
    payments, cost, balance, netCost = 0, 1, 2, 3
    for i in range(len(morts)):
        plt.figure(payments)
        morts[i].plotPayments(styles[i])
        plt.figure(cost)
        morts[i].plotTotalPaid(styles[i])
        plt.figure(balance)
        morts[i].plotBalance(styles[i])
        plt.figure(netCost)
        morts[i].plotNet(styles[i])
    labelPlot(payments, 'Monthly Payments of $' + str(amt) + ' Mortgages', 'Months', 'Monthly Payments')
    labelPlot(cost, 'Cash Outlay of $' + str(amt) + ' Mortgages', 'Months', 'Total Payments')
    labelPlot(balance, 'Balance Remaining of $' + str(amt) + ' Mortgages' , 'Months', 'Remaining Loan Balance of $')
    labelPlot(netCost, 'Net Cost of $' + str(amt) + ' Mortgages', 'Months', 'Payments - Equity $')

def compareMortgages_new(amt, years, fixedRate, pts, ptsRate, varRate1, varRate2, varMonths):
    totalMonths = years*12
    fixed1 = Fixed(amt, fixedRate, totalMonths)
    fixed2 = FixedWithPts(amt, ptsRate, totalMonths, pts)
    twoRate = TwoRate(amt, varRate2, totalMonths, varRate1, varMonths)
    morts = [fixed1, fixed2, twoRate]
    for m in range(totalMonths): # Calculate payment of 3 methods in total months
        for mort in morts:
            mort.makePayment()
    plotMortgages(morts, amt)

compareMortgages_new(200000, 30, 0.07, 3.25, 0.05, 0.045, 0.095, 48)