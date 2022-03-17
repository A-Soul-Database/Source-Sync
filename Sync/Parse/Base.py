class BaseModel:
    def __init__(self,Acquire_Url):
        self.Acquire_Url = Acquire_Url

    def Parse_Url(self):
        # 获取可供ffmpeg使用的地址
        ...

    def __Sourcer__(self):
        # 视频源 若需要添加源,则建议把名称写的好看一些些,便于大家认
        return self.__class__.__name__

    def Lister(self):
        # 录播大多数都是以列表形式呈现的,这里可以返回列表的URL值和名称,便于Loop
        # @Return [{"Name":str,"Url":str},...]
        # Name 十分重要,它将作为主键在Sources中呈现,所以如果是BiliBili,建议使用Bv
        # Url 可以不是播放链接,只要是URI即可(因为部分可能存在Token或者Expire限制),在解析具体某个元素时会获得播放链接
        ...