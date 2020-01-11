import re
import tkinter as tk
from threading import Thread
from txt_analysis import picturing
from txt_analysis.spider_xiecheng import crawl as xiecheng_crawl
from txt_analysis import spider_xiecheng
from txt_analysis.spider_zhenguo import crawl as zhenguo_crawl
from txt_analysis import spider_zhenguo
from snownlp import SnowNLP
import json
import matplotlib.pyplot as plt
from PIL import ImageTk, Image
# 显示中文
plt.rcParams['font.sans-serif'] = ['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号
#有中文出现的情况，需要u'内容'
import numpy as np
# 设定变量参数
ALL = "all comments"
ALL1 = "all comments"
positive = "good comments"
medium = "medium comments"
negative = "bad comments"
taste_pos = " taste_pos"
taste_neg = " taste_neg"
taste = " taste"
speed_pos = " speed_pos"
speed_neg = " speed_neg"
speed = " speed"
weight_pos = " weight_pos"
weight_neg = " weight_neg"
weight = " weight"
service_pos = " service_pos"
service_neg = " service_neg"
service = " service"
price_pos = " price_pos"
price_neg = " price_neg"
price = " price"
start = 7
height = 30
width = 60
re_space = re.compile('(\s+)')
all_direction = tk.E + tk.N + tk.W + tk.S
result = None
def get_result():
    global result
    try:
        ##爬虫转接
        if 'ctrip' in url_tv.get():
            result1 = spider_xiecheng.crawl(url_tv.get())
            with open("resource.txt", "w", encoding="utf-8") as f:
                json.dump(result1, f, ensure_ascii=False,indent=2)
            result = xiecheng_crawl(url_tv.get())
            prompt_text.set("携程民宿在线评论数据采集完毕，可以进行后续分析")
        elif 'meituan' in url_tv.get():
            result1 = spider_zhenguo.crawl(url_tv.get())
            with open("resource.txt", "w", encoding="utf-8") as f:
                json.dump(result1, f, ensure_ascii=False,indent=2)
            result = zhenguo_crawl(url_tv.get())
            prompt_text.set("美团民宿在线评论数据采集完毕，可以进行后续分析")
        else:
            prompt_text.set("地址有误，请重新输入!")
    except ValueError:
        prompt_text.set("地址有误，请重新输入!")
def data_collecting():
    #点击输入框时，开启多线程，将信息发送给prompt_text
    prompt_text.set("正在实时采集信息，请稍后......")
    ############采集功能使用多线程来维护界面的流畅
    t = Thread(target=get_result)
    t.start()
###########使用传参
def test_tag(parse_result, sentence, type_, foreground, i, check_tv, j):
    index = start
    if check_tv.get():
        result = parse_result[type_]
        for a in result:
            index = sentence.index(a, index)
            text.tag_add("tag%d_%d" % (i, j), "%d.%d" % (i, index), "%d.%d" % (i, index + len(a)))
            text.tag_config("tag%d_%d" % (i, j), foreground=foreground)
            index += len(a)
            j += 1
    return j
def text_tag_config(sentence, i):
    # sentence = re_space.sub(r' ', sentence)
    # print(i, sentence)
    # #########增加情感极性分数显示
    try:
        text.tag_config('a', foreground='red')
        text.tag_config('b', foreground='blue')
        sentence_2 = str(sentence)
        sentence_1 = "%d. %s" % (i, str(sentence_2))
        text.insert(tk.END, "%s\n" % str(sentence_1), ('b'))
    except:
        text.tag_config('a', foreground='red')
        text.tag_config('b', foreground='blue')
        sentence_2 = re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]").sub('\t', sentence)
        sentence_1 = "%d. %s" % (i, str(sentence_2))
        text.insert(tk.END, "%s\n" % str(sentence_1), ('b'))
    finally:
        pass
# 增加对于积极和消极的极性评价
def text_tag_config1(sentence, i, score):
    # sentence = re_space.sub(r' ', sentence)
    #########增加情感极性分数显示
    try:
        text.tag_config('a', foreground='red')
        sentence_2 = re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]").sub('\t', sentence)
        sentence_1 = "%5d. %s %s" % (i, sentence_2, score)
        text.insert(tk.END, "%s\n" % sentence_1, ('a'))
    except:
        pass

