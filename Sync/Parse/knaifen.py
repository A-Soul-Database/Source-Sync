import requests
from . import Base
#import Base
from lxml import etree


class knaifen(Base.BaseModel):

    def __init__(self,url:str="knaifen.workers.dev") -> None:
        super().__init__(url)
        assert ("asoul-rec.com" in self.Acquire_Url) or ("knaifen.workers.dev" in self.Acquire_Url), "The url is not supported"

    def Parse_Url(self) -> None:
        r = requests.get(self.Acquire_Url)
        r.encoding = 'utf-8'
        try: self.Download_Url = r.text.split('new Artplayer(')[1].split("url: '")[1].split("',")[0]
        except: self.Download_Url = ""

    def Lister(self):
        # 返回Url列表
        def Get_List(url):
            # 解析奶粉罐的列表
            l = requests.get(url)
            l.encoding = 'utf-8'
            _list = etree.HTML(l.text).xpath('//a[@class="item"]/@href')
            return [url + i for i in _list]
        
        Record_Dict_Url , Record_Item_UrI, Record_Item_URL = ["https://asoul1.asoul-rec.com/ASOUL-REC-一周年","https://asoul1.asoul-rec.com/ASOUL-REC-二周年"] , [], []

        for k in Record_Dict_Url: Record_Item_UrI.extend(Get_List(k))
        
        for _k in Record_Item_UrI: _k in [".mp4",".flv",".mov"] and Record_Item_URL.append({'Name':_k.split("/")[-1].split(".")[0],'Url':_k})

        return Record_Item_URL # 返回列表