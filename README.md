# 信用卡评分


## 目录
- [简介](#简介)
- [安装](#安装)
- [使用](#使用)
    - [训练模型](#训练模型)
    - [训练模型并生成评分卡](#训练模型并生成评分卡)
- [展示](#展示)
    - [LR的KS曲线](#LR的KS曲线)
    - [评分卡](#评分卡)
    
    
## 简介


关键词：`逻辑回归` , `评分卡模型`, `iv` , `woe`, `KS`

## 安装
    
    cd ScoreCard/docs
    pip install -r requirements.txt 

## 使用

### 训练模型

    cd ScoreCard/
    python model/logistic_regression.py
    
### 训练模型并生成评分卡

    cd ScoreCard/
    python scorecard.py

### 目录结构

![目录结构](https://github.com/xumoremore/data-analysis-system-/blob/master/introducepicture/1.png)

### demo

下面链接为打包好的.exe可执行文件，可直接运行，但要使用数据库功能电脑需要安装mysql数据库。

可执行文件链接：[百度网盘](https://pan.baidu.com/s/128nFX1aRHE8157biClGq8Q)

提取码：prto 
