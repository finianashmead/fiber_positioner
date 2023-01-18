# import the necessary packages
import sys
import os
# Processes to send commands
from subprocess import Popen, PIPE
# Processes to tell time
from time import time
from datetime import datetime

def run_ssh_cmd(host, cmd):
    cmds = ['ssh', '-t', host, cmd]
    return Popen(cmds, stdout=PIPE, stderr=PIPE, stdin=PIPE)    

def formatdateforfname(results):
    results=str(results).replace(" ","-")
    results=str(results).replace("'","")
    results=str(results).replace(":","H",1)
    results=str(results).replace(":","M")
    lastchar=len(results)
    FnameEnd=results[:lastchar-5]+'S' # This should give us 1/10 second accuracy, e.g. 2022-04-27-16H19M47.4S
    return FnameEnd
    

# Format the top of the image file name

# Construct image name bottom
# I want to construct the ImageFileName to include a prefix from standard input
# and a suffix with the date and time
# I might use the prefix as the image name on the RP

def takePhotoAndCopy(x,topfname):
    if x == '__main__':
        t = time()
        dt_string = "'"+str(datetime.fromtimestamp(t))+"'"
        FnameEnd=formatdateforfname(dt_string)
        print(FnameEnd)

# Now ask the camera to take a picture
        host = 'pi@HTD-raspberrypi'
        cmd = 'raspistill -o '+ topfname + '.jpg'
        print(cmd)
        results = run_ssh_cmd(host, cmd).stdout.read()
        print(results)

# Now bring the image back
        string = 'scp pi@HTD-raspberrypi:~/'+topfname+'.jpg'+' .'
        print(string)
        cmd = string
        os.system(cmd)
#print(cmd)
#results = run_ssh_cmd(host, cmd).stdout.read()
#print(results)
 
if  __name__ == '__main__':
    x = '__main__'
    print(len(sys.argv))
    if len(sys.argv)==1:
        topfname = "image"
    else:
         topfname = str(sys.argv[1])
#        topfname = "image2"
    print(topfname)

    takePhotoAndCopy(x,topfname)

#print(cmd)
#results = run_ssh_cmd(host, cmd).stdout.read()
#print(results)
 