########以单一句子进行，进行情感趋势画图
def emotion_analysis(which):
    col = 10
    if result is not None:
        sentiments_list = []
        text.delete(1.0, tk.END)
        comments = result["content"]
        if which == ALL1:
            j_1 = 0
            detail_content = []
            for i in comments:
                if len(i) > 2:
                    for i_1 in re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]").sub('\t', i).split('\t'):
                            detail_content.append(i_1)
            for i1 in set(detail_content):
                if len(i1) > 3:
                    s = SnowNLP(i1)
                    score = s.sentiments
                    sentiments_list.append(score)
                    j_1 += 1
                    text_tag_config1(i1, j_1, score)
        plt.hist(sentiments_list, bins=col)
        plt.xlabel("情感值")
        plt.ylabel("评论数目")
        plt.title('整体情感极性分布图')
        plt.show()
        plt.close()
def emotion_pic(which):
    col = 5

    # 使用关键字找取对应的评论
    environment_keywords = ['环境','周边','风景','空气','江景','小区','景点','夜景','街','周围','景区','声音','景色','马路']
    traffic_keywords = ['交通','车程','地段','路程','停车','机场','离','车站','地理','位置','地理','中心','海拔','码头','旁边']
    weight_keywords = ['设施','设备','条件','硬件','房间','马桶','阳台','卫生间','洗手间','空调','被子','床','大厅','电','摆设','水','电','客厅']
    service_keywords = ['服务','态度','前台','服务员','老板','掌柜','店家','工作人员','房东','小姐姐','小哥']
    meal_keywords = ['餐饮','早餐','咖啡','味道','饭','菜','水果','特产','餐','美食','烧烤','宵夜','食材','饭馆','小吃']
    if result is not None:
        text.delete(1.0, tk.END)
        comments = result["content"]
        if which == taste:
            sentiments_list = []
            j1 = 1
            detail_content = []
            for i in comments:
                if len(i) > 3:
                    for i_1 in re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]").sub('\t', i).split('\t'):
                        for keyword in environment_keywords:
                            if keyword in i_1:
                                detail_content.append(i_1)
            for i1 in set(detail_content):
                if len(i1) > 3:
                    s = SnowNLP(i1)
                    score = s.sentiments
                    sentiments_list.append(score)
                    text_tag_config1(i1, j1, score)
                    j1 += 1
            plt.hist(sentiments_list, bins=col)
            plt.xlabel("情感值")
            plt.ylabel("评论数目")
            plt.title('环境情感极性分布图')
            plt.show()
            plt.close()
        elif which == speed:
            sentiments_list = []
            j2 = 1
            detail_content = []
            for i in comments:
                if len(i) > 3:
                    for i_1 in re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]").sub('\t', i).split('\t'):
                        for keyword in traffic_keywords:
                            if keyword in i_1:
                                detail_content.append(i_1)
            for i1 in set(detail_content):
                if len(i1) > 3:
                    s = SnowNLP(i1)
                    score = s.sentiments
                    sentiments_list.append(score)
                    text_tag_config1(i1, j2, score)
                    j2 += 1
            plt.hist(sentiments_list, bins=col)
            plt.xlabel("情感值")
            plt.ylabel("评论数目")
            plt.title('交通情感极性分布图')
            plt.show()
            plt.close()
        elif which == weight:
            j3 = 1
            sentiments_list = []
            detail_content = []
            for i in comments:
                if len(i) > 3:
                    for i_1 in re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]").sub('\t', i).split('\t'):
                        for keyword in weight_keywords:
                            if keyword in i_1:
                                detail_content.append(i_1)
            for i1 in set(detail_content):
                if len(i1) > 3:
                    s = SnowNLP(i1)
                    score = s.sentiments
                    sentiments_list.append(score)
                    text_tag_config1(i1, j3, score)
                    j3 += 1
            plt.hist(sentiments_list, bins=col)
            plt.xlabel("情感值")
            plt.ylabel("评论数目")
            plt.title('设施情感极性分布图')
            plt.show()
            plt.close()
        elif which == service:
            j4 = 1
            sentiments_list = []
            detail_content = []
            for i in comments:
                if len(i) > 3:
                    for i_1 in re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]").sub('\t', i).split('\t'):
                        for keyword in service_keywords:
                            if keyword in i_1:
                                detail_content.append(i_1)
            for i1 in set(detail_content):
                if len(i1) > 3:
                    s = SnowNLP(i1)
                    score = s.sentiments
                    sentiments_list.append(score)
                    text_tag_config1(i1, j4, score)
                    j4 += 1
            plt.hist(sentiments_list, bins=col)
            plt.xlabel("情感值")
            plt.ylabel("评论数目")
            plt.title('服务情感极性分布图')
            plt.show()
            plt.close()
        elif which == price:
            j5 = 1
            sentiments_list = []
            detail_content = []
            for i in comments:
                if len(i) > 3:
                    for i_1 in re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]").sub('\t', i).split('\t'):
                        for keyword in meal_keywords:
                            if keyword in i_1:
                                detail_content.append(i_1)
            for i1 in set(detail_content):
                if len(i1) > 3:
                ###对符合条件的抓取出来，并计算情感极性
                    s = SnowNLP(i1)
                    score = s.sentiments
                    sentiments_list.append(score)
                    text_tag_config1(i1, j5, score)
                    j5 += 1
            plt.hist(sentiments_list, bins=col)
            plt.xlabel("情感值")
            plt.ylabel("评论数目")
            plt.title('餐饮情感极性分布图')
            plt.show()
            plt.close()
