#_*_coding utf-8 _*_
#开发者：xzc
#开发时间：2020/11/59:52
#文件名称：logistic_regression.py

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn import metrics
import pandas as pd
from matplotlib import pyplot as plt
from model.eval import plot_model_ks


def train(df, target):
    """
    :param df: original dataframe
    :param target: 'SeriousDlqin2yrs'
    :return: Coefficient of logistic regression
    """
    x_train, x_test, y_train, y_test = train_test_split(df.drop(target, axis=1), df[target], test_size=0.2)
    model = LogisticRegression(class_weight='balanced') # class_weight='balanced'
    model.fit(x_train, y_train)
    predict = model.predict(x_test)
    # print("lr predict:|{}|".format(sum(predict)/len(predict)))
    y_pro = [i[1] for i in model.predict_proba(x_test)]
    plot_model_ks(y_label=y_test, y_pred=y_pro)
    # print("准确率：|{}|".format(accuracy_score(predict, y_test)))
    # print("test f1 score:|{}|".format(f1_score(predict, y_test)))
    # print("train f1 score:|{}|".format(f1_score(model.predict(x_train), y_train)))
    print('model.coef:|{}|'.format(model.coef_[0]))
    return model.coef_[0]


if __name__ == '__main__':
    # 0.001:|[0.77317193 0.55108444 0.59247142 0.34052567 0.48817733]|
    # 0.000000001:[0.75856813 0.5531054  0.59741561 0.37089774 0.4678732 ]|
    # balance
    # 0.001:|[0.78200173 0.65884436 0.7213903  0.55613476 0.50664107]|
    bintop5_cols = ['bin_age',
                    "bin_NumberOfTime30-59DaysPastDueNotWorse",
                    "bin_NumberOfTime60-89DaysPastDueNotWorse",
                    "bin_NumberOfTimes90DaysLate",
                    "bin_RevolvingUtilizationOfUnsecuredLines",
                    ]

