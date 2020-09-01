import backtrader as bt
import backtrader.indicators as btind
import datetime
from spe.cust_ind import NEW_HIGH_STOP80
from spe.cust_ind import NEW_HIGH
from spe.cust_ind import hhpc


class LTF12B3(bt.Strategy):
    params = (
        ('trade_size', 1),
        ('benchmark_name', 'NSEI'),
        ('tick_size', 0.0005),
    )

    def __init__(self):
        self.inds = dict()

        for d in self.datas:
            self.inds[d] = dict()

            if d._name == self.p.benchmark_name:
                continue

            self.inds[d]['newHighCH'] = NEW_HIGH.newHigh(d,subplot=False)
            self.inds[d]['newHigh'] = self.inds[d]['newHighCH'].newHigh

            self.inds[d]['newHighStop80CH'] = NEW_HIGH_STOP80.newHighstop80(d,subplot=False)
            self.inds[d]['newHighStop80'] = self.inds[d]['newHighStop80CH'].newHighstop80

            self.inds[d]['llpcCH'] = hhpc.PC(d,subplot=False)
            self.inds[d]['llpc'] = self.inds[d]['llpcCH'].l.llpc


            self.inds[d]['buy_order'] = None
            self.inds[d]['sell_order'] = None

            self.inds[d]['tradeNo'] = 0
            self.inds[d]['counter'] = 0
            self.inds[d]['eligible'] = False
            self.inds[d]['first_order'] = True
            self.inds[d]['prev_llpc'] = 0
            self.inds[d]['hi'], self.inds[d]['lo'] = d.high, d.low
            self.inds[d]['temp'] = list()
        self.bar_counter = 0

        self.highest_lowest = []


    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.data.datetime[0]
        if isinstance(dt, float):
            dt = bt.num2date(dt)
        print('%s, %s' % (dt.isoformat(), txt))

    # def notify_order(self, order):
    #     if order.status in [order.Accepted]: #Can add order.Submitted to get that details
    #         # Buy/Sell order submitted/accepted to/by broker - Nothing to do
    #         self.log('ORDER ACCEPTED', dt=order.created.dt)
    #         self.inds[order.data]['order'] = order
    #         return

    #     if order.status in [order.Expired]:
    #         self.log('BUY EXPIRED')

    #     elif order.status in [order.Completed]:
    #         if order.isbuy():
    #             self.log(
    #                 'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
    #                 (order.executed.price,
    #                  order.executed.value,
    #                  order.executed.comm))

    #         else:  # Sell
    #             self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
    #                      (order.executed.price,
    #                       order.executed.value,
    #                       order.executed.comm))

    #     # Sentinel to None: new orders allowed
    #     # self.inds[order.data]['order'] = None


    # def notify_trade(self, trade):
    #     self.inds[trade.data]['prev_llpc'] = self.inds[trade.data]['llpc'][0]

    def prenext(self):
        # Populate d_with_len
        self.d_with_len = [d for d in self.datas if len(d) > 6]  # changed value to 0
        # call next() even when data is not available for all tickers
        self.next()

    def nextstart(self):
        # This is called exactly ONCE when all datas are loaded, when next is
        # 1st called and defaults to call `next`
        self.d_with_len = self.datas # all data sets fulfill the guarantees now

        self.next()  # delegate the work to next

    def next(self):
        self.bar_counter += 1
        for d in self.d_with_len:
            if d._name == self.p.benchmark_name:
                continue
            if self.inds[d]['buy_order']: # check for open orders, if so, then cancel order before issuing new.
                self.cancel(self.inds[d]['buy_order'])
            if self.inds[d]['sell_order']: # check for open orders, if so, then cancel order before issuing new.
                self.cancel(self.inds[d]['sell_order'])

            if self.getposition(data=d).size < self.params.trade_size  :
                self.inds[d]['buy_order'] = self.buy(data=d,price=self.inds[d]['newHigh'][0],exectype=bt.Order.Stop)
                # if self.inds[d]['first_order'] :
                #     self.inds[d]['first_order'] = False
                # else :
                #     if self.inds[d]['llpc'][0] > self.inds[d]['llpc'][-1] :
                #         self.inds[d]['buy_order'] = self.buy(data=d,price=d.open[0],exectype=bt.Order.Stop)
                    # print(self.inds[d]['last_buy_price'])
                # print('buy condition met')

            # if self.getposition(data=d).size > 0 :
            #     self.inds[d]['counter'] += 1
            #     self.inds[d]['eligible'] = True

            if self.getposition(data=d).size > 0 :
                self.inds[d]['sell_order'] = self.close(data=d,price=self.inds[d]['newHighStop80'][0],exectype=bt.Order.Stop)
                self.inds[d]['first_order'] = True
                # self.inds[d]['a']
                # print("sell condition met")

            # To Close all open positions on last bar
            if self.getposition(data=d).size > 0 and len(d) == (d.buflen() - 1):
                self.inds[d]['sell_order'] = self.close(data=d, size=self.params.trade_size)
                

            # if self.getposition(data=d).size == 0 and self.inds[d]['eligible'] :
            #     hi = d.high.get(size=self.inds[d]['counter'])
            #     lo = d.low.get(size=self.inds[d]['counter'])
            #     self.inds[d]['eligible'] = False
            #     self.highest_lowest.append([self.data.num2date(),max(hi),min(lo)])
            #     # self.negative_low[0] = (self.data.num2date(),min(lo))
            #     self.inds[d]['tradeNo'] += 1
            #     self.inds[d]['counter'] = 0
            #     # print('[+] Highest in TradeNo '+ str(self.inds[d]['tradeNo']) +' is := '+ str(self.highest))
            #     # print('[+] Lowest in TradeNo '+ str(self.inds[d]['tradeNo']) +' is := '+ str(self.lowest))


    def candle_lb():
        return 1000