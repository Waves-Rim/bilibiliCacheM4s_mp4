import os
import json

cache_dir = "E:\\bilibili_cache"

cacheInfo = []
for name in os.listdir(cache_dir):
    namePath = os.path.join(cache_dir, name)
    if os.path.isdir(namePath):
        empty = {}
        empty["dir_id"] = name
        empty["m4sPath"] = []
        empty["m4sPath"].append(os.path.join(namePath, '.videoInfo'))
        
        filesPath = os.listdir(namePath)
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
            empty["title"] = name
            empty["uname"] = "others"
            empty["groupTitle"] = "others"
        cacheInfo.append(empty)

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
        if not os.path.isdir(groupPath):
            os.system(mkd_cmd)
        else:
            print(groupPath,"已存在")
        with open(os.path.join(groupPath, "groupName.txt"), 'w') as ftxt:
            ftxt.write(groupName + '\n' + groupPath)
