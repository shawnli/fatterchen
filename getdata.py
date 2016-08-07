
#-------------------------------------------------------------------------------  
# Name:        module1  
# Purpose:  
#  
# Author:      bruce.lin.chn  
#  
# Created:     23/09/2011  
# Copyright:   (c) bruce.lin.chn 2011  
# Licence:     <your licence>  
#-------------------------------------------------------------------------------  
#!/usr/bin/env python  
  
import ystockquote  
  
print(ystockquote.get_price('002250.sz')) 
print(ystockquote.get_all('002250.sz'))  
  
print(ystockquote.get_historical_prices('002500.sz', "2011-09-19","2011-09-23"))  
