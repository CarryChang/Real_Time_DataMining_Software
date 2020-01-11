
[![996.icu](https://img.shields.io/badge/link-996.icu-red.svg)](https://996.icu)

###  Real_Time_DataMining_Sortware
#### 一款能实时进行文本挖掘的软件，包含数据的实时采集/数据清洗/结构化保存/UGC数据主题提取/情感分析/后结构化可视化等技术的综合性演示demo。基于在线民宿UGC数据的意见挖掘项目，包含数据挖掘和NLP相关的处理，负责数据采集、主题抽取、情感分析等任务。主要克服用户打分和评论不一致，实时对携程和美团在线民宿的满意度进行评测以及对额外数据进行可视化的综合性工具，多维度的对在线UGC进行数据挖掘并可视化。

<div align=center><img  src="https://github.com/CarryChang/Real_Time_DataMining_Sortware/blob/master/pic/GUI_main.png"></div>
#####  主要功能包括美团/携程在线民宿UGC的原始评论采集、主题分类、实时数据清洗、文本情感分析与后结构化结果可视化展示等模块。


>1.   使用Selenium模拟浏览器点击翻页操作，并配合Request实现了携程网爬虫封锁和自动化的采集民宿UGC内容的功能，提取后的民宿地址和在线评论等信息如下。

<div align=center><img  src="https://github.com/CarryChang/Real_Time_DataMining_Sortware/blob/master/pic/GUI_main.png"></div>

>2.   搭建了百度地图POI查询入口，可以进行自动化的批量查询POI信息的功能，信息直接存入excel中

<div align=center><img  src="https://github.com/CarryChang/Real_Time_DataMining_Sortware/blob/master/pic/GUI_main.png"></div>

> 3.   通过高频词可视化展示，归纳出评论主题
<div align=center><img  src="https://github.com/CarryChang/Real_Time_DataMining_Sortware/blob/master/pic/GUI_main.png"></div>

> 4.   构建了基于在线民宿语料的Word2vec主题聚类模型，利用主题中心词能找出对应的主题属性字典，并使用用户打分作为标注，然后通过实验贝叶斯、SVM、决策树等多种分类模型，选用最优模型对提出的评价主体 进行情感分析，针对主题属性表进行主题提取后的文本进行情感分析，分别得出当前主题对应的情感趋势，横坐标为所有关于主题为“环境”的情感得分，纵坐标为对应的情感的条数，可以起到纵观当前“环境”主题下的情感趋势，趋势往右代表当前主题评价较好，总共有{“交通”，“价格”，“体验”，“服务”，“特色”，“环境”，“设施”，“餐饮”}的主题，选取“环境”主题进行可视化之后的结果如下图所示。
<div align=center><img  src="https://github.com/CarryChang/Real_Time_DataMining_Sortware/blob/master/pic/GUI_main.png"></div>

> 5.   通过POI热力图的方式对在线民宿满意度进行展示。

<div align=center><img  src="https://github.com/CarryChang/Real_Time_DataMining_Sortware/blob/master/pic/GUI_main.png"></div>

> 6.   代码结构如下

<div align=center><img  src="https://github.com/CarryChang/Real_Time_DataMining_Sortware/blob/master/pic/GUI_main.png"></div>