def all_display(which):
    if result is not None:
        text.delete(1.0, tk.END)
        comments = result["content"]
        if which == ALL:
            i = 1
            for comment in comments:
                text_tag_config(comment, i)
                i += 1
def all_button_event(which):
    positive_score = 0.5
    negative_score = 0.15
    # 使用关键字找取对应的评论，环境，交通，设施，服务，餐饮
    environment_keywords = ['环境','周边','风景','空气','江景','小区','景点','夜景','街','周围','景区','声音','景色','马路']
    traffic_keywords = ['交通','车程','地段','路程','停车','机场','离','车站','地理','位置','地理','中心','海拔','码头','旁边']
    weight_keywords = ['设施','设备','条件','硬件','房间','马桶','阳台','卫生间','洗手间','空调','被子','床','大厅','电','摆设','水','电','客厅']
    service_keywords = ['服务','态度','前台','服务员','老板','掌柜','店家','工作人员','房东','小姐姐','小哥']
    meal_keywords = ['餐饮','早餐','咖啡','味道','饭','菜','水果','特产','餐','美食','烧烤','宵夜','食材','饭馆','小吃']
    if result is not None:
        text.delete(1.0, tk.END)
        comments = result["content"]
        # 按照评分和情感分数（snownlp展示）展示评论极性分数
        if which == positive:
            j6 = 1
            set_list = []
            for i in comments:
                # 细粒度的文本切割，2870932
                if len(i)>2:
                    for i_1 in re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]").sub('\t', i).split('\t'):
                        set_list.append(i_1)
            for sen in set(set_list):
                if len(sen)>3:
                    s = SnowNLP(sen)
                    score = s.sentiments
                    if score > positive_score:
                        text_tag_config1(sen, j6, score)
                        j6 += 1
        elif which == medium:
            j7 = 1
            set_list = []
            for i in comments:
                # 细粒度的文本切割，2870932
                if len(i)>0:
                    for i_1 in re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]").sub('\t', i).split('\t'):
                        set_list.append(i_1)
            for sen in set(set_list):
                if len(sen) > 3:
                    s = SnowNLP(sen)
                    score = s.sentiments
                    if 0.2 <= score <= 0.5:
                        text_tag_config1(sen, j7, score)
                        j7 += 1
        elif which == negative:
            j8 = 1
            set_list = []
            for i in comments:
                # 细粒度的文本切割，2870932
                if len(i)>0:
                    for i_1 in re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]").sub('\t', i).split('\t'):
                        set_list.append(i_1)
            for sen in set(set_list):
                if len(sen) > 3:
                    s = SnowNLP(sen)
                    score = s.sentiments
                    if score < negative_score:
                        text_tag_config1(sen, j8, score)
                        j8 += 1
        ###################后续分类打分
        elif which == taste_pos:
            j9 = 1
            detail_content = []
            for i in comments:
                if len(i)>3:
                    for i_1 in re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]").sub('\t', i).split('\t'):
                        for keyword in environment_keywords:
                            if keyword in i_1:
                                detail_content.append(i_1)
            for i1 in set(detail_content):
                if len(i1) > 3:
                    s = SnowNLP(i1)
                    ###对符合条件的抓取出来，并计算情感极性
                    score = s.sentiments
                    if score > positive_score:
                        text_tag_config1(i1, j9, score)
                        j9 += 1
        elif which == taste_neg:
            j10 = 1
            detail_content = []
            for i in comments:
                if len(i)>3:
                    for i_1 in re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]").sub('\t', i).split('\t'):
                        for keyword in environment_keywords:
                            if keyword in i_1:
                                detail_content.append(i_1)
            for i1 in set(detail_content):
                if len(i1) > 3:
                    s = SnowNLP(i1)
                    ###对符合条件的抓取出来，并计算情感极性
                    score = s.sentiments
                    if score <= negative_score:
                        text_tag_config1(i1, j10, score)
                        j10 += 1
        elif which == speed_pos:
            j11 = 1
            detail_content = []
            for i in comments:
                if len(i)>3:
                    for i_1 in re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]").sub('\t', i).split('\t'):
                        for keyword in traffic_keywords:
                            if keyword in i_1:
                                detail_content.append(i_1)
            for i1 in set(detail_content):
                if len(i1) > 3:
                    s = SnowNLP(i1)
                    ###对符合条件的抓取出来，并计算情感极性
                    score = s.sentiments
                    if score > positive_score:
                        text_tag_config1(i1, j11, score)
                        j11 += 1
        elif which == speed_neg:
            j12 = 1
            detail_content = []
            for i in comments:
                if len(i)>3:
                    for i_1 in re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]").sub('\t', i).split('\t'):
                        for keyword in traffic_keywords:
                            if keyword in i_1:
                                detail_content.append(i_1)
            for i1 in set(detail_content):
                if len(i1) > 3:
                    s = SnowNLP(i1)
                    ###对符合条件的抓取出来，并计算情感极性
                    score = s.sentiments
                    if score <= negative_score:
                        text_tag_config1(i1, j12, score)
                        j12 += 1
        elif which == weight_pos:
            j13 = 1
            detail_content = []
            for i in comments:
                if len(i)>3:
                    for i_1 in re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]").sub('\t', i).split('\t'):
                        for keyword in weight_keywords:
                            if keyword in i_1:
                                detail_content.append(i_1)
            for i1 in set(detail_content):
                if len(i1) > 3:
                    s = SnowNLP(i1)
                    ###对符合条件的抓取出来，并计算情感极性
                    score = s.sentiments
                    if score > positive_score:
                        text_tag_config1(i1, j13, score)
                        j13 += 1
        elif which == weight_neg:
            j14 = 1
            detail_content = []
            for i in comments:
                if len(i)>3:
                    for i_1 in re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]").sub('\t', i).split('\t'):
                        for keyword in weight_keywords:
                            if keyword in i_1:
                                detail_content.append(i_1)
            for i1 in set(detail_content):
                if len(i1) > 3:
                    s = SnowNLP(i1)
                    ###对符合条件的抓取出来，并计算情感极性
                    score = s.sentiments
                    if score <= negative_score:
                        text_tag_config1(i1, j14, score)
                        j14 += 1
        elif which == service_pos:
            j15 = 1
            detail_content = []
            for i in comments:
                if len(i)>3:
                    for i_1 in re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]").sub('\t', i).split('\t'):
                        for keyword in service_keywords:
                            if keyword in i_1:
                                detail_content.append(i_1)
            for i1 in set(detail_content):
                if len(i1) > 3:
                    s = SnowNLP(i1)
                    ###对符合条件的抓取出来，并计算情感极性
                    score = s.sentiments
                    if score > positive_score:
                        text_tag_config1(i1, j15, score)
                        j15 += 1
        elif which == service_neg:
            j16 = 1
            detail_content = []
            for i in comments:
                if len(i)>3:
                    for i_1 in re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]").sub('\t', i).split('\t'):
                        for keyword in service_keywords:
                            if keyword in i_1:
                                detail_content.append(i_1)
            for i1 in set(detail_content):
                if len(i1) > 3:
                    s = SnowNLP(i1)
                    ###对符合条件的抓取出来，并计算情感极性
                    score = s.sentiments
                    if score <= negative_score:
                        text_tag_config1(i1, j16, score)
                        j16 += 1
        elif which == price_pos:
            j17 = 1
            detail_content = []
            for i in comments:
                if len(i)>3:
                    for i_1 in re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]").sub('\t', i).split('\t'):
                        for keyword in meal_keywords:
                            if keyword in i_1:
                                detail_content.append(i_1)
            for i1 in set(detail_content):
                if len(i1) > 3:
                    s = SnowNLP(i1)
                    ###对符合条件的抓取出来，并计算情感极性
                    score = s.sentiments
                    if score > positive_score:
                        text_tag_config1(i1, j17, score)
                        j17 += 1
        elif which == price_neg:
            j18 = 1
            detail_content = []
            for i in comments:
                if len(i)>3:
                    for i_1 in re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]").sub('\t', i).split('\t'):
                        for keyword in meal_keywords:
                            if keyword in i_1:
                                detail_content.append(i_1)
            for i1 in set(detail_content):
                if len(i1) > 3:
                    s = SnowNLP(i1)
                    ###对符合条件的抓取出来，并计算情感极性
                    score = s.sentiments
                    if score <= negative_score:
                        text_tag_config1(i1, j18, score)
                        j18 += 1
