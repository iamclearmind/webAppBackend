import backtrader as bt
import backtrader.indicators as btind
from spe.cust_ind import PDIMDIHL,hhpc


class LTF19(bt.Strategy):
    params = (
        ('trade_size', 1),
        ('benchmark_name', 'NSEI'),
        ('tick_size', 0.0005),
    )

    def __init__(self):

        self.inds = dict()

        for d in self.datas :
            if d._name == self.p.benchmark_name :
                continue

            self.inds[d] = dict()

            self.inds[d]['pdimdiCH'] = PDIMDIHL.PDIMDIHL(d,subplot=False)
            self.inds[d]['pdi'] = self.inds[d]['pdimdiCH'].l.pdi
            self.inds[d]['mdi'] = self.inds[d]['pdimdiCH'].l.mdi
            self.inds[d]['pdimdiCrossUp'] = btind.crossover.CrossUp(self.inds[d]['pdi'],self.inds[d]['mdi'])
            self.inds[d]['pdimdiCrossDown'] = btind.crossover.CrossDown(self.inds[d]['pdi'], self.inds[d]['mdi'])
            self.inds[d]['hpdiu'] = self.inds[d]['pdimdiCH'].l.hpdiu
            self.inds[d]['lpdid'] = self.inds[d]['pdimdiCH'].l.lpdid

            self.inds[d]['PCH'] = hhpc.PC(d,subplot=False)
            self.inds[d]['llpc'] = self.inds[d]['PCH'].l.llpc 
            # self.inds[d]['crossDownadx'] = btind.CrossDown(self.inds[d]['adx'],self.inds[d]['adxma']) 

            self.inds[d]['order'] = None

            self.inds[d]['eligible'] = False

            self.inds[d]['counter'] = 0

            self.inds[d]['tradeno'] = 0
            self.inds[d]['is_last'] = False

            self.inds[d]['buy_condition'] = False

        self.bar_counter = 0

    def prenext(self):
        # Populate d_with_len
        self.d_with_len = [d for d in self.datas if len(d) > 60]
        # call next() even when data is not available for all tickers
        self.next()

    def nextstart(self):
        # This is called exactly ONCE when all datas are loaded, when next is
        # 1st called and defaults to call `next`
        self.d_with_len = self.datas  # all data sets fulfill the guarantees now

        self.next()  # delegate the work to next

    def next(self):

        self.bar_counter += 1

        for d in self.d_with_len:

            if d._name == self.p.benchmark_name :
                continue

            # if(self.inds[d]['is_last']):
            #     return

            if self.inds[d]['order']: # check for open orders, if so, then cancel order before issuing new.
                self.cancel(self.inds[d]['order'])

            if self.inds[d]['pdimdiCrossUp']:
                self.inds[d]['buy_condition'] = True

            if self.getposition(data=d).size < self.params.trade_size and self.inds[d]['buy_condition']:
                self.inds[d]['order'] = self.buy(data=d,price=self.inds[d]['hpdiu'][0],exectype=bt.Order.Stop)

            if self.getposition(data=d).size > 0 :
                # self.inds[d]['counter'] += 1
                # self.inds[d]['eligible'] = True
                self.inds[d]['buy_condition'] = False

            if self.inds[d]['pdimdiCrossDown']:
                self.inds[d]['buy_condition'] = False

            if self.getposition(data=d).size > 0 :
                closing_price = self.inds[d]['lpdid'][0] if self.inds[d]['lpdid'][0] > self.inds[d]['llpc'][0] else self.inds[d]['llpc'][0]
                self.inds[d]['order'] = self.close(data=d,price=closing_price,exectype=bt.Order.Stop)
                # print("sell condition met")

            # if self.getposition(data=d).size > 0 and len(d) == d.buflen() - 1:
            #     self.inds[d]['order'] = self.close(data=d)
            #     self.inds[d]['is_last'] = True

            # if self.getposition(data=d).size == 0 and self.inds[d]['eligible'] :
            #     self.inds[d]['hi'] = d.high.get(size=self.inds[d]['counter'])
            #     self.inds[d]['lo'] = d.low.get(size=self.inds[d]['counter'])
            #     self.inds[d]['eligible'] = False
            #     # self.highest_lowest.append([self.data.num2date(),max(self.inds[d]['hi']),min(self.inds[d]['lo'])])
            #     self.inds[d]['tradeno'] += 1
            #     self.counter = 0
            #     print('[+] '+d.num2date().strftime("%d-%m-%Y") +' Highest in TradeNo '+ str(self.inds[d]['tradeno']) + ' of ' + str(d._name) +' is := '+ str(max(self.inds[d]['hi'])))
            #     print('[+] '+d.num2date().strftime("%d-%m-%Y") +' Lowest in TradeNo '+ str(self.inds[d]['tradeno']) + ' of ' + str(d._name) +' is := '+ str(min(self.inds[d]['lo'])))



    def candle_lb():
        return 1000