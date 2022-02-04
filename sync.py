import requests
import os
import json
from lxml import etree
import ps.oped as oped
import time
import re

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
        self.Delete_Words = ["向晚","贝拉","珈乐","嘉然","乃琳","A-SOUL","【","】","夜谈","小剧场","游戏室","/","直播录像","直播回放","3D","B限",".mp4"," ","团播","！","!","?","？","_"] 
        self.Delete_Words = []
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
            if ".mp4" not in i or "录屏" in i:
                continue
            item = i.split("/")[-1].split(" ")
            date = item[0] # 2020.12.xx
            self.info.append({"title":i,"url":f"https://asoul1.asoul-rec.com{i}","date":date})

class Official(Base):
    """Theroetically this Class Fits For any type of Bilibili Auto Live record"""
    uids = {"A":{"uid":"672346917","series_id":"222748","name":"向晚"},"B":{"uid":"672353429","series_id":"222938","name":"贝拉"},"C":{"uid":"351609538","series_id":"222746","name":"珈乐"},
    "D":{"uid":"672328094","series_id":"222940","name":"嘉然"},"E":{"uid":"672342685","series_id":"222754","name":"乃琳"},"F":{"uid":"703007996","series_id":"223583","name":""}}
    def Generate_All_Info(self):
        date_pattern = re.compile(r'[0-9]*年[0-9]*月[0-9]*')
        title_pattern = re.compile(r'[0-9]*年[0-9]*月[0-9]*日[0-9]*点场')
        for _k,v in self.uids.items():
            pn = 1
            while True:
                lists = requests.get(f"https://api.bilibili.com/x/series/archives?mid={v['uid']}&series_id={v['series_id']}&pn={pn}",headers=self.headers).json()["data"]
                if lists['aids'] == None:
                    break
                for item in lists["archives"]:
                    title = self.replace_foribbden(item["title"])
                    date = '.'.join([(lambda c : "0" + c if len(c) == 1 else c)(fn) for fn in date_pattern.findall(title)[0].replace("年",".").replace("月",".").split('.')])
                    self.info.append({"title":f"{title_pattern.sub('',title)}","url":f"https://www.bilibili.com/video/{item['bvid']}","date":date})
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

class Record_Info:
    def _down_vid(self,url:str,timescale:list):
        Parse = requests.post("http://localhost:4400/Parse",json={"url":url}).json()
        Uniq_Id = requests.post("http://localhost:4400/Seek",json={"Start_Time":timescale[0],"End_Time":timescale[1],
        "url":Parse["Download_Url"],"Save_Name":Parse["Save_Name"],"Args":Parse["Args"]}).text
        while True:
            Progresses = requests.get(f"http://localhost:4400/Progress").json()[Uniq_Id]
            Finished = True
            for thread_item in Progresses:
                if thread_item["Running"] != 3:
                    Finished = False
            if Finished: return True
    
    def _Record_op(self,path:str):
        pass

    def _Record_Continus_Frame(self,path):
        pass

def do_sync():
    a,b,c = Jiabu(),Official(),Naifen()
    a.Generate_All_Info(),b.Generate_All_Info(),c.Generate_All_Info()
    a._save_json(),b._save_json(),c._save_json()

if __name__ == "__main__":
    do_sync()