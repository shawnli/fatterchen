from openft.open_quant_context import *


quote_context = OpenQuoteContext(host='127.0.0.1', async_port=11111)
#0quote_context.set_handler(StockQuoteTest())
#quote_context.set_handler(OrderBookTest())
##quote_context.set_handler(CurKlineTest())
#quote_context.set_handler(TickerTest())
quote_context.start()

ret_code,US_tradingdays=quote_context.get_trading_days("US","2015-01-01","2017-04-16")
ret_code,SZ_tradingdays=quote_context.get_trading_days("SZ","2015-01-01","2017-04-16")
ret_code,SZ_stockbasicinfo = quote_context.get_stock_basicinfo("SH")
ret_code,A1 = quote_context.get_history_kline("SH.000001", "2017-04-16","2017-04-18", ktype='K_DAY', autype='qfq')

#for chenran in SZ_stockbasicinfo:
print(A1)
