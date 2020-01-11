import re
import json
import requests
# from fake_useragent import UserAgent
class Crawler:
    def __init__(self):
        self.base_url = 'https://minsu.meituan.com/gw/ugc/api/v1/product/comments?productId=%s&pageNow=%s&pageSize=1000'
        self.shop_id = None
        self.page_num = 1
        self.info = {}
    def crawl(self, url=None, shop_id=None):
        self._get_shop_id(url, shop_id)
        self._get_json_request(self.base_url % (self.shop_id, 1))
        # self.page_num = 1
        # self._filter()
        return self.info
    @staticmethod
    def _is_too_short(sentence):
        #########过滤文本字数
        if len(sentence) < 2:
            return True
        if len(re.findall(r'[\u4e00-\u9fa5]', sentence)) <= len(sentence) * 0.4:
            return True
        return False
    @staticmethod
    def _is_numeric(sentence):
        match = re.findall("\d+", sentence)
        if match is not None and sum([len(m) for m in match]) >= len(sentence) * 0.75:
            return True
        return False
    @staticmethod
    def _is_english(sentence):
        match = re.findall("[a-zA-Z]+", sentence)
        if match is not None and sum([len(m) for m in match]) >= len(sentence) * 0.75:
            return True
        return False
    @staticmethod
    def _is_word_repeat(sentence):
        repeat_words, length = [], 0
        for word in sentence:
            times = sentence.count(word)
            if times >= 4 and word not in repeat_words:
                repeat_words.append(word)
                length += times
        if length > len(sentence) / 2:
            return True
        return False
    def _get_shop_id(self, url, id):
        if url is not None:
            # 匹配出数字即可
            if 'rank' in url:
                shop_id = re.findall('/housing/(.*)/', url)[0]
                self.shop_id = shop_id
            else:
                shop_id = re.search("\d+", url)
                if shop_id is None:
                    raise ValueError("Bad url")
                self.shop_id = shop_id.group()
        elif id is not None:
            self.shop_id = id
        else:
            raise ValueError("Bad url")
    def _get_json_request(self, url):
        try:
            # print(url)
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                'Cookie': 'zgwww=93b60120-342e-11ea-8352-7929dfe9c6a2; uuid=D51492DA6AAA270A8B7FE7A35B3B94DD39666FAF2EAABB2A10B5B4413F03334A; iuuid=D51492DA6AAA270A8B7FE7A35B3B94DD39666FAF2EAABB2A10B5B4413F03334A; _lxsdk_cuid=16f92f4f879c8-040cf5ba938711-353166-1fa400-16f92f4f879c8; _lxsdk=D51492DA6AAA270A8B7FE7A35B3B94DD39666FAF2EAABB2A10B5B4413F03334A; __mta=147626248.1578718526069.1578718542593.1578718605961.3; XSRF-TOKEN=eldkyp20-QuUkBlhveN5L5ovat5brDFCGXe0',
                'Host': 'minsu.meituan.com',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
            }
            result = requests.get(url, headers=headers)
        except requests.ConnectionError:
            raise ValueError("requests.ConnectionError")
        content = json.loads(result.text)
        # print(content)
        result = content["data"]
        self._get_initial_info(result)
        content = result["list"]
        for a_json in content:
            self._get_a_json_info(a_json)
    def _get_initial_info(self, result):
        self.info["content"] = []
        self.info["score"] = []
        self.info["totalScoreDesc"] = []
        self.info["commentTextList"] = []
        self.info["hostReply"] = []
        self.info["guestId"] = []
        self.info["gmtCreate"] = []
    def _get_a_json_info(self, a_json):
        try:
            self.info["score"].append(int(a_json["totalScore"]/10))
        except:
            self.info["score"].append([])
        try:
            self.info["content"].append(a_json["body"])
        except:
            self.info["content"].append([])
        try:
            self.info["commentTextList"].append(a_json["commentTextList"])
        except:
            self.info["commentTextList"].append([])
        try:
            self.info["totalScoreDesc"].append(a_json["totalScoreDesc"])
        except:
            self.info["totalScoreDesc"].append([])
        try:
            self.info["guestId"].append(a_json["guestId"])
        except:
            self.info["guestId"].append([])
        try:
            self.info["gmtCreate"].append(a_json["gmtCreate"])
        except:
            self.info["gmtCreate"].append([])
        try:
            self.info["hostReply"].append(a_json["hostReply"])
        except:
            self.info["hostReply"].append([])
_crawler = Crawler()
crawl = _crawler.crawl
if __name__ == "__main__":
    shop_id = 'https://minsu.meituan.com/housing/9080714/'
    crawler = Crawler()
    a = crawler.crawl(shop_id)