# -*- coding: utf-8 -*-

from flask import Flask, request
import pandas as pd
import numpy as np
import sqlite3

app = Flask(__name__)

# 初始化整体数据集
conn = sqlite3.connect('512go.db')
df = pd.read_sql("select * from zzx_unclean_zijin", conn)
conn.close()


@app.route('/')
def index():
    return "ha?"

# 对整体数据集进行筛选并且等额分区间统计
@app.route('/money_amount_distribution')
def money_amount_distribution():
    # copy一下数据
    inner_df = df
    # 获取request的参数
    s_date = request.args.get('s_date', '19000101000000')
    e_date = request.args.get('e_date', '21991231235959')
    min_amount = int(request.args.get('min_amount', '0'))
    max_amount = int(request.args.get('max_amount', '9999999999'))
    block_num = int(request.args.get('block_num', '10'))
    # 依据参数对inner_df进行筛选
    inner_df = inner_df[inner_df.trade_time > s_date][inner_df.trade_time < e_date]
    inner_df = inner_df[inner_df.money_amount > min_amount][inner_df.money_amount < max_amount]
    # 依据最大值最小值和区间数量来划分金额分布的区间范围
    label_range = range(min_amount, max_amount, (max_amount - min_amount) / block_num)
    # 把区间化为标准格式
    inner_labels = ["{0} - {1}".format(i, i + (max_amount - min_amount) / block_num-1) for i in label_range]
    # 将每条记录后面加上一个所属区间范围'blocks'的字段
    inner_df['blocks'] = pd.cut(inner_df.money_amount, block_num, labels=inner_labels)
    # 对各个区间的记录数进行统计
    tmp = inner_df.groupby(['blocks']).size()
    # 排序（不一定必须）
    tmp.sort_index(inplace=True)
    #print inner_df.head()
    #print tmp
    return tmp.T.to_json()


if __name__ == '__main__':
    app.run(debug=True)
