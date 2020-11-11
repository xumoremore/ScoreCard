# 信用卡评分


## 目录
- [简介](#简介)
- [安装](#安装)
- [使用](#使用)
    - [目录结构](#目录结构)
    - [训练模型](#训练模型)
    - [训练模型并生成评分卡](#训练模型并生成评分卡)
- [展示](#展示)
    - [模型评估](#模型评估)
    - [评分卡](#评分卡)
    
    
## 简介

对银行客户行为数据和历史违约情况做统计建模，构建关于客户的历史行为评分体系；模型重点在于可解释性，即对客户的每个行为特征取值都有对应的分值。数据集来自于kaggle竞赛的15w数据集，每个样本有11个特征字段，label为是否存在违约。对原始字段进行分箱，然后计算iv值，筛选iv值前5的变量，然后对变量做woe编码转换，woe的取值跟是否违约存在线性关系。然后使用逻辑回归训练数据得到各个变量的违约权重系数，然后将该系数转换成评分卡语言得到不同变量取值对应的信用评分表,其对应转换公式如下：
    
    bad_rate = bad_i / bad_T
    good_rate = good_i / good_T
    WOE = np.log(bad_rate/good_rate)
    IV = (bad_rate-good_rate)*WOE
    p = 1/1-np.exp(-theta*x)    # x=woe  p:违约概率
    odds = p/1-p
    theta*x = lr.coef_*woe = ln(1/1-p) = np.log(odds)
    score = A - B*np.log(odds) = A - B*lr.coef_*woe
    points0 = A - B*np.log(odds0)    # points0基准分
    points0-PDO = A-B*np.log(2odds0)    # PD0翻倍比
    => B = PD0/np.log2
    => A = points0 + B*np.log(odds0)
    score = points0 + B*lr.coef_*woe
    
关键词：`逻辑回归` , `评分卡模型`, `iv` , `woe`, `KS`

## 安装

系统windows10，使用环境python3.6。

    cd ScoreCard/docs
    pip install -r requirements.txt 

## 使用

### 训练模型

    cd ScoreCard/
    python model/logistic_regression.py
    
### 训练模型并生成评分卡

在ScoreCard/data/config.py文件设定评分卡基准分，翻倍比，初始基准分。在训练数据放在ScoreCard/data目录下，在scorecard.py文件里面指定训练数据路径，结果保存路径，以及保留特征变量数量。下面开始训练模型并且生成评分卡。

    cd ScoreCard/
    python scorecard.py
    
### 目录结构
略

## 展示

### 模型评估

![ks曲线](https://github.com/xumoremore/ScoreCard/blob/main/docs/KS.png)

### 评分卡

![信用评分表](https://github.com/xumoremore/ScoreCard/blob/main/docs/scorecard.png)


