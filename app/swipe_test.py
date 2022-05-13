'''Appium 滑动API：Swipe（int start x,int start y,int end x,int y,duration)
int start x－开始滑动的x坐标，
int start y －开始滑动的y坐标。
int end x －结束点x坐标，
int end y －结束点y坐标。
duration 滑动时间（默认5毫秒）；'''
# -*- coding: utf-8 -*-
from time import sleep
import os
import time
#获取屏幕机器大小x,y
def getSize(driver):
    x=driver.get_window_size()['width']
    y=driver.get_window_size()['height']
    return (x,y)

#屏幕向上滑动
def swipeup(driver,t):
    print("正在向上滑动..")
    screensize=getSize(driver)
    x1=int(screensize[0]*0.5)#x坐标
    y1=int(screensize[1]*0.75)#起始y坐标
    y2=int(screensize[1]*0.25)#终点y坐标
    driver.swipe(x1,y1,x1,y2,t)

#屏幕向下滑动
def swipedown(driver,t):
    print("正在向下滑动...")
    screensize=getSize(driver)
    x1=int(screensize[0]*0.5)#x坐标
    y1=int(screensize[1]*0.25)#起始y坐标
    y2=int(screensize[1]*0.75)#终点y坐标
    driver.swipe(x1,y1,x1,y2,t)

#屏幕向左滑动
def swipeleft(driver,n,t):
    print("正在向左滑动...")
    screensize=getSize(driver)
    x1=int(screensize[0]*0.9)
    y1=int(screensize[1]*0.5)
    x2=int(screensize[0]*0.1)
    for i in range(0,n):#for循环，控制滑动次数
        time.sleep(3)
        driver.swipe(x1,y1,x2,y1,t)
        print("成功向左滑动：",n,"次")

#屏幕向右滑动
def swiperight(driver,n,t):
    print("正在向右滑动...")
    screensize=getSize(driver)
    x1=int(screensize[0]*0.1)
    y1=int(screensize[1]*0.5)
    x2=int(screensize[0]*0.9)
    for i in range(0,n):
        time.sleep(3)
        driver.swipe(x1,y1,x2,y1,t)
        print("成功向右滑动：",n,"次")

# 读取参数,指定设备，adb滑动屏幕
def sildes(udid,x,y,x1,y1,h):
    # 用adb模拟手指滑动屏幕
    os.system('adb -s '+udid+' shell input swipe {} {} {} {} {}'.format(x,y,x1,y1,h))
    print("运行",udid,"%s y轴|%s x轴|%s y1轴|%s x1轴"%(x,y,x1,y1))