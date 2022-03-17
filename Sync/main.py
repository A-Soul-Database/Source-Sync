from . import Detect
from . import Parse
import json

Sources = json.loads(open("./sources.json","r",encoding="utf-8").read()) or {}

def Search(Name:str):
    # 根据 文件名搜索
    return Sources.get(Name)


def Add_Item(Base:str,Source_Name:str,Url:str,Sourcer:str,Time:float)->bool:
    # 添加项目
    # Base(主键源): Asdb 中的Bv值; URI: 其他源的路径 ; Sourcer: 来源名称; Time: 时间戳(其他源 - 主键源)
    global Sources
    try:
        if not Sources.get(Base):
            Sources[Base] = []
        Sources[Base].append({"Sourcer":Sourcer,"Url":Url,"Time":Time})
        Sources.update({Source_Name:{"Base":Base,"Url":Url,"Time":Time}})
        return True
    except: return False

