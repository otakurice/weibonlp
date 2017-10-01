# encoding:UTF-8
import pymysql,re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from snownlp import SnowNLP
from collections import Counter

def readmysql(): #读取数据库
    commentlist = []
    textlist = []
    userlist = []
    conn =pymysql.connect(host='服务器IP',user='用户名',password='密码',charset="utf8")    #连接服务器
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM xue.xueresponse WHERE id < '%d'" % 20)
        rows = cur.fetchall()
        for row in rows:
            row = list(row)
            del row[0]
            if row not in commentlist:
                commentlist.append([row[0],row[1],row[2],row[3],row[4],row[5]])
                comment_id = row[0]
                user_name = row[1]
                userlist.append(user_name)
                created_at = row[2]
                text = row[3]
                if text:
                    textlist.append(text)
                likenum = row[4]
                source = row[5]
            # print("%d %s %s %s %s %s" % (comment_id,user_name,created_at,text,likenum,source))
    return commentlist,userlist,textlist

def snowanalysis(textlist):
    sentimentslist = []
    for li in textlist:
        s = SnowNLP(li)
        # print(li)
        # print(s.sentiments)
        sentimentslist.append(s.sentiments)
    plt.hist(sentimentslist,bins=np.arange(0,1,0.02))
    plt.show()
    # sentimentslist.to_file('评论情感系数.png')
    # pd.DataFrame(sentimentslist).to_excel('薛之谦微博评论情感值.xlsx')
    # print(sentimentslist)

def emojilist(textlist):
    emojilist = []
    for li in textlist:
        emojis = re.findall(re.compile(u'(\[.*?\])',re.S),li)
        if emojis:
            for emoji in emojis:
                emojilist.append(emoji)
    emojidict = Counter(emojilist)
    print(emojidict)

def follows(textlist):
    userdict = Counter(userlist)
    print(userdict.most_common(20))

if __name__=='__main__':
    #运行
    commentlist,userlist,textlist = readmysql()
    snowanalysis(textlist)
    emojilist(textlist)
    follows(textlist)
