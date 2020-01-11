import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文乱码
# 顾客情感分布
def score_detail(result):
    positive_score = 0.5
    negative_score = 0.15
    import re
    from snownlp import SnowNLP
    if result is not None:
        set_list = []
        j1 = 0
        j2 = 0
        j3 = 0
        for i in result['content']:
            # 细粒度的文本切割
            for i_1 in re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]").sub('\t', str(i)).split('\t'):
                set_list.append(i_1)
        for sen in set(set_list):
            if len(sen) > 3:
                s = SnowNLP(sen)
                score = s.sentiments
                if score > positive_score:
                    j1 += 1
                elif negative_score<score <= positive_score:
                    j2 +=1
                else:
                    j3 +=1
        label = ['积极', '一般', '消极']
        label_number = [j1, j2, j3]
        plt.pie(label_number, labels=label,
                autopct="%1.2f%%", shadow=True, startangle=0)
        title = '顾客情感分布'
        plt.title(title, loc="left", fontsize=20)
        plt.axis("equal")
        plt.show()
        plt.close()

#     # 顾客打分分析
def average_score(result):
    if result is not None:
        # 导入json数据
        cost_times = result["score"]
        title = "顾客整体打分分析"
        sources = ("1分", "2分", "3分", "4分", "5分")
        sizes = [0] * len(sources)
        for a_time in cost_times:
            # print(a_time)
            ############使用限定时间
            if a_time <= 1:
                sizes[0] += 1
            elif a_time <= 2:
                sizes[1] += 1
            elif a_time <= 3:
                sizes[2] += 1
            elif a_time <= 4:
                sizes[3] += 1
            else:
                sizes[4] += 1
        the_max = max(sizes)
        the_index = sizes.index(the_max)
        explode = [0, 0, 0, 0, 0]
        explode[the_index] = 0.1
        explode = tuple(explode)
        # 使用饼图
        plt.pie(sizes, labels=sources, explode=explode, autopct="%1.2f%%", shadow=True, startangle=0)
        plt.title(title, loc="left", fontsize=20)
        ####使用正圆
        plt.axis("equal")
        plt.show()
        plt.close()
# 入住时间分析
def s_from(result):
    import time
    dict1 = {}
    if result is not None:
        sfrom = result["gmtCreate"]
        title = "入住时间序列分析"
        for i in sfrom:
            # print(i)
            if '-' in str(i):
                info = i.split('-')
                dt = info[0] + '-' + info[1]
                if dt in dict1.keys():
                    dict1[dt].append(1)
                else:
                    dict1[dt] = []
                    dict1[dt].append(1)
            else:
                timestamp = int(i / 1000)
                time_local = time.localtime(timestamp)
                # 转换成新的时间格式(2016-05-05 20:28:54)
                dt = time.strftime("%Y-%m", time_local)
                if dt in dict1.keys():
                    dict1[dt].append(1)
                else:
                    dict1[dt] = []
                    dict1[dt].append(1)
        # print(dict1)
        label = []
        label_number = []
        # 排序统计
        for i in sorted(dict1, reverse=True):
            label.append(i)
            label_number.append(len(dict1[i]))
        plt.title(title, fontsize=20)
        plt.plot(label, label_number, linestyle='-', marker='*', c='r')
        plt.show()
####民宿标签
def recommend_dishes2(result):
    if result is not None:
        try:
            # 直接计数
            label = []
            label_number = []
            for key in result['commentTextList']:
                if len(key)>1:
                    if len(key[0])>2 and key[1]>0:
                        label.append(key[0])
                        label_number.append(key[1])
            plt.pie(label_number,labels=label,
                    autopct="%1.2f%%", shadow=True, startangle=0)
            plt.title("民宿标签分析", loc="left", fontsize=20)
            plt.axis("equal")
            plt.show()
            plt.close()
        except:
            # 进行统计操作
            dict1 = {}
            for key in result['commentTextList']:
                for key1 in key:
                    if key1 in dict1.keys():
                        dict1[key1].append(1)
                    else:
                        dict1[key1] = []
                        dict1[key1].append(1)
            label = []
            label_number = []
            for key2 in dict1.keys():
                if len(key2) > 2 and len(dict1[key2]) > 0:
                    label.append(key2)
                    label_number.append(len(dict1[key2]))
            plt.pie(label_number, labels=label,
                    autopct="%1.2f%%", shadow=True, startangle=0)
            plt.title("民宿标签分析", loc="left", fontsize=20)
            plt.axis("equal")
            plt.show()
            plt.close()
def cost_time(result):
    if result is not None:
        title = "民宿复住分析"
        # 统计二次以上的，没有为零，使用饼图
        dict1 = {}
        for key1 in result["guestId"]:
            if key1 in dict1.keys():
                dict1[key1].append(dict(url_str=key1))
            else:
                dict1[key1] = []
                dict1[key1].append(dict(url_str=key1))
        y = 0
        n = 0
        for key2 in dict1.keys():
            # 统计回头客的占比
            if len(dict1[key2]) > 1:
                n += 1
            else:
               y += 1
        labels = ['首次', '非首次']
        label_number = [y, n]
        plt.pie(label_number, labels=labels,
                autopct="%1.2f%%", shadow=True, startangle=0)
        plt.title(title, loc="left", fontsize=20)
        plt.axis("equal")
        plt.show()
        plt.close()
def _test():
    from matplotlib import pyplot as plt
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文乱码
    import json
    result = json.loads(open('resource.txt','r',encoding='utf-8').read())
    # 顾客意见完成
    # score_detail(result)
    # 顾客打分完成
    # average_score(result)
    # # 入住时间序列分析完成
    s_from(result)
    # # 顾客标签
    # recommend_dishes2(result)
    # #民宿复住分析完成
    # cost_time(result)
if __name__ == "__main__":
    # 打分分析，回头客统计，guestId,入住时间统计，gmtCreate,意见统计
    pass
    _test()