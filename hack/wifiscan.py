# coding=utf8
from subprocess import *
import subprocess
import threading
import os
# call(["ls", "-l"],shell= True)
# out = call(["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/A/Resources/airport", "scan"])
#value = os.popen(scanShell).read()
# scanShell = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/A/Resources/airport scan"

# print value


# def connectWifi(shell):
#     print shell
#     out = os.popen(shell).read()
#     print out
#     if out == 0:
#         resultFile = open('result.text', "w")
#         resultFile.write(shell)
#         resultFile.close()
#         os._exit()
file = open('/Users/junxiaozhang/www/python_workspace/python_hack/resource/key.txt', 'r+')
lines = file.readlines()
shells = []
for line in lines:
    # print line.strip()
    # out = call(["networksetup","-setairportnetwork","en0","TP-LINK_401",line.strip()])
    value = os.popen("networksetup setairportnetwork en0 FAST_0ED8 "+line.strip()).read()
    # shells.append("networksetup setairportnetwork en0 FAST_0ED8 "+line.strip())
    print value
    if value  == 0:
        print line.strip()
        break
# threads = []
# start = 0
# step = 10
# if len(shells) > (start+step):
#     # tempary = shells[start:(start+step)]
#     tempary = shells
#     for tempShell in tempary:
#         threads.append(threading.Thread(target=connectWifi, args=(tempShell,)))
#
#     for tmpThread in threads:
#         tmpThread.start()
#         tmpThread.join()

# out = call(["networksetup","-setairportnetwork","en0","喊爸爸就让你连","291722629"])
# out = Popen("networksetup -setairportnetwork en0 Xiaomi_80A5_5G 18652603012", shell=True, stdout= subprocess.PIPE)
# out = Popen("networksetup -setairportnetwork en0 喊爸爸就让你连 18652603012", shell=True, stdout= subprocess.PIPE)
# while out.poll()==None:
#     print "1111"
#     print out.stdout.readline()
# print out.returncode


