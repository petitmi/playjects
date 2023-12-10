#coding=utf8
import requests
import itchat
import random
import pandas as pd
import codecs
import re
from datetime import datetime
import time
def transfer_meaning(text):
    return codecs.escape_decode(bytes(text, 'utf-8'))[0].decode('utf-8')
def get_response(msg):
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key'    : 'c9b38fc693dc409ebea513352be80146',    #这里自行输入key
        'info'   : msg,
        'userid' : '175007',     #这是我的账号
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        return r.get('text')
    except:
        return "啥意思"    #出问题就回复“呵呵”

itchat.auto_login(hotReload=True)    #热启动，不需要多次扫码登录

def timer(username):
    while True:
        cur_time = time.localtime(time.time())
        # (and cur_time.tm_min == 20) and (cur_time.tm_sec == 0)
        if ((cur_time.tm_hour == 17) ):
            if cur_time.tm_sec==0:
                itchat.send("五点计时器：%s:%s"%(cur_time.tm_hour,cur_time.tm_min ), toUserName=username)
        time.sleep(1)

#全部好友
# friends = str(itchat.get_friends(update=True))
# #定位好友
# user_text=re.search(r"'NickName': '中华永力狗'",friends)
# user_start=user_text.start()
# user_define=friends[user_start-100:user_start+40]
# #匹配好友username
# re_username=re.compile("'UserName': '(.*?)', 'NickName': '中华永力狗'")
# username = re_username.findall(user_define)[0]
# #定时器
# timer(username)

@itchat.msg_register(itchat.content.TEXT,isFriendChat=True)
def first_reply(msg):
    if '0' in msg['Text']:
        csv_peom = pd.read_csv(r'/Users/petitmi/Downloads/pythonCode/code/wechat_reply/peom_y.csv', error_bad_lines=False)
        peom = csv_peom.iloc[random.randint(0, len(csv_peom)-1),]
        reply=peom.标题+'\n文/'+peom.作者+'\n\n'+transfer_meaning(peom.诗)
    elif '好诗' in msg['Text']:
        reply='谢谢！'
    else:
        pass
        reply=get_response(msg)
        # reply = "小弥弥子正在吃饭，回复0看诗"
    return reply
itchat.run()
