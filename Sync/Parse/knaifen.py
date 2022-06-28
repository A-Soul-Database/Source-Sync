import requests
from . import Base
#import Base
from lxml import etree


class knaifen(Base.BaseModel):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36 AsdbRangeDownloaderv1"}

    def __init__(self) -> None:
        ...

    def Parse_Url(self) -> None:
        r = requests.get(self.Acquire_Url,headers=self.headers,timeout=10)
        r.encoding = 'utf-8'
        #print(r.text)
        try: self.Download_Url , self.Download_Url_Args = r.text.split('new Artplayer(')[1].split("url: '")[1].split("',")[0] , ""
        except Exception as e: print(f"Error {e} , {r.text}")

    def Lister(self):
        # 返回Url列表
        Sourcer = {
            "21Centry":"https://asoul.asoul-rec.com/",
            "OD":"https://asoul1.asoul-rec.com",
            "DDIndex":"https://rec.ddindexs.com",
        }
        def Get_List(url):
            # 解析奶粉罐的列表
            l = requests.get(Sourcer["OD"]+url,timeout=10)
            l.encoding = 'utf-8'
            _list = etree.HTML(l.text).xpath('//a[@class="item"]/@href')
            return [f"{Sourcer['DDIndex']}{url}/{i.split('/')[-1]}" for i in _list] # 奶粉的路径为相对路径,应该为Host+Path
        
        Record_Dict_Url , Record_Item_UrI, Record_Item_URL = ["/ASOUL-REC-一周年","/ASOUL-REC-二周年"] , [], []
        
        for k in Record_Dict_Url: Record_Item_UrI.extend(Get_List(k))

        for _k in Record_Item_UrI: (_k.split(".")[-1] in ["mp4","flv","mov"])and Record_Item_URL.append({'Name':_k.split("/")[-1],'Url':_k,'Sourcer':self.__Sourcer__()})

        return Record_Item_URL # 返回列表

    def Change_Url(self, url):
        assert ("asoul-rec.com" in url) or ("knaifen.workers.dev" in url) or ("ddindexs.com" in url), "The url is not supported"
        return super().Change_Url(url)

    def __Sourcer__(self):
        return "@珈然小姐的奶粉罐"

    def __get_Random_Range__(self):
        return [800,2400]