root = tk.Tk()
# 增加图片
canvas = tk.Canvas(root, width=443, height=200, bd=0, highlightthickness=0)
imgpath = 'pic/1.jpeg'
img = Image.open(imgpath)
photo = ImageTk.PhotoImage(img)
canvas.create_image(230, 30, image=photo)
canvas.pack()
root.resizable(False, False)
# 开始文本处理
frame1 = tk.Frame(root, bd=1, relief=tk.SUNKEN)
frame1.pack(fill=tk.BOTH, expand=tk.YES, anchor=tk.CENTER)
# 输入框定义
row_num = 0
url_tv = tk.StringVar()
url_tv_column_span = 9
tk.Entry(frame1,textvariable=url_tv).grid(
    row=row_num, column=0, columnspan=url_tv_column_span,padx=2, sticky=all_direction)
####绑定按钮事件，将采集绑定到多线程开始采集按钮
tk.Button(frame1, text="开始采集",command=data_collecting).grid(
    row=row_num, column=url_tv_column_span, sticky=all_direction)
row_num = 1
prompt_text = tk.StringVar()
tk.Label(frame1, textvariable=prompt_text).grid(row=row_num, column=0, columnspan=8, pady=5, sticky=all_direction)
prompt_text.set("请在上面输入数据采集的链接，携程和美团民宿已开通")
# 设置按钮
row_num = 2
columnspan = 2
tk.Button(frame1, text="所有评论展示", command=lambda: all_display(ALL)).grid(
    row=row_num, column=columnspan * 0, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
##使用commands绑定动作
tk.Button(frame1, text="总体情感趋势", command=lambda: emotion_analysis(ALL1)).grid(
    row=row_num, column=columnspan * 1, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
tk.Button(frame1, text="积极评论分析", command=lambda: all_button_event(positive)).grid(
    row=row_num, column=columnspan * 2, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
tk.Button(frame1, text="一般评论分析", command=lambda: all_button_event(medium)).grid(
    row=row_num, column=columnspan * 3, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
tk.Button(frame1, text="消极评论分析", command=lambda: all_button_event(negative)).grid(
    row=row_num, column=columnspan * 4, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
row_num = 3
tk.Button(frame1, text="环境积极评论", command=lambda: all_button_event(taste_pos)).grid(
    row=row_num, column=columnspan * 0, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
tk.Button(frame1, text="交通积极评论", command=lambda: all_button_event(speed_pos)).grid(
    row=row_num, column=columnspan * 1, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
tk.Button(frame1, text="设施积极评论", command=lambda: all_button_event(weight_pos)).grid(
    row=row_num, column=columnspan * 2, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
tk.Button(frame1, text="服务积极评论", command=lambda: all_button_event(service_pos)).grid(
    row=row_num, column=columnspan * 3, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
tk.Button(frame1, text="餐饮积极评论", command=lambda: all_button_event(price_pos)).grid(
    row=row_num, column=columnspan * 4, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
row_num = 4
tk.Button(frame1, text="环境消极评论", command=lambda: all_button_event(taste_neg)).grid(
    row=row_num, column=columnspan * 0, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
tk.Button(frame1, text="交通消极评论", command=lambda: all_button_event(speed_neg)).grid(
    row=row_num, column=columnspan * 1, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
tk.Button(frame1, text="设施消极评论", command=lambda: all_button_event(weight_neg)).grid(
    row=row_num, column=columnspan * 2, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
tk.Button(frame1, text="服务消极评论", command=lambda: all_button_event(service_neg)).grid(
    row=row_num, column=columnspan * 3, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
tk.Button(frame1, text="餐饮消极评论", command=lambda: all_button_event(price_neg)).grid(
    row=row_num, column=columnspan * 4, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
row_num = 5
tk.Button(frame1, text="环境情感趋势", command=lambda: emotion_pic(taste)).grid(
    row=row_num, column=columnspan * 0, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
tk.Button(frame1, text="交通情感趋势", command=lambda: emotion_pic(speed)).grid(
    row=row_num, column=columnspan * 1, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
tk.Button(frame1, text="设施情感趋势", command=lambda: emotion_pic(weight)).grid(
    row=row_num, column=columnspan * 2, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
tk.Button(frame1, text="服务情感趋势", command=lambda: emotion_pic(service)).grid(
    row=row_num, column=columnspan * 3, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
tk.Button(frame1, text="餐饮情感趋势", command=lambda: emotion_pic(price)).grid(
    row=row_num, column=columnspan * 4, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
#统计分析
frame0 = tk.LabelFrame(root, text="评论数字图表区", padx=2, pady=2, relief=tk.GROOVE)
frame0.pack(fill=tk.BOTH, expand=tk.YES)
columnspan = 7
# 调节按钮之间的行距，可视化文本之中的数据
##交通时间汇总，推荐商品汇总，终端分布，质量分布，按钮绑定事件，row表示行数
tk.Button(frame0, text="顾客情感分布", command=lambda: picturing.score_detail(result)).grid(
    row=1, column=columnspan * 4, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
tk.Button(frame0, text="顾客打分统计", command=lambda: picturing.average_score(result)).grid(
    row=1, column=columnspan * 0, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
tk.Button(frame0, text="入住时间序列", command=lambda: picturing.s_from(result)).grid(
    row=1, column=columnspan * 1, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
tk.Button(frame0, text="民宿标签分析", command=lambda: picturing.recommend_dishes2(result)).grid(
    row=1, column=columnspan * 2, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
tk.Button(frame0, text="民宿复住分析", command=lambda: picturing.cost_time(result)).grid(
    row=1, column=columnspan * 3, columnspan=columnspan, padx=2, pady=2, sticky=all_direction)
# 开始文本处理
frame2 = tk.Frame(root, bd=1, relief=tk.SUNKEN)
frame2.pack(fill=tk.BOTH, expand=tk.YES, anchor=tk.CENTER)
row_num = 5
#文本框更改hight和width更改大小
text = tk.Text(frame2, height=30, width=56)
text.grid(row=row_num, column=0, columnspan=11, padx=10, pady=10)
scrollbar = tk.Scrollbar(frame2, orient=tk.VERTICAL, command=text.yview)
scrollbar.grid(row=row_num, column=11, rowspan=1, sticky=all_direction)
text.configure(yscrollcommand=scrollbar.set)
root.title('CarryChang_实时意见挖掘程序')
root.mainloop()