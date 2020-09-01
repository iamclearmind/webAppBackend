#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
#
# Copyright (C) 2015, 2016, 2017 Daniel Rodriguez
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


import collections

import backtrader as bt
from backtrader import Order, Position


class cmTrans(bt.Analyzer):
    '''This analyzer reports the transactions occurred with each an every data in
    the system

    It looks at the order execution bits to create a ``Position`` starting from
    0 during each ``next`` cycle.

    The result is used during next to record the transactions

    '''
    # params = (
    #     ('headers', False),
    # )

    def start(self):
        # super(Transactions, self).start()
        # if self.p.headers:
        #     self.rets[self.p._pfheaders[0]] = [list(self.p._pfheaders[1:])]

        self._pos   = []
        self._allorders = []
        # self._idnames = list(enumerate(self.strategy.getdatanames()))

    def notify_order(self, order):
        # An order could have several partial executions per cycle (unlikely
        # but possible) and therefore: collect each new execution notification
        # and let the work for next
        if order.status in [order.Accepted]:

            all_o_list = []
            o_dn = order.data._name
            o_ref = order.ref
            o_dt = order.created.dt
            o_size = order.created.size
            o_price = order.created.price
            if o_size > 0:
                o_type = 'BUY ORDER'
            elif o_size < 0:
                o_type = 'SELL ORDER'
            else:
                o_type = 'NONE'
            all_o_list = [o_type, bt.num2date(o_dt).strftime("%d-%m-%Y"), o_dn, o_size, o_price, None, None, None]
            self._pos.append(all_o_list)

        # We use a fresh Position object for each round to get summary of what
        # the execution bits have done in that round
        if order.status not in [Order.Partial, Order.Completed]:

            return  # It's not an execution

        if order.status is Order.Completed :
            
            o_list = []
            o_dn    = order.data._name
            o_ref   = order.ref
            o_dt    = order.executed.dt
            o_size  = order.executed.size
            o_price = order.executed.price
            pnl     = order.executed.pnl
            if o_size > 0 :
                o_type = 'BUY TRADE'
            elif o_size < 0:
                o_type = 'SELL TRADE'
            else :
                o_type = 'NONE'
            o_list = [o_type,bt.num2date(o_dt).strftime("%d-%m-%Y"),o_dn,o_size,o_price,    None, None, None]
            self._pos.append(o_list)

    def notify_trade(self, trade):
        if trade.justopened:
            # Trade just opened
            pass
        elif trade.status == trade.Closed:
            u_list = []
            # self._pos.append('##########Trade Closed##########')
            tsize = trade.size
            dt = trade.data.num2date()
            dname = trade.data._name
            tprice = trade.data.open[0]
            tid = trade.ref
            pnl = round(trade.pnlcomm,2)
            ts_price = trade.price # Avg entry price. 
            if trade.long:
                ttype = 'LONG'
                t_ret = round((tprice - ts_price)/ts_price*100,2)
            elif not trade.long:
                ttype = 'SHORT'
                t_ret = round((tprice - ts_price)/ts_price*100*-1,2)
            # to_price = trade.data.open[-trade.barlen]
            # thist = trade.history
            # t_ret = Get value at start date, get current value
            u_list = ['HISAB',dt.strftime("%d-%m-%Y"),dname,ttype,tprice,pnl,t_ret,trade.barlen]
            self._pos.append(u_list)
            
            
