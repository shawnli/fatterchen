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


quote_context = OpenQuoteContext(host='127.0.0.1', sync_port=11111,  async_port=11111)
quote_context.set_handler(StockQuoteTest())
quote_context.set_handler(OrderBookTest())
quote_context.set_handler(CurKlineTest())
quote_context.set_handler(TickerTest())
quote_context.start()

#ret_code,US_tradingdays=quote_context.get_trading_days("US","2015-01-01","2017-04-16")
#ret_code,SZ_tradingdays=quote_context.get_trading_days("SZ","2015-01-01","2017-04-16")
#ret_code,SZ_stockbasicinfo = quote_context.get_stock_basicinfo("SH")
#ret_code,ret_data = quote_context.get_history_kline("SZ.000001", "2017-04-16","2017-04-18")
stock_code_list = ["SZ.000001", "SH.600332", "SZ.300376"]

for stk_code in stock_code_list:
        ret_status, ret_data = quote_context.subscribe(stk_code, "K_DAY")
        
ret_status, ret_data = quote_context.query_subscription()

print(ret_data)

for stk_code in stock_code_list:
        ret_status, ret_data = quote_context.get_cur_kline(stk_code, 100,"K_DAY")
        kline_table = ret_data
        print("%s KLINE %s" % (stk_code, "K_DAY"))
        print(kline_table)
        print("\n\n")




#for chenran in SZ_stockbasicinfo:
#print(ret_data)
#quote_context.subscribe('SZ.00001', "QUOTE", push=True)
