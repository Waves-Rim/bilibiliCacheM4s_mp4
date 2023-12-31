# b站缓存m4s转mp4



## 1. 为什么需要做这件事

之前心血来潮，从b站缓存了不少视频到本地。

但是都是m4s格式，而且没有名称、分组。只能依赖其客户端软件播放。同时其客户端又让人很不舒服，卡顿、广告、洗脑式推广...

所以打算将其转为通用mp4格式，摆脱软件依赖，并给文件进行命名、分组。

又因为数据量很庞大，故借助python脚本进行这项工作。



## 2. 已知相关信息

a. 缓存目录下，每个视频缓存都在一个单独的文件夹下，此文件夹用纯数字命名；

b. 单独视频文件夹下，".videoInfo"中是一个记录了视频名称、作者、分组等信息的字典，其键值分别为”title“，"uname"，"groupTitle"。但是有些视频，此文件为空；

c. 文件夹下，两个**.m4s文件分别是合成mp4文件所需要的音频和视频数据。但是需要去除其开头的9个二进制0后，才能正常使用；

d. 修改后的**.m4s文件可以使用以下命令来转化为MP4文件

```bash
> ffmpeg -i input1.m4s -i input2.m4s -c copy out.mp4
```

e. python中，可以使用ex = subprocess.Popen(cmd)来执行上述命令，并用ex.wait()来等待上述命令执行完成。



## 3. 思路、流程、代码

```python
# 1. 为每个视频构建信息字典
empty = {
    "dir_id"    : '',
    "title"     : '',
    "uname"     : '',
    "groupTitle": '',
    "m4sPath"  : []
 	}

# 2. 遍历缓存目录，获取相关信息
cache_dir = "E:\\bilibili_cache"

cacheInfo = []
for name in os.path.listdir(cache_dir):
    namePath = os.path.join(cache_dir, name)
    if os.path.isdir(namePath):
        empty = {}
        empty["dir_id"] = name
        filesPath = os.listdir(namePath)
        empty["m4sPath"].append(os.path.join(namePath, '\\.videoInfo'))
        for fileName in filesPath:
            if '.m4s' in fileName:
                empty["m4sPath"].append(fileName)
        try:
            with open(empty["m4sPath"][0], encoding='utf-8') as frd:
                videoInfo = json.load(frd)
            empty["title"] = videoInfo["title"]
            empty["uname"] = videoInfo["uname"]
            empty["groupTitle"] = videoInfo["groupTitle"]
        except:
            print(namePath, '----->>> error')
            empty["title"] = name
            empty["uname"] = "others"
            empty["groupTitle"] = "others"
        cacheInfo.append(empty)
        
# 3. 统计视频作者名称，及其分组名称，创建分组目录。
groupDir = {}
for item in cacheInfo:
    groupDir[item["uname"]] = []
for item in cacheInfo:
    if item["groupTitle"] not in groupDir[item["uname"]]:
        groupDir[item["uname"]].append(item["groupTitle"])

mp4Dir = "E:\\mp4dir"
for uname in groupDir:
    for groupName in groupDir[uname]:
        groupNumber = groupDir[uname].index(groupName)
        groupPath = os.path.join(mp4Dir, uname, str(groupNumber))
        mkd_cmd = "mkdir " + groupPath
        os.system(mkd_cmd)
        with open(os.path.join(groupPath, "groupName.txt"), 'w') as ftxt:
            ftxt.write(groupName + '\n' + groupPath)

# 4. 休整m4s文件，然后合并为mp4，并存储于分组目录中。
for item in cacheInfo:
    uname = item["uname"]
    groupName = item["groupTitle"]
    groupNumber = groupDir[uname].index(groupName)
    mp4Name = ''
    illegaSymbols = "[]<>\\|/?*+ \r\n"
    for symbol in item["title"]:
        if symbol not in illegaSymbols:
            mp4Name += symbol
    mp4Name += '.mp4'
    mp4Path = os.path.join(mp4Dir, uname, str(groupNumber), mp4Name)
    
    m4sCachePath1 = os.path.join(mp4Dir, "cache1.m4s")
    with open(item["m4sPath"][1], 'rb') as frb_m4s1:
        with open(m4sCachePath1, 'wb') as fwb_m4s1:
            fwb_m4s1.write(frb_m4s1.read()[9:])
    m4sCachePath2 = os.path.join(mp4Dir, "cache2.m4s")
    with open(item["m4sPath"][2], 'rb') as frb_m4s2:
        with open(m4sCachePath1, 'wb') as fwb_m4s2:
            fwb_m4s2.write(frb_m4s2.read()[9:])
            
    ff_cmd = "ffmpeg -i " + m4sCachePath1 + " -i " + m4sCachePath2 + " -c copy " + mp4Path
    ex = subprocess.Popen(ff_cmd, close_fds=True)
    ex.wait()
    os.remove(m4sCachePath1)
    os.remove(m4sCachePath2)
```

