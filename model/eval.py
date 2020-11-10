#_*_coding utf-8 _*_
#开发者：xzc
#开发时间：2020/11/919:53
#文件名称：test.py

from sklearn import metrics
import pandas as pd
from matplotlib import pyplot as plt

def plot_roc(y_label, y_pred):
    """
    y_label:测试集的y
    y_pred:对测试集预测后的概率

    return:ROC曲线
    """
    tpr, fpr, threshold = metrics.roc_curve(y_label, y_pred)
    AUC = metrics.roc_auc_score(y_label, y_pred)
    fig = plt.figure(figsize=(6, 4))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(tpr, fpr, color='blue', label='AUC=%.3f' % AUC)
    ax.plot([0, 1], [0, 1], 'r--')
    ax.set_ylim(0, 1)
    ax.set_xlim(0, 1)
    ax.set_title('ROC')
    ax.legend(loc='best')
    plt.show()


def plot_model_ks(y_label, y_pred):
    """
    y_label:True label
    y_pred:probilaty of predict label
    return:KS曲线
    """
    pred_list = list(y_pred)
    label_list = list(y_label)
    total_bad = sum(label_list)
    total_good = len(label_list) - total_bad
    items = sorted(zip(pred_list, label_list), key=lambda x: x[0])
    step = (max(pred_list) - min(pred_list)) / 200

    pred_bin = []
    good_rate = []
    bad_rate = []
    ks_list = []
    for i in range(1, 201):
        idx = min(pred_list) + i * step
        pred_bin.append(idx)
        label_bin = [x[1] for x in items if x[0] < idx]
        bad_num = sum(label_bin)
        good_num = len(label_bin) - bad_num
        goodrate = good_num / total_good
        badrate = bad_num / total_bad
        ks = abs(goodrate - badrate)
        good_rate.append(goodrate)
        bad_rate.append(badrate)
        ks_list.append(ks)
        # print("ks_list:|{}|".format(ks_list))
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(pred_bin, good_rate, color='green', label='good_rate')
    ax.plot(pred_bin, bad_rate, color='red', label='bad_rate')
    ax.plot(pred_bin, ks_list, color='blue', label='good-bad')
    ax.set_title('KS:{:.3f}'.format(max(ks_list)))
    ax.legend(loc='best')
    plt.show()
    # return plt.show(ax)