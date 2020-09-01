from dao import db_datasource as ds

def get_ticker_names():
    connection = ds.prod_db_conn()
    cursor = connection.cursor()
    record = return_record(cursor,"select scrip_code,count(*) as c from ohlcv_bo_equity_1440 group by scrip_code order by c desc")
    pass

def return_record(cursor,query):
    cursor.execute(query)
    record = cursor.fetchall()
    return record


if __name__ == '__main__':
    get_ticker_names()