import json
import random
import os
import statistics
import Sync

Sources = json.loads(open("./data/sources.json","r",encoding="utf-8").read()) if os.path.exists("./data/sources.json") else {}
forbidden_urls = json.loads(open("./data/forbidden_urls.json","r",encoding="utf-8").read()) if os.path.exists("./data/forbidden_urls.json") else {}
not os.path.exists("./Sync/Detect/Alphas") and print("\n Warning: Detect Alphas Not Found! \n")

def Search(keywords:str):
    # 根据 文件名搜索
    for _base,_detail in Sources.items():
        if keywords == _base: return _base
        for _item in _detail:
            if keywords == _item["Name"] or keywords == _item["Url"] : return _base

def Is_forbidden(Url:str):
    # 检测是否被禁止
    for i in forbidden_urls:
        if i in Url: return True

def Add_Item(Base:str,Source_Name:str,Url:str,Sourcer:str,Offset:float)->bool:
    # 添加项目
    # Base(主键源): Asdb 中的Bv值; URI: 其他源的路径 ; Sourcer: 来源名称; Time: 时间戳(其他源 - 主键源)
    global Sources
    try:
        if not Sources.get(Base):
            Sources[Base] = []
        Sources[Base].append({"Sourcer":Sourcer,"Url":Url,"Offset":Offset,"Name":Source_Name})
        #Sources.update({Source_Name:{"Base":Base,"Url":Url,"Offset":Offset}})
        return True
    except: return False

def Save_Sources():
    # 保存源
    open("./data/sources.json","w",encoding="utf-8").write(json.dumps(Sources,indent=4,ensure_ascii=False))

def Install_Core():
    # 安装识别库
    ...

class RCD:
    # RCD: Randomly Consistent Detection 随机持续性检测
    # 随机持续性检测可用于对源和时间同步
    # 随机选取片段比较,片段间隔为1s
    
    def Random_Clips(self,Random_Range:list=[1200,2400],Consistenet_Duration:int=60)->list:
        # 随机返回一个时间段 时间段的秒数在Random_Range中,片段持续Consistenet_Duration 秒
        time_scale = random.randint(Random_Range[0],Random_Range[-1])
        return [time_scale,time_scale+Consistenet_Duration]

    

    def Caculate(self,Detected_Data:list,Consist_Range:list)->list:
        # 计算Offset并返回
        bvs = set( [fn["bv"] for fn in Detected_Data if fn["signal"]] )
        if len(bvs) >1 or len(bvs) == 0: return {"signal":False} #如果Bv不同或为空,则认为该片段无效
        bv = list(bvs)[0] # 取第一个Bv为检测bv

        Consist_Range_mean= statistics.mean(Consist_Range) # 时间段平均值
        Offset = [Consist_Range_mean-fn["time"] for fn in Detected_Data if fn["signal"]]
        Normal = self.Caculate_Normal(Offset)
        return {"signal":not (type(Normal)==bool),"Offset":Normal,"bv":bv}

    def Is_Constitent(self,Datas,Legnth_Of_Clip,Confidence:float=0.6)->bool:
        # 检测是否连续 置信度为Confidence        
        Detected_Times = [] # 检测出的时间(按照大小排序)
        for fn in Datas:
            if fn["signal"]:Detected_Times.append(fn["time"])
        valuable_length = len(Detected_Times)
        if len(Detected_Times) < 3: return False,[] #避免卡死
        if valuable_length < Legnth_Of_Clip*Confidence : return False , [] # 如果数据不足,则认为不连续
        a=sorted(Detected_Times)
        max_l=[]
        i=0
        while i<len(a)-1:
            l=list([a[i]])
            for j in range(i+1,len(a)):
                if a[j]-l[-1]<=3:
                    i+=1
                    l.append(a[j])
                else:
                    i = j
                    break
            if len(l)>len(max_l): max_l=l.copy()
            l.clear()
        #print(valuable_length,len(max_l),max_l)
        if valuable_length*Confidence > len(max_l): return False,max_l
        else: return True , max_l

    def Caculate_Normal(self,Datas:list):
        # 计算正态分布置信度为50%时的值
        if len(Datas)<2: return False
        Offset_mean = statistics.mean(Datas)
        Offset_std = statistics.stdev(Datas)
        if Offset_std <0 or Offset_std == 0: return False
        Offset_Normal = statistics.NormalDist(Offset_mean,Offset_std)
        return Offset_Normal.inv_cdf(0.5)

def Do_Sync(CONFIG:dict,D_Url:str,Args:str):
    # 执行同步
    # 首先检测是否同步,若同步:则返回Offset和Bv号
    # 为了防止未收录导致死循环,设置最大检测次数 CONFIG["Max_Detect_Times"]
    # 若检测次数超过,则返回False, CONFIG 来源为actions.py
    RCD_Obj = RCD()
    Roll_Nums = 0
    while Roll_Nums < CONFIG["Max_Rool_Num"]:
        Random_Time_Scale = RCD_Obj.Random_Clips(Random_Range=CONFIG["Random_Range"],Consistenet_Duration=CONFIG["Consistenet_Duration"])
           #随机一个时间段
        This_Result = Sync.Detect.hash.Do_Detect(url=D_Url,
            Args = Args ,Time_Scales = Random_Time_Scale)
        if type(This_Result)==dict: continue # 检测失败
        Is_Consistent = RCD_Obj.Is_Constitent(Datas=This_Result,Legnth_Of_Clip=CONFIG["Consistenet_Duration"])
        if Is_Consistent[0]:
            return RCD_Obj.Caculate(Detected_Data=This_Result,Consist_Range=Random_Time_Scale)
        else:
            Roll_Nums+=1
            continue

    return {"signal":False}