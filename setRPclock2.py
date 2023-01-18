from time import time
from datetime import datetime
from subprocess import Popen, PIPE

def run_ssh_cmd(host, cmd):
    cmds = ['ssh', '-t', host, cmd]
    return Popen(cmds, stdout=PIPE, stderr=PIPE, stdin=PIPE)    
    
# I want to construct the command (for ssh): sudo date -s '2020-03-28 15:57:00'
# to send to the rp

t = time()
dt_string = "'"+str(datetime.fromtimestamp(t))+"'"

def setRPclockTime(x):
    if x == '__main__':
        host = 'pi@HTD-raspberrypi'
        cmd = "sudo date -s "+dt_string
        print(cmd)
        results = run_ssh_cmd(host, cmd).stdout.read()
        print(results)



if __name__ == '__main__':
#    host = 'pi@HTD-raspberrypi'
#cmd = 'raspistill -o Desktop/image112jpg'
#    cmd = "sudo date -s "+dt_string
#    print(cmd)
#    results = run_ssh_cmd(host, cmd).stdout.read()
#    print(results)
     x = '__main__'
     setRPclockTime(x)  
     

