import Sync
import time

CONFIG = {
    "Max_Rool_Num":10,
    "Consistenet_Duration":20, #每个分段持续时间(单位:秒)
}



for Sourcer in Sync.Parse.Lister:
    Sourcer_Instance = Sourcer()
    print("Start Sync For Sourcer: {}.".format(Sourcer_Instance.__Sourcer__()))
    Lists = Sourcer_Instance.Lister()
    CONFIG["Random_Range"] = Sourcer_Instance.__get_Random_Range__()

    for _item in Lists:
        Start_time = time.time()
        print(_item)
        if Sync.main.Search_With_Sourcer(_item["Url"],_item["Sourcer"]) is not None: continue # 如果检测到,则跳过
        if Sync.main.Is_forbidden(_item["Url"]): continue # 如果为无需检测的,则跳过
        
        break
        Sourcer_Instance.Change_Url(_item["Url"]) , Sourcer_Instance.Parse_Url() # 改变Url并解析
        info = Sync.main.Do_Sync(CONFIG=CONFIG,D_Url=Sourcer_Instance.Download_Url,Args=Sourcer_Instance.Download_Url_Args)
        if info["signal"]:
            Sync.main.Add_Item(Base=info["bv"],Url=_item["Url"],Source_Name=_item["Name"],Sourcer=_item["Sourcer"],Offset=info["Offset"])
            Sync.main.Save_Sources()
        else:
            print("Sync Failed For {}.".format(_item["Name"]))
        print("Time Cost:",time.time()-Start_time)

