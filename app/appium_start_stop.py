import subprocess
import sys,os

def appium_start(host, port):
    #bootstrap_port = str(port + 1)
    cmd = 'start /b appium -a '+host+' -p '+str(port)
    print(cmd)
    subprocess.Popen(cmd, shell=True, stdout=open('../'+str(port)+'.txt','a'),stderr=subprocess.STDOUT)

def appium_stop(port):
    mac_cmd = f"lsof -i tcp:{port}"
    win_cmd = f"netstat -ano | findstr {port}"
    # 判断操作系统
    os_platform = sys.platform
    print('操作系统：',os_platform)
    # #windows 系统
    if os_platform == "win32":
        win_p = subprocess.Popen(win_cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        for line in win_p.stdout.readlines():
            if line:
                line = line.decode('utf8')
                if "LISTENING" in line:
                    win_pid = line.split("LISTENING")[1].strip()
                    os.system(f"taskkill -f -pid {win_pid}")
    else:
        # unix系统
        p = subprocess.Popen(mac_cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        for line in p.stdout.readlines():
            line = line.decode('utf8')
            if "node" in line:
                stdoutline = line.split(" ")
                # print(stdoutline)
                pid = stdoutline[4]
                os.system(f"kill {pid}")

if __name__ == '__main__':
    appium_start('127.0.0.1', 4725)
    #appium_stop(4725)