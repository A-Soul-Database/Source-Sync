import json
import random
import math
import os

Sources = json.loads(open("./sources.json","r",encoding="utf-8").read()) if os.path.exists("./sources.json") else {}

def Search(Name:str):
    # 根据 文件名搜索
    return Sources.get(Name)


def Add_Item(Base:str,Source_Name:str,Url:str,Sourcer:str,Offset:float)->bool:
    # 添加项目
    # Base(主键源): Asdb 中的Bv值; URI: 其他源的路径 ; Sourcer: 来源名称; Time: 时间戳(其他源 - 主键源)
    global Sources
    try:
        if not Sources.get(Base):
            Sources[Base] = []
        Sources[Base].append({"Sourcer":Sourcer,"Url":Url,"Offset":Offset})
        Sources.update({Source_Name:{"Base":Base,"Url":Url,"Offset":Offset}})
        return True
    except: return False

def Save_Sources():
    # 保存源
    open("./sources.json","w",encoding="utf-8").write(json.dumps(Sources,indent=4,ensure_ascii=False))

class Sec_Math:
    # 方差, 随机数等方法
    
    def Random(All_Num:int=10,Range:list=[1200,3000])->list:
        # 随机生成All_Num个随机数, 且范围在Range中
        # Op不会多于20分钟,所以Range取20-50分钟最佳
        # 时间过久需要考虑分P问题
        return [random.randint(Range[0],Range[1]) for i in range(All_Num)]

    def Standerd_Diviation(Data:list)->float:
        Data = list(Data)
        print(Data)
        # 计算标准差
        if len(set([i[1]["bv"] for i in Data])) != 1: return {"signal":False,"Error":"Bv Not Same"}
        # 如果同一录播出现主键Bv不同的情况,大概率G了

        # 对于一个源Bv不同,可能出现两种情况
        # 1. 相似场景(很少出现)
        # 2. 主键未收录(对于某些抖音视频/各种原因没收录的情况) 会导致搜索到相似的录播中
        # 主键未收录还可能返回空值
        # 标准差就是为了尽量减少这种问题出现的

        Offset,tmp = [] , []
        for i in Data:
            Alter_Time = i[0] # 这个是其他源的时间,是随机生成的
            Offset.append(Alter_Time - i[1]["time"]) # 其他源减去主键源
        if len(Offset) ==0 : return {"signal":False,"Error":"Offset Empty"}
        Minimal_Offset = min([abs(i) for i in Offset])
        Offset = round(sum(Offset)/len(Offset),2) #平均偏移量

        for i in Data: tmp.append(math.pow(i[0]-i[1]["time"]-Offset,2)) # 平方差
        Standerd_Diviation =  round(math.sqrt(sum(tmp)/len(tmp)),2) # 标准差
        if Standerd_Diviation >10 : return {"signal":True,"Offset":Minimal_Offset,"Standerd_Diviation":Standerd_Diviation,"BV":Data[0][1]["bv"]} # 如果标准差大于10,返回最小偏移量
        return {"signal":True,"Offset":Offset,"Standerd_Diviation":Standerd_Diviation,"BV":Data[0][1]["bv"]}