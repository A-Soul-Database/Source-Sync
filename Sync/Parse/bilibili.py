from . import Base

class BiliBili(Base.BaseModel):

    def __init__(self, url):
        super().__init__(url)

    def Parse(self):
        ...