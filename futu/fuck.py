import tushare as ts

import downloaddata
from openft.open_quant_context import *


class StockQuoteTest(StockQuoteHandlerBase):
    def on_recv_rsp(self, rsp_str):
        ret_code, content = super(StockQuoteTest, self).on_recv_rsp(rsp_str)
        if ret_code != RET_OK:
            print("StockQuoteTest: error, msg: %s" % content)
            return RET_ERROR, content
        print("StockQuoteTest ", content)
        return RET_OK, content


class OrderBookTest(OrderBookHandlerBase):
    def on_recv_rsp(self, rsp_str):
        ret_code, content = super(OrderBookTest, self).on_recv_rsp(rsp_str)
        if ret_code != RET_OK:
            print("OrderBookTest: error, msg: %s" % content)
            return RET_ERROR, content
        print("OrderBookTest", content)
        return RET_OK, content


class CurKlineTest(CurKlineHandlerBase):
    def on_recv_rsp(self, rsp_str):
        ret_code, content = super(CurKlineTest, self).on_recv_rsp(rsp_str)
        if ret_code != RET_OK:
            print("CurKlineTest: error, msg: %s" % content)
            return RET_ERROR, content
        print("CurKlineTest", content)
        return RET_OK, content


class TickerTest(TickerHandlerBase):
    def on_recv_rsp(self, rsp_str):
        ret_code, content = super(TickerTest, self).on_recv_rsp(rsp_str)
        if ret_code != RET_OK:
            print("TickerTest: error, msg: %s" % content)
            return RET_ERROR, content
        print("TickerTest", content)
        return RET_OK, content




quote_context = OpenQuoteContext(host='127.0.0.1', async_port=11111)
quote_context.set_handler(StockQuoteTest())
quote_context.set_handler(OrderBookTest())
quote_context.set_handler(CurKlineTest())
quote_context.set_handler(TickerTest())
quote_context.start()

stock_info=ts.get_stock_basics()

ret_status, ret_data = quote_context.get_trading_days("US", "2017-01-01", "2017-01-18")
if ret_status == RET_ERROR:
    print(ret_data)
    exit()


for index,onestock in stock_info.iterrows():
    print(index)
    stock_data=[]

    for x in ret_data:
      d = ts.get_tick_data(index,date=x)
      stock_data.append(d)
    #print(stock_data)
    file_name_prefix="D:/thinnerchen/datas/"
    file_object = open(file_name_prefix+index+".txt", 'wt')
    file_object.write(str(stock_data))
    file_object.close()