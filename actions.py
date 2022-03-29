import Sync
import time

RCD = Sync.main.RCD() # 创建一个随机连续性检测对象

CONFIG = {
    "Clip_Num":40, #单个视频分段次数,每段都会检测
    "Random_Range":[1000,2400], #随机视频分段时间范围
    "Consistenet_Duration":10, #每个分段持续时间(单位:秒)
}

for Sourcer in Sync.Parse.Lister:
    Sourcer_Instance = Sourcer()
    print("Start Sync For Sourcer: {}.".format(Sourcer_Instance.__Sourcer__()))
    Lists = Sourcer_Instance.Lister()
    for _item in Lists:
        print(_item)
        Sourcer_Instance.Change_Url(_item["Url"]) , Sourcer_Instance.Parse_Url() # 改变Url并解析
        Detect_Result = []

        for Single_Split_Clip_Range in RCD.Random_Clips(
            Clip_Num=CONFIG["Clip_Num"],
            Random_Range=CONFIG["Random_Range"],
            Consistenet_Duration=CONFIG["Consistenet_Duration"]
        ):
            result = Sync.Detect.hash.Do_Detect(
                url = Sourcer_Instance.Download_Url,
                Args = Sourcer_Instance.Download_Url_Args,
                Time_Scales = Single_Split_Clip_Range
            )
            a = RCD.Caculate(result,Single_Split_Clip_Range)
            Detect_Result.append(a)
            print(a)
            time.sleep(0.5)
        RCD.Generate_Single_Result(Detect_Result)
        break