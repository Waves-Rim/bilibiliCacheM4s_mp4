import os
import json
import time
import subprocess

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
                empty["m4sPath"].append(os.path.join(namePath, fileName))
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
        with open(os.path.join(groupPath, "groupName.txt"), 'w') as ftxt:
            ftxt.write(groupName + '\n' + groupPath)

cachePath = "E:\\mp4dir\\m4sCache"
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
    
    m4sCachePath1 = os.path.join(cachePath, "cache1.m4s")
    with open(item["m4sPath"][1], 'rb') as frb_m4s1:
        with open(m4sCachePath1, 'wb') as fwb_m4s1:
            fwb_m4s1.write(frb_m4s1.read()[9:])
    m4sCachePath2 = os.path.join(cachePath, "cache2.m4s")
    with open(item["m4sPath"][2], 'rb') as frb_m4s2:
        with open(m4sCachePath2, 'wb') as fwb_m4s2:
            fwb_m4s2.write(frb_m4s2.read()[9:])
            
    ff_cmd = "ffmpeg -i " + m4sCachePath1 + " -i " + m4sCachePath2 + " -c copy " + mp4Path + " -y"
    print(ff_cmd)
    ex = subprocess.Popen(ff_cmd, close_fds=True)
    ex.wait()

    cleanCacheCmd = "del " + os.path.join(cachePath, "*.m4s")
    print(cleanCacheCmd)
    clrBatPath = os.path.join(cachePath, "clr.bat")
    with open(clrBatPath, 'w') as fbat:
        fbat.write(cleanCacheCmd)
    ex = subprocess.Popen(clrBatPath, close_fds=True)
    ex.wait()
    
    print("Done " + str(cacheInfo.index(item) + 1) + '/' + str(len(cacheInfo)))
