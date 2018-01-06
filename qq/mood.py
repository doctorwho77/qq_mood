import requests
import re
import datetime
import MySQLdb
import pandas as pd
from ArticleSpider.qq import QRlogin

def parse_mood(i):
    '''从返回的json中，提取我们想要的字段'''
    text = re.sub('"commentlist":.*?"conlist":', '', i)
    if text:
        myMood = {}
        myMood["isTransfered"] = False
        tid = re.findall('"t1_termtype":.*?"tid":"(.*?)"', text)[0]  # 获取说说ID
        tid = qq + '_' + tid
        myMood['id'] = tid
        myMood['pos_y'] = 0
        myMood['pos_x'] = 0
        mood_cont = re.findall('\],"content":"(.*?)"', text)
        if re.findall('},"name":"(.*?)",', text):
            name = re.findall('},"name":"(.*?)",', text)[0]
            myMood['name'] = name
        if len(mood_cont) == 2:  # 如果长度为2则判断为属于转载
            myMood["Mood_cont"] = "评语:" + mood_cont[0] + "--------->转载内容:" + mood_cont[1]  # 说说内容
            myMood["isTransfered"] = True
        elif len(mood_cont) == 1:
            myMood["Mood_cont"] = mood_cont[0]
        else:
            myMood["Mood_cont"] = ""
        if re.findall('"created_time":(\d+)', text):
            created_time = re.findall('"created_time":(\d+)', text)[0]
            temp_pubTime = datetime.datetime.fromtimestamp(int(created_time))
            temp_pubTime = temp_pubTime.strftime("%Y-%m-%d %H:%M:%S")
            dt = temp_pubTime.split(' ')
            time = dt[1]
            myMood['time'] = time
            date = dt[0]
            myMood['date'] = date
        if re.findall('"source_name":"(.*?)"', text):
            source_name = re.findall('"source_name":"(.*?)"', text)[0]  # 获取发表的工具（如某手机）
            myMood['tool'] = source_name
        if re.findall('"pos_x":"(.*?)"', text):
            pos_x = re.findall('"pos_x":"(.*?)"', text)[0]
            pos_y = re.findall('"pos_y":"(.*?)"', text)[0]
            if pos_x:
                myMood['pos_x'] = pos_x
            if pos_y:
                myMood['pos_y'] = pos_y
            idname = re.findall('"idname":"(.*?)"', text)[0]
            myMood['idneme'] = idname
            cmtnum = re.findall('"cmtnum":(.*?),', text)[0]
            myMood['cmtnum'] = cmtnum
        return myMood
#从csv文件中取qq号，并保存在一个列表中
scv=pd.read_csv('QQmail.csv', encoding='utf-8',usecols=[2])
friend=[]
for indexs in scv.index:
    friend.append(scv.loc[indexs].values)
friends=[]
for f in friend:
    f=str(f).strip("[]'")
    if re.search('@qq.com',f):
        f = f[:-7]
        friends.append(f)
headers={
    'Host': 'h5.qzone.qq.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
    'Accept': '*/*',
    'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://user.qzone.qq.com/790178228?_t_=0.22746974226377736',
    'Connection':'keep-alive'
}#伪造浏览器头
conn = MySQLdb.connect('localhost', 'root', '123456', 'qq_mood', charset="utf8", use_unicode=True)#连接mysql数据库
cursor = conn.cursor()#定义游标
cookie,gtk,qzonetoken=QRlogin.QR_login()#通过登录函数取得cookies，gtk，qzonetoken
s=requests.session()#用requests初始化会话
for qq in friends:#遍历qq号列表
    for p in range(0,1000):
        pos=p*20
        params={
        'uin':qq,
        'ftype':'0',
        'sort':'0',
        'pos':pos,
        'num':'20',
        'replynum':'100',
        'g_tk':gtk,
        'callback':'_preloadCallback',
        'code_version':'1',
        'format':'jsonp',
        'need_private_comment':'1',
        'qzonetoken':qzonetoken
        }

        response=s.request('GET','https://h5.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6',params=params,headers=headers,cookies=cookie)
        print(response.status_code)#通过打印状态码判断是否请求成功
        text=response.text#读取响应内容
        if not re.search('lbs', text):#通过lbs判断此qq的说说是否爬取完毕
            print('%s说说下载完成'% qq)
            break
        textlist = re.split('\{"certified"', text)[1:]
        for i in textlist:
            myMood=parse_mood(i)
            '''将提取的字段值插入mysql数据库，通过用异常处理防止个别的小bug中断爬虫，开始的时候可以先不用异常处理判断是否能正常插入数据库'''
            try:
                insert_sql = '''
                           insert into mood(id,content,time,sitename,pox_x,pox_y,tool,comments_num,date,isTransfered,name)
                           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        '''
                cursor.execute(insert_sql, (myMood['id'],myMood["Mood_cont"],myMood['time'],myMood['idneme'],myMood['pos_x'],myMood['pos_y'],myMood['tool'],myMood['cmtnum'],myMood['date'],myMood["isTransfered"],myMood['name']))
                conn.commit()
            except:
                pass





print('说说全部下载完成！')
