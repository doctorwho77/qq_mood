import re
from selenium import webdriver
from time import sleep
from PIL import Image

def getGTK(cookie):
    """ 根据cookie得到GTK """
    hashes = 5381
    for letter in cookie['p_skey']:
        hashes += (hashes << 5) + ord(letter)


    return hashes & 0x7fffffff


headers={
    'Host': 'h5.qzone.qq.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
    'Accept': '*/*',
    'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://user.qzone.qq.com/790178228?_t_=0.22746974226377736',
    'Connection':'keep-alive'
}

data={
    'qzreferrer':'https://qzs.qq.com/qzone/app/mood_v6/html/index.html#mood&uin=790178228&pfid=2&qz_ver=8&appcanvas=0&qz_style=35&params=&entertime=1497709695663&canvastype=&cdn_use_https=1',
    'uin':'790178228',
    'hostUin':'790178228',
    'topicId':'790178228_b429192f3d54a5578a1a0500',
    'commentUin':'790178228',
    'content':'评论一下',
    'richval':'',
    'richtype':'',
    'inCharset':'',
    'outCharset':'',
    'ref':'',
    'private':'0',
    'with_fwd':'0',
    'to_tweet':'0',
    'hostuin':'790178228',
    'code_version':'1',
    'format':'fs'
}
browser=webdriver.PhantomJS(executable_path="D:\phantomjs.exe")
url="https://qzone.qq.com/"
browser.get(url)
browser.maximize_window()
sleep(3)
browser.switch_to_frame("login_frame")
browser.find_element_by_id('switcher_plogin').click()
username=browser.find_element_by_id("u")
username.clear()
username.send_keys('3336534422')
password=browser.find_element_by_id("p")
password.clear()
password.send_keys('pengcheng1995')
browser.find_element_by_id("login_button").click()
sleep(3)

if '验证码' in browser.page_source :
    browser.get_screenshot_as_file('yzm.png')
    frame=browser.find_elements_by_tag_name('iframe')
    browser.switch_to_frame(frame_reference=frame)
    browser.get_screenshot_as_file('yzm.png')
    im = Image.open('yzm.png')
    im.show()
    yzm = str(input('输入验证码：'))
    cap=browser.find_element_by_id("capAns")
    cap.clear()
    cap.send_keys(yzm)
    tijiao=browser.find_element_by_id('submit')
    tijiao.submit()
#browser.get('https://user.qzone.qq.com/1186631324/taotao')
sleep(1)
print(browser.title)
cookie = {}
for elem in browser.get_cookies():
    cookie[elem['name']] = elem['value']
print('Get the cookie of QQ:%s successfully!(共%d个键值对)' % ('336534422', len(cookie)))
html = browser.page_source
g_qzonetoken=re.search(r'window\.g_qzonetoken = \(function\(\)\{ try\{return (.*?);\} catch\(e\)',html)
gtk=getGTK(cookie)
print(cookie)
print(gtk)
print(g_qzonetoken.group(1))
browser.quit()