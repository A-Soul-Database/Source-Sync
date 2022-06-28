# 多源协同
![无标题.png](https://s2.loli.net/2022/02/03/ZHPDh96OWwTzcGs.png)

可用于
- 时间轴
- 提高鲁棒性
- 多数据源加入

## 使用方法
1. 运行`pip install -r requirements`安装必要依赖，并确保你安装了ffmpeg
2. 运行`python ./data/prepare_data.py`下载哈希库(每次有新录播都要更新)
3. 运行`python actions.py` 进行全up主校验,时间偏移为 Asdb 默认源
4. 对好的源文件可在`data/sources.json`中找到

## Todo
Version 1.2
[x] 奶粉新站的解析
[x] subprocess卡死问题
[] 日志

## 数据源Sources.json结构  

在Asdb使用的主键为  `BV1NL411T7M7` 其对应的为List,List里面对应了两个其他的录播  

```json
{

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