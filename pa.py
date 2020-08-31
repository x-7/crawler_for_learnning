# -*- coding: UTF-8 -*-
from selenium import webdriver
import json
import time

output='./medicine.txt'
mobileEmulation = {'deviceName': 'iPhone 6/7/8'}   #设置手机环境
options = webdriver.ChromeOptions()
options.add_argument('headless')    #设置不显示页面
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option('mobileEmulation', mobileEmulation)
#executable_path 为chromedriver文件路径，chromedriver是谷歌浏览器驱动软件
driver = webdriver.Chrome(executable_path='./chromedriver', options=options)
URL = '{your url}'


def pa(i):
    url = URL+ str(i)
    driver.get(url)
    xpath_drug = "//body"
    data = driver.find_elements_by_xpath(xpath_drug)

    # 清洗获取的数据，tag = True 是数据不为空
    info = ""
    tag = True
    for i2 in data:
        if i2.text == "[]":
            tag = False
        else:
            info += str(i2.text)
    if tag == True:
        d = info.split("},{")
        info = "},{".join(d[:-1]) + "}]"
    # # 关闭
    # driver.quit()
    if info=="}]":
        print("exit with id: {}".format(i))
        raise Exception('exit with id {}'.format(i))
    return info


def get_file_line_counts(file_name):
    with open(file_name,mode='r') as f:
        count=len(f.readlines())
    return count


if __name__ == "__main__":
    total=168760
    count=get_file_line_counts(output)
    start = count+1
    start_time = time.time()
    s50=""
    with open(output,mode='a') as f:
        for i in range(start,total+1):
            info = pa(i)
            s50=s50+info+"\n"
            if i%10==0:
                f.write(s50)
                s50=""
                finished = i-start+1
                left = total-i
                cost = time.time()-start_time
                left_time = left/(finished/cost)
                print('index:{},cost:{} minute,left time:{} minute'.format(i,int(cost/60),int(left_time/60)))
        f.write(s50)
        print('over')
    driver.quit()