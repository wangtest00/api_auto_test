import random,string,time

def certlist():
    st=''
    for j in range(5):  #生成5个随机英文大写字母
        st+=random.choice(string.ascii_uppercase)
    num = str(random.randint(1000, 9999))
    certNo=num+"6666"+num
    panNo=st+num+"W"
    certlist=[]
    certlist.append(certNo)
    certlist.append(panNo)
    #print(certlist)
    return certlist

 #退出登录
def logout(driver):
    driver.find_element_by_id('com.turrant:id/radio_mine').click()
    time.sleep(3)
    driver.find_element_by_id('com.turrant:id/exit_layout').click()
    time.sleep(3)
    driver.find_element_by_id('com.turrant:id/btn_sure').click()

if __name__ == '__main__':
    certlist()