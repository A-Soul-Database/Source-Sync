from ast import Compare
import requests
import os
import json
from lxml import etree
from PhotoSearch.oped import main as oped
import time
import jieba
import numpy as np
import jieba.analyse
import itertools
Config = {
    "Sources":["Jiabu","Naifen","Ofiicial"]
}
'''
# Detect Sources 
if requests.get("http://localhost:4399/ping").status_code != 200 and requests.get("http://localhost:4400/ping").status_code != 200:
    os._exit(128)
'''

# AnalySis
class Base:
    def __init__(self):
        self.info = []
        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0"}
        self.Delete_Words = ["向晚","贝拉","珈乐","嘉然","乃琳","A-SOUL","【","】","夜谈","小剧场","游戏室","/","直播录像","直播回放","3D","B限",".mp4"," ","团播"] 
        #self.Delete_Words = ["【","】","/","直播录像","直播回放","3D","B限",".mp4"," ","团播"] 

    def _load_saved(self):
        return json.loads(open(f"{self.__class__.__name__}.SourceList","r",encoding="utf-8").read())

    def _save_json(self):
        open(f"{self.__class__.__name__}.SourceList","w",encoding='utf-8').write(json.dumps(self.info,ensure_ascii=False,sort_keys=True,indent=4))
    
    def replace_foribbden(self,text):
        for word in self.Delete_Words:
            text = text.replace(word,"")
        return text

class Naifen(Base):
    def __init__(self,name:str=""):
        super().__init__()
        self.name = name
    
    def Generate_All_Info(self):
        url = "https://asoul1.asoul-rec.com/ASOUL-REC/"
        elements = etree.HTML(requests.get(url).content)
        urls = elements.xpath('//a[@class="item"]/@href')
        for i in urls:
            if ".mp4" not in i:
                continue
            item = i.split("/")[-1].split(" ")
            date = item[0] # 2020.12.xx
            try:
                title = item[-1]
                etc = self.replace_foribbden(''.join(item[1:]))
            except:
                title = ""
                etc = ""
            self.info.append({"title":etc,"url":f"https://asoul1.asoul-rec.com{i}","date":date})

class Official(Base):
    """Theroetically this Class Fits For any type of Bilibili Auto Live record"""
    uids = {"A":{"uid":"672346917","series_id":"222748"},"B":{"uid":"672353429","series_id":"222938"},"C":{"uid":"351609538","series_id":"222746"},"D":{"uid":"672328094","series_id":"222940"},"E":{"uid":"672342685","series_id":"222754"},"F":{"uid":"703007996","series_id":"223583"}}
    def Generate_All_Info(self):
        for _k,v in self.uids.items():
            pn = 1
            while True:
                lists = requests.get(f"https://api.bilibili.com/x/series/archives?mid={v['uid']}&series_id={v['series_id']}&pn={pn}",headers=self.headers).json()["data"]
                if lists['aids'] == None:
                    print(f"Got {_k}")
                    break
                for item in lists["archives"]:
                    title = self.replace_foribbden(item["title"])

                    _tmp = []
                    _title_tmp = title[::-1]
                    date = "20" + _title_tmp[_title_tmp.find("日"):_title_tmp.find("02",_title_tmp.find("年"))].replace("年",".").replace("月",".").replace("日","")[::-1]
                    for i in date.split("."):
                        if len(i) == 1 : i = "0"+ i 
                        _tmp.append(i)
                    date = ".".join(_tmp)
                    
                    self.info.append({"title":title[:title.find("20")],"url":f"https://www.bilibili.com/video/{item['bvid']}","date":date})
                pn+=1
                time.sleep(1)

