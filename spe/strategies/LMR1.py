# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 00:41:00 2020

@author: prateek
"""


import backtrader as bt
from backtrader.indicators import SMA
from spe.cust_ind import hhpc
from spe.cust_ind import pchannel

class LMR1(bt.Strategy) :

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
      self.dclose = self.datas[0].close
      self.ma50 = SMA(self.data0.close, period = self.p.period1,subplot=False)
      self.ma200 = SMA(self.data0.close, period = self.p.period2,subplot=False)
      self.price_channel = pchannel.priceChannel(self.data0,subplot=False)
      self.pch5 = self.price_channel.pch
      self.price_channels = hhpc.PC(self.data0,subplot=False)
      self.llpc = self.price_channels.llpc
      self.order = None
      self.bar_counter = 0


    def notify_order(self, order):
      if order.status in [order.Submitted, order.Accepted]:
        return

       # Check if an order has been completed
       # Attention: broker could reject order if not enough cash
      if order.status in [order.Completed]:
        if order.isbuy():
          self.log('BUY EXECUTED, %.2f' % order.executed.price)
        elif order.issell():
          self.log('SELL EXECUTED, %.2f' % order.executed.price)

        self.bar_executed = len(self)

      elif order.status in [order.Canceled, order.Margin, order.Rejected]:
        self.log('Order Canceled/Margin/Rejected')

     # Write down: no pending order
      self.order = None

    def next(self):

     # Check if an order is pending ... if yes, we cannot send a 2nd one
      self.bar_counter += 1
      if self.order:
        self.cancel(self.order)
        return


     # Check if we are in the market
      if self.position.size == 0 :
        if self.dclose[0] > self.ma200[0] and self.dclose < self.ma50[0]:
          self.order = self.buy(exectype = bt.Order.Stop, price = self.pch5[0])
      elif self.position.size == 1 :
        if len(self) >= (self.bar_executed):
          self.order = self.sell(exectype = bt.Order.Stop, price = self.llpc[0])

        # To Close all open positions on last bar
        if self.position.size > 0 and len(self.data0) == (self.data.buflen() - 1):
            self.order = self.close(self.data0, size=self.params.trade_size)

    def candle_lb():
        return 1000
