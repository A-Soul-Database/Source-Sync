import Sync
import time
# Do WorkFlow :)
Start_Time = time.time()
print(f'Start Time At : {time.strftime("%Y-%m-%d %X",time.localtime())}')

for _i in Sync.Parse.Lister: 
    # 每个视频源都需要实现这样的方法,便于调用
    tmp = _i() # 创建源实例
    print(f"Start Sync For {tmp.__Sourcer__()}")
    Roll_List = tmp.Lister() # 获取数据源信息
    #Roll_List = Roll_List[0:2]
    for i in Roll_List:
        if Sync.main.Search(i["Name"]) is not None: continue #若已经校准,则跳过
        else:

            tmp.Change_Url(i["Url"]) # 改变源的Url
            tmp.Parse_Url()

            if tmp.Download_Url != "":
                Time_Range = Sync.main.Sec_Math.Random() # 随机生成多个时间戳
                Result = []

                for time_item in Time_Range:
                    try:
                        Detect = Sync.Detect.hash.Do_Detect(tmp.Download_Url,tmp.Download_Url_Args,time_item)
                    except:
                        # 可能网络异常
                        continue
                    Result.append(Detect)
                    # 将结果写入list中

                result = Sync.main.Sec_Math.Standerd_Diviation(zip(Time_Range,Result))
                print(result)
                #将Time_Range和Result组合
                # [(1235, {'bv': 'bv123','time':1237}), ...

                if result["signal"]:Sync.main.Add_Item(result["BV"],i["Name"],tmp.Acquire_Url,tmp.__Sourcer__(),result["Offset"]) 
                # 将结果写入数据表中
                time.sleep(1)
        Sync.main.Save_Sources() # 保存数据

print(f'End Time At : {time.strftime("%Y-%m-%d %X",time.localtime())} \n Total Time : {time.time()-Start_Time} Seconds')