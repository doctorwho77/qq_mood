import requests
import re
import datetime
from time import sleep
from urllib import parse
def comment(my_qq,target_qq,topicid,content,gtk,qzonetoken,cookie):
    data={
    'qzreferrer':'https://qzs.qq.com/qzone/app/mood_v6/html/index.html#mood&uin=790178228&pfid=2&qz_ver=8&appcanvas=0&qz_style=35&params=&entertime=1498019616488&canvastype=&cdn_use_https=1',
    'uin':my_qq,
    'hostUin':target_qq,
    'topicId':topicid,
    'commentUin':my_qq,
    'content':content,
    'richval':'',
    'richtype':'',
    'inCharset':'',
    'outCharset':'',
    'ref':'',
    'private':'0',
    'with_fwd':'0',
    'to_tweet':'0',
    'hostuin':my_qq,
    'code_version':'1',
    'format':'fs'
    }
    comment_data=parse.urlencode(data)
    content_length=str(data)
    comment_params={
    'g_tk':gtk,
    'qzonetoken':qzonetoken
    }
    comment_headers={
    'Host': 'h5.qzone.qq.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
    'Accept': '*/*',
    'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection':'keep-alive',
    'Content-Type':'application/x-www-form-urlencoded',
    'Content-Length':content_length,
    'Upgrade-Insecure-Requests':'1'
    }

    res=s.request('POST','https://h5.qzone.qq.com/proxy/domain/taotao.qzone.qq.com/cgi-bin/emotion_cgi_addcomment_ugc',params=comment_params,data=comment_data,headers=comment_headers,cookies=cookie)
    print(res.status_code)
    res=res.text
    print(res)
    commentid=re.findall('"id":(.*?),"postTime"',res)
    if commentid:
        f=open('target_qq.txt','a')
        f.write(str(topicid))
        f.write('  ')
        f.write(str(commentid[0]))
        f.write('\n')
        f.close()
        print('评论成功')
        return True
    else:
        print('评论失败')
        return False




headers={
    'Host': 'h5.qzone.qq.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
    'Accept': '*/*',
    'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://user.qzone.qq.com/790178228?_t_=0.22746974226377736',
    'Connection':'keep-alive'
}

cookie={'QZ_FE_WEBP_SUPPORT': '0', 'ptcz': '7cac1c7521b1ad8be9b1489f9b0aaba8efe9500f0f5dcb7693a9f693d37a8dff', 'fnc': '2', 'skey': '@F6CRfhQVd', 'pgv_si': 's493469696', 'ptui_loginuin': '790178228', 'RK': 'gYFn6+IOYo', 'pt2gguin': 'o0790178228', 'p_uin': 'o0790178228', 'rv2': '808A93A64B1A6FC5AE6D906AB5E744B38AF1EAA4163EC57A76', 'ptisp': 'ctc', 'p_skey': '5Iv6LkqOjJH*JPtrq0xqZmVlBNkbKLCRcDasiGGq71w_', '_qpsvr_localtk': '0.6656868932768703', 'pgv_pvi': '7208859648', '790178228_todaycount': '4', '__Q_w_s_hat_seed': '1', '790178228_totalcount': '24703', 'pgv_pvid': '1698820840', 'qz_screen': '1366x768', 'pt4_token': 'WeiGzJbrn*TO4HO4FFXRdiD3SpXE2UqW2Litsm-TZPw_', 'pgv_info': 'ssid=s6237051136', 'uin': 'o0790178228', 'Loading': 'Yes', 'property20': '9D827FD9F839B247CF95AA1787B450E4D22D6C9F2A76DC8C4D27798667EBB92CA7122514560889AF'}
gtk=
qzonetoken=
s=requests.session()
my_qq=
target_qq=
content='加油！'
cnt=0
for page in range(0,170):
    pos = page * 20
    params={
    'uin':target_qq,
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
    print(response.status_code)

    text=response.text
    if not re.search('lbs', text):
        print('全部说说评论完成,共添加评论%s条'% cnt)
        exit()
    textlist = re.split('\{"certified"', text)[0:]
    for i in range(1,len(textlist)):
        text=re.sub('"commentlist":.*?"conlist":','',textlist[i])
        tid = re.findall('"t1_termtype":.*?"tid":"(.*?)"', text)[0]
        topicid=target_qq+'_'+str(tid)
        print(topicid)
        counts=comment(my_qq=my_qq,target_qq=target_qq,content=content,topicid=topicid,gtk=gtk,qzonetoken=qzonetoken,cookie=cookie)
        sleep(180)
        if counts==True:
            cnt=cnt+1





