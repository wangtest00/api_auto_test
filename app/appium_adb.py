import subprocess
import sys,os

def appium_start(host, port):
    cmd = 'appium -a '+host+' -p '+str(port)
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
#卸载app,用包名就行了
def uninstall_app(udid,apppackage):
    os.system('adb -s '+udid+' uninstall '+apppackage)

#唤醒屏幕，区分udid
def huanxing_screen(udid):
    os.system('adb -s '+udid+' shell input keyevent KEYCODE_POWER')
#wifi调试连接adb
def adb_connect(udid):
    os.system('adb connect '+udid+'')
    return udid

def adb_disconnect(udid):
    os.system('adb disconnect '+udid+'')

if __name__ == '__main__':
    #appium_start('127.0.0.1', 4725)
    #appium_stop(4725)
    applist = ['OPPO', '11', '192.168.20.107:5555', 'com.turrant', 'com.turrant.ui.activity.LaunchActivity']
    uninstall_app(applist[2],applist[3])
    #huanxing_screen('192.168.20.106:5555')