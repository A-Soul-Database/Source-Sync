# 多源协同
![无标题.png](https://s2.loli.net/2022/02/03/ZHPDh96OWwTzcGs.png)

可用于
- 时间轴
- 提高鲁棒性
- 多数据源加入

## 数据源Sources.json结构  
在source.json中有很多个源,下列为其中一个录播对应的三个源  
在Asdb使用的主键为  `BV1NL411T7M7` 其对应的为List,List里面对应了两个其他的录播  
其他两个录播对应了主Key的Bv值    
```json
{
    "2022.02.23 乃琳 手可摘星辰~.mp4":{
        "Base":"BV1NL411T7M7",
        "Url":"https://asoul1.asoul-rec.com/ASOUL-REC-%E4%BA%8C%E5%91%A8%E5%B9%B4/2022.02.23 乃琳 手可摘星辰~.mp4",
        "Time":-3.2
    },
    "BV1V3411j7GW":{
        "Base":"BV1NL411T7M7",
        "Url":"https://www.bilibili.com/video/BV1V3411j7GW",
        "Time":2.8
    },

    "BV1NL411T7M7":[
        {
            "Url":"https://asoul1.asoul-rec.com/ASOUL-REC-%E4%BA%8C%E5%91%A8%E5%B9%B4/2022.02.23 乃琳 手可摘星辰~.mp4",
            "Time":-3.2
        },
        {
            "Url":"https://www.bilibili.com/video/BV1V3411j7GW",
            "Time":2.8
        }
    ]
}
```