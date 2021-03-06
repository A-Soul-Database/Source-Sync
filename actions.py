# -*- coding: utf-8 -*-
import Sync
import time
import logging
logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename="./actions.log",filemode="w",encoding="utf-8")
logging_console = logging.StreamHandler()
logging_console.setLevel(logging.INFO)
logging.getLogger().addHandler(logging_console)
CONFIG = {
    "Max_Rool_Num":10,
    "Consistenet_Duration":20, #每个分段持续时间(单位:秒)
}
Lister = [Sync.Parse.bilibili.Official,Sync.Parse.knaifen.knaifen
    ,Sync.Parse.bilibili.Record_type1,Sync.Parse.bilibili.Record_type2]



for Sourcer in Lister:
    Sourcer_Instance = Sourcer()
    #print("Start Sync For Sourcer: {}.".format(Sourcer_Instance.__Sourcer__()))
    logging.info("Start Sync For Sourcer: {}.".format(Sourcer_Instance.__Sourcer__()))
    Lists = Sourcer_Instance.Lister()
    CONFIG["Random_Range"] = Sourcer_Instance.__get_Random_Range__()
    progress = 1
    for _item in Lists:
        progress+=1
        Start_time = time.time()
        logging.info(f"{progress}/{len(Lists)}")
        if Sync.main.Search_With_Sourcer(_item["Url"],_item["Sourcer"]) is not None: 
            logging.debug(f"Item {_item['Name']} Exist, Skip.")
            continue # 如果检测到,则跳过
        if Sync.main.Is_forbidden(Url=_item["Name"],Sourcer=Sourcer_Instance.__Sourcer__()): 
            logging.debug(f"Item {_item['Name']} In Forbidden Urls, Skip.")
            continue # 如果为无需检测的,则跳过
        #print(f" {_item}   {progress}/{len(Lists)}")
        logging.debug(f"{Sourcer_Instance.__Sourcer__()} : {_item['Name']}")
        Sourcer_Instance.Change_Url(_item["Url"]) , Sourcer_Instance.Parse_Url() # 改变Url并解析
        info = Sync.main.Do_Sync(CONFIG=CONFIG,D_Url=Sourcer_Instance.Download_Url,Args=Sourcer_Instance.Download_Url_Args)
        if info["signal"]:
            Sync.main.Add_Item(Base=info["bv"],Url=_item["Url"],Source_Name=_item["Name"],Sourcer=_item["Sourcer"],Offset=info["Offset"])
            Sync.main.Save_Sources()
        else:
            logging.error("Sync Failed For {}.".format(_item["Name"]))
        logging.debug(f"Time Cost:{time.time()-Start_time}")
