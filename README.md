# 信用卡评分


## 目录
- [简介](#简介)
- [安装](#安装)
- [使用](#使用)
    - [目录结构](#目录结构)
    - [训练模型](#训练模型)
    - [训练模型并生成评分卡](#训练模型并生成评分卡)
- [展示](#展示)
    - [LR的KS曲线](#LR的KS曲线)
    - [评分卡](#评分卡)
    
    
## 简介


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

### LR的KS曲线

![ks曲线](https://github.com/xumoremore/ScoreCard/blob/main/docs/KS.png)

### 评分卡

![信用评分表](https://github.com/xumoremore/ScoreCard/blob/main/docs/scorecard.png)


