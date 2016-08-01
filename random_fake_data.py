# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 10:47:58 2016

@author: zhangzexin
"""

import random
import sqlite3


cx = sqlite3.connect('512go.db')
cu=cx.cursor()


#for i in range(100000):
#    payer_account = 'E6602' + str(random.randint(23400, 23500))
#    receiver_account = 'E6602' + str(random.randint(23400, 23500))
#    trade_time = '%04d'%(random.randint(2010,2016)) + '%02d'%(random.randint(1,12)) + '%02d'%(random.randint(1,28)) + '%02d'%(random.randint(0,23)) + '%02d'%(random.randint(0,59)) + '%02d'%(random.randint(0,59))
#    money_amount = round(random.uniform(0.1, 999999), 2)
#    tp = (payer_account, receiver_account, trade_time, money_amount)
#    print tp
#    cu.execute("insert into zzx_unclean_zijin values (?,?,?,?)", tp)
    
for i in range(50000):
    payer_account = 'E6602' + str(random.randint(23400, 23500))
    receiver_account = 'E6602' + str(random.randint(23400, 23500))
    trade_time = '%04d'%(random.randint(2010,2016)) + '%02d'%(random.randint(1,12)) + '%02d'%(random.randint(1,28)) + '%02d'%(random.randint(0,23)) + '%02d'%(random.randint(0,59)) + '%02d'%(random.randint(0,59))
    money_amount = round(random.uniform(0.1, 999999), 2)
    income_out = random.choice((u'进', u'出'))
    tp = (payer_account, receiver_account, trade_time, money_amount, income_out)
    print tp
    cu.execute("insert into zzx_unclean_zijin_nsyh values (?,?,?,?,?)", tp)    
    
cx.commit()
cx.close()