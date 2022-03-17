import Sync
import json
# Do WorkFlow :)

for i in Sync.Parse.Lister: 
    # 每个视频源都需要实现这样的方法,便于调用
    tmp = i() # 创建源实例
    print(f"Start Sync For {tmp.__Sourcer__()}")
    