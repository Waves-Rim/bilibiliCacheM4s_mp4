import os
import json

cache_dir = "E:\\bilibili_cache"

cacheInfo = []
for name in os.listdir(cache_dir):
    namePath = os.path.join(cache_dir, name)
    print(namePath)
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
            print("error")
            empty["title"] = name
            empty["uname"] = "others"
            empty["groupTitle"] = "others"
        fcache.write(str(empty) + '\n')
        cacheInfo.append(empty)
