import backtrader as bt
from pymongo import MongoClient


class dummy_strat(bt.Strategy):
    params = (
        ('trade_size', 1),
        ('benchmark_name', 'NSEI'),
        ('tick_size', 0.0005),
    )

    def __init__(self):
        self.dictionary = dict()
        for d in self.datas:
            self.dictionary[d] = dict()

    def stop(self):
        for d in self.datas :
            self.dictionary[d]['Status'] = str('NA')

        for d in self.datas:
            # print(self.order.status)
            self.dictionary[d]['Srcipt_code'] = d._name

            client = MongoClient("mongodb+srv://devendra:peSyS7YTgPtYwOHI@cluster0.b3n0m.mongodb.net/data?retryWrites=true&w=majority")
            db = client.data
            db.daily.update_one({"Srcipt_code" : str(self.dictionary[d]['Srcipt_code'])},{"$set":{"Status" : str(self.dictionary[d]['Status'])}})
            # db.monthly.insert_one(self.dictionary[d])
            # db.weekly.insert_one(self.dictionary[d])

    def candle_lb():
        return 1


