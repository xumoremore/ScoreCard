#_*_coding utf-8 _*_
#开发者：xzc
#开发时间：2020/11/411:29
#文件名称：woe_bin.py
import pandas as pd
import numpy as np
import copy

def woe(df, features, target):
    """
    df: original bin dataframe
    feature: columns list wait for convert to woe
    target: target feature name
    -----------------------------------
    woe = bad_rate/good_rate
          bad_rate = bad_i/bad_t
          good_rate = good_i/good_t
    -----------------------------------
    :return: original value of df[features] convert to woe valud of df_woecv[features]
    """
    assert isinstance(features, list), "woe中的features必须以列表形式传入"
    woecv_cols = copy.deepcopy(features)
    woecv_cols.append(target)
    df_woecv = df.copy()[woecv_cols]
    df_woecard = pd.DataFrame(columns=['features', 'variable', 'woe'])
    for feature in features:
        # 统计该字段每个取值下违约数量和总数
        df_woe = df.groupby(feature).agg({target: ['sum', 'count']})  # 跟透视表原理一样
        df_woe.columns = list(map(''.join, df_woe.columns.values))
        df_woe = df_woe.reset_index()
        df_woe = df_woe.rename(columns={target + 'sum': 'bad', target + 'count': 'all'})
        df_woe['good'] = df_woe['all'] - df_woe['bad']

        df_woe.replace(0, 0.001, inplace=True)
        df_woe = df_woe[[feature, 'good', 'bad']]
        df_woe['bad_rate'] = (df_woe['bad'] / df_woe['bad'].sum())
        df_woe['good_rate'] = df_woe['good'] / df_woe['good'].sum()
        # np.log1p防止log里面的内容为0
        """
        woe = np.ln( bad_rate/good_rate )
        当bad_rate=0,  woe=-inf
        当good_rate=0,  woe=inf  
        """
        df_woe['woe_'+feature] = np.log(df_woe['bad_rate'].divide(df_woe['good_rate']))
        df_woe = df_woe[[feature, 'woe_'+feature]]
        df_woecv = df_woecv.merge(df_woe, on=feature, how='left')
        df_woecv.drop(feature, axis=1, inplace=True)
        # 生成woecard
        df_colwoe = pd.DataFrame(columns=['features', 'variable', 'woe'])
        df_colwoe['variable'] = df_woe[feature]
        df_colwoe['features'] = feature
        df_colwoe['woe'] = df_woe['woe_'+feature]
        df_woecard = pd.concat([df_woecard, df_colwoe])
    return df_woecv, df_woecard


