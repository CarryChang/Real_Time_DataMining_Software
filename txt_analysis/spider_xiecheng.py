import re
import json
import requests
#首先先在输入的地址中提取店铺ID，然后将店铺ID和找到的接口进行匹配得到一个地址链接
##然后将得到的地址链接导入到网络爬虫中去得到json1文件
#最后解析jason文件得到内容
class Crawler:
    def __init__(self):
        #1625734074
        self.shop_id = None
        self.page_index = 0
        self.page_num = 1
        self.info = {}
    def crawl(self, url=None, shop_id=None):
        self._get_shop_id(url, shop_id)
        i = 0
        base_url = 'https://m.ctrip.com/restapi/soa2/12455/json/BnbCommentList'
        while i < self.page_num:
            data = json.dumps(
                {"pid": '{}'.format(self.shop_id), "searchType": 2, "tagId": 0,
                 "pageindex": '{}'.format(i), "pageSize": 40,
                 "order": 0,
                 "head": {"cid": "", "ctok": "", "cver": "1.0", "lang": "01", "sid": "8888", "syscode": "09",
                          "auth": "",
                          "xsid": "", "extension": [{"name": "webp", "value": "1"}, {"name": "cityid", "value": ""},
                                                    {"name": "platform", "value": "pc"},
                                                    {"name": "source", "value": "2"},
                                                    {"name": "pagecode", "value": "10650016818"},
                                                    {"name": "module", "value": "11"}]}})
            self._get_json_request(base_url,data)
            i += 1
        self.page_num = 1
        return self.info
    def _get_shop_id(self, url, id):
        if url is not None and 'onlineinn' in url:
            # 链接整理
            shop_id = re.findall('pid=(.*?)&',url)[0]
            # print(shop_id)
            if shop_id is None:
                raise ValueError("Bad url")
            self.shop_id = shop_id
        elif id is not None:
            self.shop_id = id
        else:
            raise ValueError("Bad url")
    def _get_json_request(self, url,data):
        try:
            headers = {
                'content-type': 'application/json',
                'cookieOrigin': 'https://inn.ctrip.com',
                'Origin': 'https://inn.ctrip.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
            }
            result = requests.post(url, headers=headers,data=data).json()
        except requests.ConnectionError:
            raise ValueError("requests.ConnectionError")
        if self.page_num == 1:
            self._get_initial_info(result)
        self._get_a_json_info(result)
    def _get_initial_info(self, result):
        # 提取输入翻页地址
        self.page_num = result["count"] // 40 + 1
        # print(self.page_num)
        # average_score = {}
        # average_score["average_dish_score"] = float(result["average_dish_score"])
        # average_score["average_service_score"] = float(result["average_service_score"])
        # average_score["average_score"] = float(result["average_score"])
        # self.info["average_score"] = average_score
        # # get the score detail
        # self.info["score_detail"] = result["score_detail"]
        # # get the weeks score
        # weeks_score = {}
        # for key, value in result["weeks_score"].items():
        #     weeks_score[key] = float(value)
        # self.info["weeks_score"] = weeks_score
        # # get the recommend dished
        # self.info["recommend_dishes"] = result["recommend_dishes"]
        # # get the comment num
        # self.info["comment_num"] = result['comment_num']
        # # initialize the self.info variable
        self.info["content"] = []
        self.info["content"] = []
        self.info["score"] = []
        self.info["commentTextList"] = []
        self.info["checkInType"] = []
        self.info["guestId"] = []
        self.info["gmtCreate"] = []
        self.info["levelName"] = []
        for a_json1 in result["bnbCommentTags"]:
            try:
                q1 = a_json1["tagName"]
                q2 = a_json1["popularity"]
                self.info["commentTextList"].append([q1,q2])
            except:
                self.info["commentTextList"].append([])
    def _get_a_json_info(self,result):
        for a_json in result["clist"]:
            try:
                self.info["score"].append(int(a_json["rate"]))
            except:
                self.info["score"].append([])
            try:
                self.info["content"].append(a_json["content"])
            except:
                self.info["content"].append([])
            try:
                self.info["guestId"].append(a_json["uinfo"]['userId'])
            except:
                self.info["guestId"].append([])
            try:
                self.info["levelName"].append(a_json["uinfo"]['levelName'])
            except:
                self.info["levelName"].append([])
            try:
                self.info["gmtCreate"].append(a_json["ctime"])
            except:
                self.info["gmtCreate"].append([])
            try:
                # print(tralvel_type[a_json["checkInType"]])
                # 需要做字典映射：,出游类型：家庭出游，朋友出游，情侣出游，代人预订，商务出差
                # self.info["checkInType"].append(tralvel_type[a_json["checkInType"]])
                self.info["checkInType"].append(a_json["checkInType"])
            except:
                self.info["checkInType"].append([])
_crawler = Crawler()
crawl = _crawler.crawl
if __name__ == "__main__":
    shop_id = 'https://inn.ctrip.com/onlineinn/detail?pid=929393353&channelid=211'
    # print(shop_id)
    crawler = Crawler()
    a = crawler.crawl(shop_id)