class Jiabu(Base):
    uid = "393396916"
    def __init__(self) -> None:
        super().__init__()
        
    def Generate_All_Info(self):
        pn = 1
        while True:
            lists = requests.get(f"https://api.bilibili.com/x/space/arc/search?mid={self.uid}&ps=30&pn={pn}",headers=self.headers).json()["data"]["list"]["vlist"]
            for item in lists:
                if "【直播录像】" not in item["title"]:
                    continue
                try:
                    _tmp = []
                    for i in [fn for fn in item["description"].split("\n") if "直播日期" in fn][0].split("：")[-1].replace("年",".").replace("月",".").replace("日","").split('.'):
                        if len(i) == 1: i = "0"+i
                        _tmp.append(i)
                    date = '.'.join(_tmp)
                except:
                    date = time.strftime("%Y.%m.%d",time.localtime(item["created"]))
                finally:
                    _tmp = '.'.join(date.split(".")[1:])
                    title = self.replace_foribbden(item["title"]).replace(date,"").replace(_tmp,"")
                self.info.append({"title":title,"url":f"https://www.bilibili.com/video/{item['bvid']}","date":date})
            if len(lists) == 0:
                break
            pn+=1
            time.sleep(1)

class Link_Items:
    Compare_Info = []

    def Add_Info(self,infoA:dict):
        self.Compare_Info.append(infoA)

    def Link_Info(self):
        Compare_Info = self._get_Compare_info()
        Link,Combine = [],[]

        for _listA, _listB in itertools.combinations(Compare_Info,2):
            for _listA_item, _listB_item in itertools.product(_listA,_listB):
                if _listA_item["date"] == _listB_item["date"]:
                    a,b = simhash(_listA_item["title"]), simhash(_listB_item["title"])
                    if a.hammingDis(b) < 20: Link.append([_listA_item,_listB_item])
        
        for _listingA , _listingB in itertools.combinations(Link,2):
            _listing = []
            for _listingA_item, _listingB_item in itertools.product(_listingA,_listingB):
                if _listingA_item["url"] == _listingB_item["url"]:
                    # Put listing B into listing A
                    _listingB.remove(_listingB_item)
                    _listing = _listingA + _listingB
                    Combine.append(_listing)
                    # Remove listing B

        return Combine


    def _get_Compare_info(self):
        return self.Compare_Info

class simhash:
    # Source: CSDN@madujin
    def __init__(self,content):
        self.simhash=self.simhash(content)
 
    def __str__(self):
        return str(self.simhash)
 
    def simhash(self,content):
        seg = jieba.cut(content)
        #jieba.analyse.set_stop_words('stopword.txt')
        keyWord = jieba.analyse.extract_tags(
            '|'.join(seg), topK=20, withWeight=True, allowPOS=())
        keyList = []
        # print(keyWord)
        for feature, weight in keyWord:
            weight = int(weight * 20)
            feature = self.string_hash(feature)
            temp = []
            for i in feature:
                if(i == '1'):
                    temp.append(weight)
                else:
                    temp.append(-weight)
            # print(temp)
            keyList.append(temp)
        list1 = np.sum(np.array(keyList), axis=0)
        #print(list1)
        if(keyList==[]): #编码读不出来
            return '00'   
        simhash = ''
        for i in list1:
            if(i > 0):
                simhash = simhash + '1'
            else:
                simhash = simhash + '0'
        return simhash
 
 
    def string_hash(self,source):
        if source == "":
            return 0
        else:
            x = ord(source[0]) << 7
            m = 1000003
            mask = 2 ** 128 - 1
            for c in source:
                x = ((x * m) ^ ord(c)) & mask
            x ^= len(source)
            if x == -1:
                x = -2
            x = bin(x).replace('0b', '').zfill(64)[-64:]
            #print(source,x)
            return str(x)
 
 
    def hammingDis(self,com):
        t1 = '0b' + self.simhash
        t2 = '0b' + com.simhash
        n=int(t1, 2) ^ int(t2, 2)
        i=0
        while n:
            n &= (n-1)
            i+=1
        return i

def do_sync():
    a,b,c = Jiabu(),Official(),Naifen()
    a.Generate_All_Info(),b.Generate_All_Info(),c.Generate_All_Info()
    a._save_json(),b._save_json(),c._save_json()

if __name__ == "__main__":
    test,a,b,c = Link_Items(),Jiabu(),Official(),Naifen()
    test.Add_Info(a._load_saved()),test.Add_Info(b._load_saved()),test.Add_Info(c._load_saved())
    test._get_Compare_info()
    print(test.Link_Info())