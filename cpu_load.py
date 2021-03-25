class Cpu:
    uptime = ""
    scnuptime = ""
    scnuser = ""
    vol = ""
    volfree = ""
    ps = ""
    scnps = ""

    def __init__(self, uptime, scnuptime, scnuser, vol, volfree, ps, scnps):
        Cpu.uptime = uptime
        Cpu.scnuptime = scnuptime
        Cpu.scnuser = scnuser
        Cpu.vol = vol
        Cpu.volfree = volfree
        Cpu.ps = ps
        Cpu.scnps = scnps

    def to_dict(self):
        data = {}
        data['uptime'] = self.uptime
        data['scnuptime'] = self.scnuptime
        data['scnuser'] = self.scnuser
        data['vol'] = self.vol
        data['volfree'] = self.volfree
        data['ps'] = self.ps
        data['scnps'] = self.scnps
        return data


def main():
    import os
    import json
    import re

    cpuInfo = os.popen("uptime").read()
    Scn = os.popen(
        "ssh -i /volume2/web/api/id_rsa root@scn 'uptime; arp -a'").read()
    Scn = re.sub(' +', ' ', Scn)
    Scn = Scn.split("\n")
    scnInfo = Scn[0]
    Scn.pop(0)
    Scn.pop(0)
    Scn.pop(len(Scn)-1)
    # cpuInfo = os.popen("echo '18:36:37 up 1 day,  1:14,  1 user,  load average: 0.00, 0.00, 0.00'").read().split(", ")

    volumeInfo = os.popen("df -m | grep volume2").read()
    # volumeInfo = "/dev/vg1001/lv  7.3T  326G  6.9T   5% /volume2"
    volumeInfo = re.sub(' +', ' ', volumeInfo)
    volumeInfo = volumeInfo.split(" ")
    volumeInfo[1] = str(round(float(volumeInfo[1])/1024/1024, 2)) + ' TB'
    volumeInfo[2] = str(round(float(volumeInfo[2])/1024, 2)) + ' GB' if float(volumeInfo[2]) < 1000000 else str(round(float(volumeInfo[2])/1024/1024, 2)) + ' TB'

    ps = os.popen("ps -eo user,pid,%cpu,command --sort=-pcpu | head -n 11").read()
    ps = re.sub(' +', ' ', ps)
    ps = ps.split("\n")
    ps.pop(0)
    ps = ps[0:10]

    scnPs = os.popen("ssh -i /volume2/web/api/id_rsa root@scn top -b -n 1 | head -n 14  | tail -n 10 | awk '{print $3,$1,$8,$9}'").read()
    scnPs = re.sub(' +', ' ', scnPs)
    scnPs = scnPs.split("\n")
    scnPs = scnPs[0:5]

    out = Cpu(cpuInfo, scnInfo, Scn,
              "Used " + volumeInfo[2] + " of " + volumeInfo[1] + " (" + volumeInfo[4] + ")", volumeInfo[4],
             ps, scnPs).to_dict()
    y = json.dumps(out)
    print(y)


if __name__ == "__main__":
    main()
