import json
import random
import os
import statistics

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
        #Sources.update({Source_Name:{"Base":Base,"Url":Url,"Offset":Offset}})
        return True
    except: return False

def Save_Sources():
    # 保存源
    open("./sources.json","w",encoding="utf-8").write(json.dumps(Sources,indent=4,ensure_ascii=False))


class RCD:
    # RCD: Randomly Consistent Detection 随机持续性检测
    # 随机持续性检测可用于对源和时间同步
    # 随机选取片段比较,片段间隔为1s
    
    def Random_Clips(self,Clip_Num:int=3,Random_Range:list=[1200,2400],Consistenet_Duration:int=60)->list:
        # 随机返回Clip_Num个时间段 每个时间段的秒数在Random_Range中,每个片段持续Consistenet_Duration 秒
        Return_Clips = []
        for i in range(Clip_Num):
            time_scale = random.randint(Random_Range[0],Random_Range[-1])
            Return_Clips.append([time_scale,time_scale+Consistenet_Duration])
        return Return_Clips
    

    def Caculate(self,Detected_Data:list,Random_Origin_List:list)->list:
        # 计算平均 Offset 并返回
        Offset = []
        bvs = set([fn["bv"] for fn in Detected_Data if fn["signal"]])
        print(bvs)
        if len(bvs) >1 : return {"signal":False} #如果Bv不同,则认为该片段无效
        bv = list(bvs)[0] # 取第一个Bv为检测bv
        Detect_Times = set([fn["time"] for fn in Detected_Data if fn["signal"]]) #检测出的时间(按照大小排序)
        Have_Times = [fn for fn in range(Random_Origin_List[0],Random_Origin_List[-1])] # 把给定的范围转换为每一秒的时间点
        for _item in list(zip(Detect_Times,Have_Times)): Offset.append(_item[1]-_item[0]) # 计算每一秒对应的时间差
        # 计算对应的正态分布的最大数目
        if len(Offset)> 5: Offset.remove(max(Offset)) , Offset.remove(min(Offset)) # 去除最大值和最小值
        return {"signal":True,"Offset":self.Caculate_Normal(Offset),"bv":bv}

    def Generate_Single_Result(self,Data:list):
        # 通过检测结果进行正态性检验
        Offsets = [fn["Offset"] for fn in Data if fn["signal"]]
        if len(Offsets) > 5: Offsets.remove(max(Offsets)) , Offsets.remove(min(Offsets)) # 去除最大值和最小值
        return {"bv":"bv","Offset":self.Caculate_Normal(Offsets)}

    def Caculate_Normal(self,Datas:list):
        # 计算正态分布中间最大值
        Offset_mean = statistics.mean(Datas)
        Offset_std = statistics.stdev(Datas)
        Offset_Normal = statistics.NormalDist(Offset_mean,Offset_std)
        return Offset_Normal.inv_cdf(0.5)