import re
from selenium import webdriver
from time import sleep
from PIL import Image

#定义登录函数
def QR_login():
    def getGTK(cookie):
        """ 根据cookie得到GTK """
        hashes = 5381
        for letter in cookie['p_skey']:
            hashes += (hashes << 5) + ord(letter)

        return hashes & 0x7fffffff
    browser=webdriver.PhantomJS(executable_path="D:\phantomjs.exe")#这里要输入你的phantomjs所在的路径
    url="https://qzone.qq.com/"#QQ登录网址
    browser.get(url)
    browser.maximize_window()#全屏
    sleep(3)#等三秒
    browser.get_screenshot_as_file('QR.png')#截屏并保存图片
    im = Image.open('QR.png')#打开图片
    im.show()#用手机扫二维码登录qq空间
    sleep(20)#等二十秒，可根据自己的网速和性能修改
    print(browser.title)#打印网页标题
    cookie = {}#初始化cookie字典
    for elem in browser.get_cookies():#取cookies
        cookie[elem['name']] = elem['value']
    print('Get the cookie of QQlogin successfully!(共%d个键值对)' % (len(cookie)))
    html = browser.page_source#保存网页源码
    g_qzonetoken=re.search(r'window\.g_qzonetoken = \(function\(\)\{ try\{return (.*?);\} catch\(e\)',html)#从网页源码中提取g_qzonetoken
    gtk=getGTK(cookie)#通过getGTK函数计算gtk
    browser.quit()
    return (cookie,gtk,g_qzonetoken.group(1))
if __name__=="__main__":
    QR_login()