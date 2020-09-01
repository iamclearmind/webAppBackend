import backtrader as bt

class zigzag(bt.Indicator):
    lines = ('zigzag',)
    plotlines=dict(
        zigzag=dict(color='green')
    )

    def __init__(self):
        self.first = True
        self.positive = False
        self.negative = False


    def next(self):
        if self.first:
            self.first = False
            self.l.zigzag[0] = self.data0.close[0]
        else :
            self.l.zigzag[0] = self.l.zigzag[-1]

            if self.data0.close[0] >= (self.l.zigzag[0] * 1.05):
                print("[+] Positive condition met ")
                self.positive = True
                self.negative = False
                self.l.zigzag[0] = self.data0.close[0]

            if self.data0.close[0] <= (self.l.zigzag[0] * 0.95):
                print("[+] Negative condition met")
                self.positive = False
                self.negative = True
                self.l.zigzag[0] = self.data0.close[0]

            # Punam Uncle's Logic
            # if self.l.zigzag[0] > self.l.zigzag[-1] and self.data0.close[0] > self.l.zigzag[0]:
            #     self.l.zigzag[0] = self.data0.close[0]
            #
            # if self.l.zigzag[0] < self.l.zigzag[-1] and self.data0.close[0] < self.l.zigzag[0]:
            #     self.l.zigzag[0] = self.data0.close[0]

            # Pranav's Logic
            if self.positive and self.data0.close[0] > self.l.zigzag[0]:
                self.l.zigzag[0] = self.data0.close[0]

            if self.negative and self.data0.close[0] < self.l.zigzag[0]:
                self.l.zigzag[0] = self.data0.close[0]
