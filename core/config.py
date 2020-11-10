#_*_coding utf-8 _*_
#开发者：xzc
#开发时间：2020/11/49:49
#文件名称：config.py

from easydict import EasyDict as edict

__C = edict()
cfg = __C

__C.points0 = 650    # 基准分, 0: 数字
__C.PDO = 50     # 翻倍比    O: 字母
__C.ODDS0 = 1/5    # 初始化违约率，在违约率为1/5的情况下，信用分值为points  0: 数字

