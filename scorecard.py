#_*_coding utf-8 _*_
#开发者：xzc
#开发时间：2020/11/411:26
#文件名称：scorecard.py

import pandas as pd
import numpy as np
from core.config import cfg
from core import var_convert
from core import var_filter
import model

def ab(points0, PDO, ODDS0):
    """
    points0 = A-B*ln(odds)
    points0 - PD0 = A-B*ln(2*odds)
    :param points0: based score
    :param PDO: point of double odds
    :param ODDS0: based odds
    :return: 
    """
    B = PDO / np.log(2)
    A = points0 + B * np.log(ODDS0)  # log(odds0/(1+odds0))
    return {'A':A, 'B':B}

def generate_scorecard(df_woecard, model_coef, B):
    """
    p: Probability of default
    odds: winning probability
    p = 1/1+exp(-theta^T*x)
    odds = p/1-p
    score = B*ln(odds) 
          = (theta)^T*x 
          = model_coef*woe
    :param df_woecard: the woe values of features 
    :param model_coef: the coef of features
    :param B: PD0/np.log(2)
    :return: scoredcard
    """
    score_list = []
    # 模型系数
    for i, (name, group) in enumerate(df_woecard.groupby("features")):
        #         print("i:|{}|, name:|{}|, df:|{}|".format(i, name, df))
        odds_sum = 0
        for index, row in group.iterrows():
            score_list.append([name, row['variable'], int(round(model_coef[i] * row['woe'] * B))])  # round返回浮点数的四舍五入
        odds_sum += -model_coef[i] * row['woe']
    scorecard = pd.DataFrame(score_list, columns=['features', 'variable', 'Score'])
    return scorecard


def str_to_int(s):
    if s=='-inf':
        return -999999
    if s=='inf':
        return 999999
    return float(s)


# # 将value映射到bin
# def map_value_to_bin(feature_value, col_scores):
#     for index, row in col_scores.iterrows():
#         bins = str(row['variable'])
#         left_open = bins[0] =='('
#         right_open = bins[-1]==')'
#         binnings = bins[1:-1].split(',')
#         temp = str_to_int(binnings[0])
#         temp2 = str_to_int(binnings[1])
#         # 检测左括号
#         in_range = True
#         if left_open:
#             if feature_value <= temp:
#                 in_range = False
#         else:
#             if feature_value < temp:
#                 in_range = False
#         # 检查右括号
#         if right_open:
#             if feature_value <= temp2:
#                 in_range = False
#         else:
#             if feature_value > temp2:
#                 in_range = False
#         if in_range:
#             return row['variable']


def map_to_score(df, scorecard):
    """
    cal one single sample's score
    :param df: original single sample
    :param scorecard: the card of every feature's score
    :return: score of df
    """
    score_columns = list(scorecard['features'].unique())
    scores_sum = 0
    for col in score_columns:
        # 从建好的评分卡表中取出评分规则
        col_scores = scorecard[scorecard['features'] == col]
        # 取出具体的评分值
        feature_value = df[col]
        # feature_bin = map_value_to_bin(feature_value, col_scores)
        feature_bin = feature_value
        col_score = col_scores[col_scores['variable'] == feature_bin]
        scores_sum += col_score['Score'].values[0]
    return scores_sum

def cal_score(df, scorecard, A):
    """
    cal all sample's score
    score = A - B*ln(odds)
    :param df: original dataframe
    :param scorecard: the card of every feature's score
    :param A: points0 + B * np.log(ODDS0)  # based score
    :return: df + score of df
    """
    df = df.copy()
    df['score'] = df.apply(map_to_score, args=(scorecard,), axis=1)
    df['score'] = df["score"].astype(int)
    df['score'] = -df['score'] + A
    return df


if __name__ == '__main__':
    df = pd.read_csv('data/preprocessed_data.csv')
    # var_filter.IV(df=df, target='SeriousDlqin2yrs').view()
    top5cols = var_filter.IV(df=df, target='SeriousDlqin2yrs').top(5)
    df_bin = df[top5cols]
    df_woe, df_woecard = var_convert.woe(df=df, features=top5cols, target='SeriousDlqin2yrs')  # 只选择了5个col，则返回的df_woe也只有5个字段
    # print(df_woe.isnull().sum())
    model_coef = model.logistic_regression.train(df=df_woe, target='SeriousDlqin2yrs')
    AB = ab(cfg.points0, cfg.PDO, cfg.ODDS0)
    scorecard = generate_scorecard(df_woecard=df_woecard, model_coef=model_coef, B=AB['B'])
    scorecard.to_csv('data/scorecard.csv')
    mapscore = cal_score(df=df[top5cols], scorecard=scorecard, A=AB['A'])
    mapscore.to_csv('data/mapscore.csv')


