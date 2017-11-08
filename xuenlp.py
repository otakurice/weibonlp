# encoding:UTF-8
import pymysql,re
import jieba
import jieba.posseg as pseg
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import imread
from snownlp import SnowNLP
from wordcloud import WordCloud,ImageColorGenerator
from collections import Counter

def readmysql(): #读取数据库
    commentlist = []
    textlist = []
    userlist = []
    conn =pymysql.connect(host='服务器IP',user='用户名',password='密码',charset="utf8")    #连接服务器
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM nlp.love_guan WHERE id < '%d'" % 10000)
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

def wordtocloud(textlist):
    fulltext = ''
    isCN = 1
    back_coloring = imread("bg.jpg")
    cloud = WordCloud(font_path='font.ttf', # 若是有中文的话，这句代码必须添加，不然会出现方框，不出现汉字
            background_color="white",  # 背景颜色
            max_words=2000,  # 词云显示的最大词数
            mask=back_coloring,  # 设置背景图片
            max_font_size=100,  # 字体最大值
            random_state=42,
            width=1000, height=860, margin=2,# 设置图片默认的大小,但是如果使用背景图片的话,那么保存的图片大小将会按照其大小保存,margin为词语边缘距离
            )
    for li in textlist:
        fulltext += ' '.join(jieba.cut(li,cut_all = False))
    wc = cloud.generate(fulltext)
    image_colors = ImageColorGenerator(back_coloring)
    plt.figure("wordc")
    plt.imshow(wc.recolor(color_func=image_colors))
    wc.to_file('微博评论词云.png')

def snowanalysis(textlist):
    sentimentslist = []
    for li in textlist:
        s = SnowNLP(li)
        # print(li)
        # print(s.sentiments)
        sentimentslist.append(s.sentiments)
    fig1 = plt.figure("sentiment")
    plt.hist(sentimentslist,bins=np.arange(0,1,0.02))
    plt.show()

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
    wordtocloud(textlist)
    snowanalysis(textlist)
    emojilist(textlist)
    follows(textlist)
