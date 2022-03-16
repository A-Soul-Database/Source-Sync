import Detect
import Parse
import json

sources = json.loads(open("./sources.json","r").read()) or {}

def Search(Name:str):
    # 根据 文件名搜索
    return sources.get(Name)