#_*_coding utf-8 _*_
#开发者：xzc
#开发时间：2020/11/411:29
#文件名称：iv_filter.py
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

class IV(object):
    def __init__(self, df, target):
        self.df = df
        self.features = list(self.df.columns.values)
        self.features.remove(target)
        self.target = target
        self.feature_iv = {}
        for feature in self.features:
            self.feature_iv[feature] = self.cal_iv(feature)

    def cal_iv(self, feature):
        """
        iv = (bad_rate-good_rate) * woe
        :param feature: feature name for cal iv
        :return: iv of feature
        """
        df_iv = self.df.groupby(feature).agg({self.target:['sum', 'count']}) # 跟透视表原理一样
        df_iv.columns = list(map(''.join, df_iv.columns.values))
        df_iv = df_iv.reset_index()
        df_iv = df_iv.rename(columns={self.target+'sum':'bad', self.target+'count':'all'})
        df_iv['good'] = df_iv['all'] - df_iv['bad']
        df_iv = df_iv[[feature, 'good', 'bad']]
        df_iv['bad_rate'] = df_iv['bad'] / df_iv['bad'].sum()
        df_iv['good_rate'] = df_iv['good'] / df_iv['good'].sum()
        # np.log1p将x映射成正态分布防止log里面的内容为0
        df_iv['woe'] = np.log1p(df_iv['bad_rate'].divide(df_iv['good_rate']))
        df_iv['iv'] = (df_iv['bad_rate'] - df_iv['good_rate']) * df_iv['woe']
        return df_iv['iv'].sum()

    def top(self, n):
        """
        :param n: except return iv top n columns
        :return: top n feature name
        """
        sorted_features = [i[0] for i in sorted(self.feature_iv.items(), key=lambda item: item[1], reverse=True)]
        assert n<len(sorted_features), 'n的值必须大于所计算iv的feature数量！'
        return sorted_features[:n]

    def view(self):
        df_iv = pd.DataFrame(self.feature_iv, index=[0])
        fig = plt.figure(figsize=(20,10))
        sns.barplot(data=df_iv)
        plt.xticks(rotation=20)
        plt.show()

