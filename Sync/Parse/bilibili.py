from . import Base
#import Base
import requests
import time

class BiliBili(Base.BaseModel):

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36","Refer":"https://www.bilibili.com/"}
    Download_Url_Args = ' -user_agent "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36" -headers "Referer:https://www.bilibili.com/" '
    # ffmpeg 和 requests 需要的UA和Refer值,防止403

    def __init__(self, url):
        super().__init__(url)
        if "bilibili" in self.Acquire_Url : self.bv = self.Acquire_Url.split("/")[-1].split("?")[0]
        else:
            self.bv = self.Acquire_Url
            self.Acquire_Url = f"https://www.bilibili.com/video/{self.bv}"

    def Parse_Url(self):
        Bv_Info = requests.get(f"https://api.bilibili.com/x/web-interface/view?bvid={self.bv}",headers=self.headers).json()
        cid = Bv_Info["data"]["pages"][0]["cid"] #默认p1
        self.Download_Url = requests.get(f"https://api.bilibili.com/x/player/playurl?bvid={self.bv}&cid={cid}&otype=json&&platform=html5&high_quality=1",headers=self.headers).json()["data"]["durl"][0]["url"]


class Normal_Uid(BiliBili):
    # 第三方录播组的账号解决方法
    # 对于不同的录播组,在标题判断,弹幕分P等功能需要单独实现
    uids = ["547510303"]
    def __init__(self,url):
        super().__init__(url)
        

    def Lister(self):
        # https://api.bilibili.com/x/v2/medialist/resource/list?type=1&oid={}&otype=2&biz_id=393396916&ps=30
        # oid:列表最后一位的av号 
        # biz_id:播放列表id type=1时为uid,代表所有投稿视频; type=5时为直播录像,biz_id为合集列表
        ...
    
    def roll_series_list(self,biz_id:str,oid:str="",returns:list=[]):
        time.sleep(0.1)
        _info = requests.get(f"https://api.bilibili.com/x/v2/medialist/resource/list?type=1&oid={oid}&otype=2&biz_id={biz_id}&ps=30",headers=self.headers).json()
        for i in _info["data"]["media_list"]:
            returns.append({"Name":i["title"],"Url":f"https://www.bilibili.com/{i['bv_id']}"}) # 遍历列表中的元素

        if _info["data"]["has_more"]:self.roll_series_list(biz_id,_info["data"]["media_list"][-1]["id"],returns) # 如果列表没有循环完毕,则继续循环
        return returns


class Official(BiliBili):
    # 官方账号的视频列表
    uids = [
        "672342685","672328094","351609538","672353429","672346917","703007996"
    ]
    def __init__(self,url):
        super().__init__(url)
    
    def Lister(self):
        series_ids , bvs = [] , []
        for i in self.uids:
            series_info = requests.get(f"https://api.bilibili.com/x/polymer/space/seasons_series_list?mid={i}&page_num=1&page_size=20",headers=self.headers).json()
            series_lists = series_info["data"]["items_lists"]["series_list"]
            for _item in series_lists:
                if _item["meta"]["name"] == "直播回放":series_ids.append(_item["meta"]["series_id"])
                break
        
        for _item in series_ids: bvs += self.roll_series_list(_item)

        return bvs
    
    def roll_series_list(self,biz_id:str,oid:str="",returns:list=[]):
        time.sleep(0.1)
        _info = requests.get(f"https://api.bilibili.com/x/v2/medialist/resource/list?type=5&oid={oid}&otype=2&biz_id={biz_id}&ps=30",headers=self.headers).json()
        for i in _info["data"]["media_list"]:
            returns.append({"Name":i["title"],"Url":f"https://www.bilibili.com/{i['bv_id']}"}) # 遍历列表中的元素

        if _info["data"]["has_more"]:self.roll_series_list(biz_id,_info["data"]["media_list"][-1]["id"],returns) # 如果列表没有循环完毕,则继续循环
        return returns
