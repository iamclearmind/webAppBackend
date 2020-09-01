# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 12:13:24 2020

@author: Harsh
"""

# Import the backtrader platform
import backtrader as bt
# import backtrader.feeds as btfeed
from datetime import timedelta

################## Path hack. Later to be solved as package ##################
# import sys, os
# sys.path.insert(0, os.path.abspath('..'))
from spe.cust_ind import hhpc
from spe.cust_ind import dmi_inds
from spe.cust_ind import rscch
##############################################################################

# Create a Stratey
class cmTwo_monthly(bt.Strategy):
    
    params = (
    ('benchmark_name','NSEI'),
    # ('res', 1440),
    )
    
    def log(self, txt, dt=None):
        #''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.datetime(0)
#        print('%s' % (txt))

    def __init__(self):
        
        
        '''
        Create an dictionary of indicators so that we can dynamically add the
        indicators to the strategy using a loop. This mean the strategy will
        work with any numner of data feeds. 
        '''
        
        self.benchmark = self.getdatabyname(self.p.benchmark_name)
    
        self.inds = dict()
        for i, d in enumerate(self.datas):
            print('Initializing Indicators for Data :', d._name)
            if d._name == self.p.benchmark_name :
                continue
            self.inds[d] = dict()
            
            #Custom Indicators
            self.inds[d]['dmich'] = dmi_inds.DMICH(d)
            self.inds[d]['bch'] = dmi_inds.BCH(d)
            self.inds[d]['rsch'] = rscch.RSCCH(d,self.benchmark)
            self.inds[d]['pc'] = hhpc.PC(d)
            
            # New Custom Indicators
            self.inds[d]['RSH10'] = bt.indicators.SMA(self.inds[d]['rsch'].rsh,period=10)
            self.inds[d]['RSL10'] = bt.indicators.SMA(self.inds[d]['rsch'].rsl,period=10)
            self.inds[d]['ROC1'] = bt.indicators.ROC100(d,period=1)
            
            #Standard Indicatora
            # self.inds[d]['sma_close'] = bt.indicators.SMA(d.close,period=50)
            # self.inds[d]['vma'] = bt.indicators.SMA(d.volume,period=200)
            # self.inds[d]['RSCMA5'] = bt.indicators.SMA(self.inds[d]['rsch'].rsc,period=5)
            self.inds[d]['RSCMA10'] = bt.indicators.SMA(self.inds[d]['rsch'].rsc,period=10)
            # self.inds[d]['RSCMA200'] = bt.indicators.SMA(self.inds[d]['rsch'].rsc,period=200)
            self.inds[d]['PCH25'] = bt.indicators.basicops.Highest(d.high(-1),period=25)# -1 to not include current bar
            self.inds[d]['PCL25'] = bt.indicators.basicops.Lowest(d.low(-1),period=25)
           
            #Cross Conditions RSC
            self.inds[d]['RSC CU'] = bt.indicators.crossover.CrossUp(self.inds[d]['rsch'].rsc, self.inds[d]['RSCMA10'])
            self.inds[d]['RSC CD'] = bt.indicators.crossover.CrossDown(self.inds[d]['rsch'].rsc, self.inds[d]['RSCMA10'])
            

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None
        
        self.last_values = {}
        self.data_value_json = {}
    
    def stop(self):
        
        for i, d in enumerate(self.datas):
            dt, dn = self.datetime.date(), d._name
            if d._name == self.p.benchmark_name :
                continue            
            
            self.last_values['Date'] = dt
            # self.last_values['Scrip_code'] = dn
            # self.last_values['RSC'] = self.inds[d]['rsch'].rsc[0]
                        
            # Clearmind Screener Output
            dataclose = d.close[0]
            adx_val = self.inds[d]['bch'].dmi.adx[0]
            adx_ma = self.inds[d]['bch'].adx_ma.sma[0]
            
            self.last_values['PCH5'] = self.inds[d]['pc'].pch[0]
            self.last_values['PCL5'] = self.inds[d]['pc'].pcl[0] 
            self.last_values['RSLT'] = 1 if self.inds[d]['RSCMA10'] > self.inds[d]['RSCMA200'] else 0 # New addition        
            self.last_values['RS'] = 1 if dataclose > self.inds[d]['rsch'].rsh[0] else 0
            self.last_values['PDIMDI'] = 1 if self.inds[d]['dmich'].pdi[0] > self.inds[d]['dmich'].mdi[0] else 0            
            self.last_values['HH'] = 1 if dataclose > self.inds[d]['pc'].hhpc[0] else 0            
      
            self.last_values['CLRBAR'] = 1 if adx_val > adx_ma else 0            
            self.last_values['LL'] = 1 if dataclose < self.inds[d]['pc'].llpc[0]  else 0   
            self.last_values['HHC5'] = self.inds[d]['pc'].hhpc[0]
            self.last_values['LLC5'] = self.inds[d]['pc'].llpc[0]
            self.last_values['PCH25'] = self.inds[d]['PCH25'][0]
            self.last_values['PCL25'] = self.inds[d]['PCL25'][0]

            #New Additions
            self.last_values['RSH(C>10)'] = 1 if dataclose > self.inds[d]['RSH10'][0] else 0
            self.last_values['HHPC(C>5)'] = 1 if dataclose > self.inds[d]['pc'].hhpc[0] else 0
            self.last_values['BBH'] = 1 if dataclose > self.inds[d]['bch'].bbh[0] else 0      
            self.last_values['RSL(C<10)'] = 1 if dataclose < self.inds[d]['RSL10'][0] else 0
            self.last_values['RBR'] = 1 if dataclose < self.inds[d]['bch'].rbl[0] else 0
            
            self.last_values['ROC(1)'] = self.inds[d]['ROC1'][0]
            self.last_values['%>HHC'] = (dataclose - self.inds[d]['pc'].hhpc[0])/self.inds[d]['pc'].hhpc[0]*100 if dataclose > self.inds[d]['pc'].hhpc[0] else 0
            self.last_values['%<LLC'] = (dataclose - self.inds[d]['pc'].llpc[0])/self.inds[d]['pc'].llpc[0]*100 if dataclose < self.inds[d]['pc'].llpc[0] else 0
            
            self.last_values['FFU'] = 1 if self.last_values['PCH5'] > self.last_values['HHC5'] else 0
            self.last_values['FFD'] = 1 if self.last_values['PCL5'] < self.last_values['LLC5'] else 0
            self.last_values['MRL'] = 1 if self.last_values['PCH5'] < self.last_values['LLC5'] else 0
            self.last_values['MRS'] = 1 if self.last_values['PCL5'] > self.last_values['HHC5'] else 0
            
            self.last_values['RSC CROSS UP'] = 1 if self.inds[d]['RSC CU'] == 1 else 0
            self.last_values['RSC CROSS DOWN'] = 1 if self.inds[d]['RSC CD'] == 1 else 0
            
            # Indicator Values for Debug 
            # self.last_values['RSC'] = self.inds[d]['rsch'].rsc[0]
            # self.last_values['RSC10'] = self.inds[d]['RSCMA10'][0]
            self.last_values['RSH10'] = self.inds[d]['rsch'].rsh[0]
            self.last_values['RSL10'] = self.inds[d]['rsch'].rsl[0]
            self.last_values['BBH_value'] = self.inds[d]['bch'].bbh[0]
            self.last_values['RBL_value'] = self.inds[d]['bch'].rbl[0]
            
            self.data_value_json[dn] = self.last_values.copy()
            
    def strat_name():
        return 'cmTwo'
    
    def candle_lb():
        return 50

###############################################################################