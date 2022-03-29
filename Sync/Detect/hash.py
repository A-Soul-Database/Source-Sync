"""
利用cv每隔一定时间截取一帧并保存
From https://github.com/A-Soul-Database/PhotoSearch/commit/1e6e72c3f9e7a26e8652ac21bb4fe26eaf64ae64
"""
from sys import stderr
import imagehash
from PIL import Image
import distance
import json
import subprocess
import time
import os

Config = {
    "Hash_Size":12,
    "Search_Distance":25,
    "Confidence_Distance":10,
}


def splitDict(m:dict,clips:int)->list:
    """
    将字典按片段分割
    :param m:
    :return:
    """
    new_list = []
    dict_len = len(m)
    # 获取分组数
    while_count = dict_len // clips + 1 if dict_len % clips != 0 else dict_len / clips
    split_start = 0
    split_end = clips
    while(while_count > 0):
        new_list.append({k: m[k] for k in list(m.keys())[split_start:split_end]})
        split_start += clips
        split_end += clips
        while_count -= 1
    return new_list

class Search:

    def ultraSearch(self,image:str):
        """
        优化处: 
                1:多线程
                2:分割前两个hash
        """
        result = {}
        to_search_hash = imagehash.phash(Image.open(f'{image}'),hash_size=Config["Hash_Size"]).__str__()
        hashinfo = json.loads(open(f"./Alphas/{to_search_hash[:1]}.json","r").read()) if __name__ == "__main__" else json.loads(open(f"./Sync/Detect/Alphas/{to_search_hash[:1]}.json","r",encoding="utf-8").read())
        for i in hashinfo:
            distancse = int(distance.hamming(to_search_hash,i))
            if distancse < Config["Search_Distance"]:
                result[hashinfo[i]]=f"Confidences: {round(1-distancse/len(to_search_hash),2)}"
                if distancse < Config["Confidence_Distance"]:
                    break
        
        result= sorted(result.items(), key=lambda d:d[1],reverse=True)
        try:
    
            result,confidence = list(dict(result).items())[0][0],list(dict(result).items())[0][1]
            return {
                "signal":True,
                "bv":result.split("-")[0] if "-" in result else result.split(",")[0],
                "time":float(result.split(",")[1]),"p":"1" if "-" not in result else result.split("-")[-1].split(",")[0],
                "confidence":float(confidence.split(":")[1])
                }
        except:
            return {"signal":False}
        # 只返回第一个 返回实例: BVxxxxx-2,123.0 / BVxxxx,123
        # Bv号-分P,时间点

def Do_Detect(url,Args,Time_Scales:list=[],Single_Type_Secs:int=0,Delay:int=0.5,Single_Type:bool=False):

    def Screenshot(Down_Url,args,Secs):
        # 指定某一秒截图
        return subprocess.Popen('ffmpeg -y {} -ss {}  -i "{}"  -vframes 1 output.png'.format(args,Secs,Down_Url),shell=True)
    
    def Screenshots(Down_url,Args,Time_Scales):
        # 指定某一时间段截图
        p = subprocess.Popen(f'ffmpeg -y {Args} -ss {Time_Scales[0]} -i "{Down_url}" -to {Time_Scales[1]-Time_Scales[0]} -avoid_negative_ts 1 -c copy "tmp.mp4"',
            stderr=subprocess.DEVNULL,stdout=subprocess.DEVNULL)
        p.wait()
        return subprocess.Popen('ffmpeg -y -i tmp.mp4 -vf fps=1 out%d.png'
            ,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,shell=True).wait()

    def Acquire_Source():
        # 根据某张图片搜索视频及秒数
        return Search().ultraSearch("output.png")
    
    def Acquire_Source_List():
        # 根据某一时间段搜索视频及秒数
        Results = []
        for i in os.listdir("./"):
            if i.endswith(".png"): Results.append(Search().ultraSearch(i))
        os.remove("tmp.mp4")
        for i in os.listdir("./"):
            if i.endswith(".png"): os.remove(i)
        return Results

    time.sleep(Delay)
    
    if Single_Type: 
        try:
            Screenshot(url,Args,Single_Type_Secs)
            return Acquire_Source()
        except: return {"signal":False}
    else:
        try:
            Screenshots(url,Args,Time_Scales)
            return Acquire_Source_List()
        except: return {"signal":False} #防止网络错误

def Do_Clear():
    # 清理临时文件
    for i in os.listdir("./"):
        if i.endswith(".png"): os.remove(i)
    os.remove("tmp.mp4")

if __name__ == "__main__":
    a = Do_Detect("http://localhost/1.mp4","",[0,50])
    print(a)
    '''
    imgs = input("Please input the path you want to search:\n")
    a = Search().ultraSearch(imgs)
    print(a)
    '''