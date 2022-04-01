import Sync
import time


CONFIG = {
    "Max_Rool_Num":10,
    "Random_Range":[800,2400], #随机视频分段时间范围
    "Consistenet_Duration":20, #每个分段持续时间(单位:秒)
}

for Sourcer in Sync.Parse.Lister:
    Sourcer_Instance = Sourcer()

    print("Start Sync For Sourcer: {}.".format(Sourcer_Instance.__Sourcer__()))

    Lists = Sourcer_Instance.Lister()
    for _item in Lists:
        Start_time = time.time()
        print(_item)
        Sourcer_Instance.Change_Url(_item["Url"]) , Sourcer_Instance.Parse_Url() # 改变Url并解析
        Detect_Result = []

        print(Sync.main.Do_Sync(CONFIG=CONFIG,D_Url=Sourcer_Instance.Download_Url,Args=Sourcer_Instance.Download_Url_Args))

        print("Time Cost:",time.time()-Start_time)

