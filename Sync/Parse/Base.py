class BaseModel:
    def __init__(self,Acquire_Url):
        self.Acquire_Url = Acquire_Url

    def Lister(self):
        # 根据请求网站获取视频列表
        ...

    def Parse_Url(self):
        # 获取可供ffmpeg使用的地址
        ...
