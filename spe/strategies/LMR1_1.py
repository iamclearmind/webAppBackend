# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 00:41:00 2020

@author: prateek
"""


import backtrader as bt
from backtrader.indicators import SMA
from spe.cust_ind import hhpc
from spe.cust_ind import pchannel

class LMR1_1(bt.Strategy) :

    params = (
    ('trade_size',1),
    ('benchmark_name', 'NSEI'),
    ('tick_size', 0.0005),
    ('period1', 50),
    ('period2', 200),
    )

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.inds = dict()
        for d in self.datas :
            if d._name == self.p.benchmark_name :
                continue

            self.inds[d] = dict()

            self.inds[d]['dclose'] = self.datas[0].close
            self.inds[d]['ma50'] = SMA(d.close, period = self.p.period1,subplot=False)
            self.inds[d]['ma200'] = SMA(d.close, period = self.p.period2,subplot=False)
            self.inds[d]['price_channel'] = pchannel.priceChannel(d,subplot=False)
            self.inds[d]['pch5'] = self.inds[d]['price_channel'].pch
            self.inds[d]['price_channels'] = hhpc.PC(d,subplot=False)
            self.inds[d]['llpc'] = self.inds[d]['price_channels'].llpc

            self.inds[d]['order'] = None

        self.bar_counter = 0

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.data.datetime[0]
        if isinstance(dt, float):
            dt = bt.num2date(dt)
        print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        if order.status in [order.Accepted]: #Can add order.Submitted to get that details
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            self.log('ORDER ACCEPTED', dt=order.created.dt)
            self.order = order
            return

        if order.status in [order.Expired]:
            self.log('BUY EXPIRED')

        elif order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

        # Sentinel to None: new orders allowed
        # self.order = None

    def prenext(self):
        # Populate d_with_len
        self.d_with_len = [d for d in self.datas if len(d) > 60]
        # call next() even when data is not available for all tickers
        self.next()

    def nextstart(self):
        # This is called exactly ONCE when all datas are loaded, when next is
        # 1st called and defaults to call `next`
        self.d_with_len = self.datas # all data sets fulfill the guarantees now

        self.next()  # delegate the work to nextbar_executed


    def next(self):

        self.bar_counter += 1

        for d in self.d_with_len :

            if d._name == self.p.benchmark_name :
                continue

            if self.inds[d]['order']:
                self.cancel(self.inds[d]['order'])
                # return

            # Check if we are in the market
            if self.getposition(data=d).size == 0 :
                if self.inds[d]['dclose'][0] > self.inds[d]['ma200'][0] and self.inds[d]['dclose'] < self.inds[d]['ma50'][0]:
                    self.inds[d]['order'] = self.buy(data=d,exectype = bt.Order.Stop, price = self.inds[d]['pch5'][0])

            elif self.getposition(data=d).size == 1 :
                if len(self) >= (self.bar_executed):
                    self.inds[d]['order'] = self.sell(data=d, exectype = bt.Order.Stop, price = self.inds[d]['llpc'][0])

            # To Close all open positions on last bar
            if self.getposition(data=d).size > 0 and len(d) == (d.buflen() - 1):
                self.inds[d]['order'] = self.close(data=d, size=self.params.trade_size)

    def candle_lb():
        return 1000



