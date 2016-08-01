# -*- coding: utf-8 -*-


from flask import Flask, json, request
import pandas as pd
import numpy as np
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('512go.db')
df = pd.read_sql("select * from zzx_unclean_zijin", conn)
conn.close()


@app.route('/')
def index():
    return "ha?"


@app.route('/money_amount_distribution')
def money_amount_distribution():
    inner_df = df
    s_date = request.args.get('s_date', '19000101000000')
    e_date = request.args.get('e_date', '21991231235959')
    min_amount = int(request.args.get('min_amount', '0'))
    max_amount = int(request.args.get('max_amount', '9999999999'))
    block_num = int(request.args.get('block_num', '10'))
    inner_df = inner_df[inner_df.trade_time > s_date][inner_df.trade_time < e_date]
    inner_df = inner_df[inner_df.money_amount > min_amount][inner_df.money_amount < max_amount]
    inner_labels = ["{0} - {1}".format(i, i + (max_amount - min_amount) / block_num-1) for i in range(min_amount,
                                                                                                    max_amount,
                                                                                                    (
                                                                                                        max_amount - min_amount) / block_num)]
    inner_df['blocks'] = pd.cut(inner_df.money_amount, block_num, labels=inner_labels)
    tmp = inner_df.groupby(['blocks']).size()
    tmp.sort_index(inplace=True)
    print inner_df.head()
    print tmp
    return tmp.to_json()


if __name__ == '__main__':
    app.run(debug=True)
