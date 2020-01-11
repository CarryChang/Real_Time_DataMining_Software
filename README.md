
[![996.icu](https://img.shields.io/badge/link-996.icu-red.svg)](https://996.icu)

###  Real_Time_DataMining_Sortware
#### 一款能实时进行文本挖掘的软件，包含数据的实时采集/数据清洗/结构化保存/UGC数据主题提取/情感分析/后结构化可视化等技术的综合性演示demo。基于在线民宿UGC数据的意见挖掘项目，包含数据挖掘和NLP相关的处理，负责数据采集、主题抽取、情感分析等任务。主要克服用户打分和评论不一致，实时对携程和美团在线民宿的满意度进行评测以及对额外数据进行可视化的综合性工具，多维度的对在线UGC进行数据挖掘并可视化，对比顾客直接打分的结果来看，运用机器学习的情感分析方法更能挖掘到详细的顾客意见和对应的合理评分。
#### 直接运行Python3 RealTime_UGC_Analysis_GUI.py 即可打开本软件的GUI界面，缺失的库按照提示进行安装即可。
<div align=center><img  src="https://github.com/CarryChang/Real_Time_DataMining_Sortware/blob/master/pic/GUI_main.png"></div>

#####  主要功能包括美团/携程在线民宿UGC的原始评论采集、主题分类、实时数据清洗、文本情感分析与后结构化结果可视化展示等模块。


>1.   使用Request模拟浏览实现了携程/美团民宿的实时自动化的采集民宿UGC内容的功能，提取后的民宿地址和在线评论等信息如下。

<div align=center><img  src="https://github.com/CarryChang/Real_Time_DataMining_Sortware/blob/master/pic/meituan.png"></div>
<div align=center><img  src="https://github.com/CarryChang/Real_Time_DataMining_Sortware/blob/master/pic/data_collector.png"></div>

>2.   搭UGC主题情感分析：环境

<div align=center><img  src="https://github.com/CarryChang/Real_Time_DataMining_Sortware/blob/master/pic/environment_analysis.png"></div>

> 3.   提取UGC标签，并进行量化可视化
<div align=center><img  src="https://github.com/CarryChang/Real_Time_DataMining_Sortware/blob/master/pic/label.png"></div>

> 4.   单家民宿的UGC情感分析结果
<div align=center><img  src="https://github.com/CarryChang/Real_Time_DataMining_Sortware/blob/master/pic/sentiment_analysis.png"></div>
<div align=center><img  src="https://github.com/CarryChang/Real_Time_DataMining_Sortware/blob/master/pic/whole_emotion_analysis.png"></div>

> 5.   UGC顾客打分占比

<div align=center><img  src="https://github.com/CarryChang/Real_Time_DataMining_Sortware/blob/master/pic/total_score.png"></div>

> 6.   对应店铺的第二次以上的预定情况

<div align=center><img  src="https://github.com/CarryChang/Real_Time_DataMining_Sortware/blob/master/pic/rebook.png"></div>
