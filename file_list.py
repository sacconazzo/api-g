class fileG:
    subdir = ""
    name = ""
    size = 0

    def __init__(self, subdir, name, sizeI):
        fileG.subdir = subdir
        fileG.name = name
        size = float(sizeI)
        fileG.size = size/1024
        if (size > 1000000000):
            fileG.sz = str(round(size/1024/1024/1024, 2)) + ' GB'
        elif (size > 1000000):
            fileG.sz = str(round(size/1024/1024, 2)) + ' MB'
        elif (size > 1000):
            fileG.sz = str(round(size/1024, 2)) + ' kB'
        else:
            fileG.sz = str(size) + ' B'

    def to_dict(self):
        data = {}
        data['name'] = self.name
        data['subdir'] = self.subdir
        data['size'] = self.size
        data['sz'] = self.sz
        return data


def main():
    import os
    import json
    import re

    dr = "/volumeUSB1/usbshare"
    # dr = "/Users/giona/downloads" #for testing
    init = "."
    fl = []
    fls = {}
    fls['n'] = 0
    fls['size'] = 0
    fls['volume'] = "less then 0"
    for root, dirs, files in os.walk(dr):
        dirs[:] = [d for d in dirs if not d[0] == init and not d[0] == '@'] 
        for file in files:
            if not file.startswith(init):
                size = os.path.getsize(root + '/' + file)
                fls['size'] += size
                fl.append(fileG(root, file, size).to_dict())
    fls['n'] = len(fl)
    fls['storing'] = False
    exe = os.system('ps | grep mv > /dev/null')
    if exe == 0:
        fls['storing'] = True
    volumeInfo = os.popen("df --human-readable | grep USB").read()
    if volumeInfo:
        volumeInfo = re.sub(' +', ' ', volumeInfo)
        volumeInfo = volumeInfo.split(" ")
        fls['volume'] = volumeInfo[1]
    fls['sz'] = fileG(dr, '', fls['size']).to_dict()['sz']
    fls['files'] = fl
    y = json.dumps(fls)
    # sorted(y)
    print(y)


if __name__ == "__main__":
    main()
