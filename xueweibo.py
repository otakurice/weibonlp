# encoding:UTF-8
import pymysql,re,time,requests,urllib.request
from collections import OrderedDict

#薛回应P图 4154417035431509
#李转账捐款 4155545118733236
#鹿晗微博 4160547165300149
#关晓彤微博 4160547694498927
weibo_id = input('输入单条微博ID：')
# url='https://m.weibo.cn/single/rcList?format=cards&id=' + weibo_id + '&type=comment&hot=1&page={}' #爬热门评论
url='https://m.weibo.cn/api/comments/show?id=' + weibo_id + '&page={}' #爬时间排序评论
headers = {
    'User-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    'Host' : 'm.weibo.cn',
    'Accept' : 'application/json, text/plain, */*',
    'Accept-Language' : 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding' : 'gzip, deflate, br',
    'Referer' : 'https://m.weibo.cn/status/' + weibo_id,
    'Cookie' : '_T_WM=e25a28bec35b27c72d37ae2104433873; WEIBOCN_WM=3349; H5_wentry=H5; backURL=http%3A%2F%2Fm.weibo.cn%2F; SUB=_2A250zXayDeThGeVJ7VYV8SnJyTuIHXVUThr6rDV6PUJbkdBeLRDzkW1FrGCo75fsx_qRR822fcI2HoErRQ..; SUHB=0sqRDiYRHXFJdM; SCF=Ag4UgBbd7u4DMdyvdAjGRMgi7lfo6vB4Or8nQI4-9HQ4cLYm_RgdaeTdAH_68X4EbewMK-X4JMj5IQeuQUymxxc.; SSOLoginState=1506346722; M_WEIBOCN_PARAMS=featurecode%3D20000320%26oid%3D3638527344076162%26luicode%3D10000011%26lfid%3D1076031239246050; H5_INDEX=3; H5_INDEX_TITLE=%E8%8A%82cao%E9%85%B1',
    'DNT' : '1',
    'Connection' : 'keep-alive',
    }
i = 0
comment_num = 1
while True:
    # if i==1:     #26-31行 爬热门评论
    #     r = requests.get(url = url.format(i),headers = headers)
    #     comment_page = r.json()[1]['card_group']
    # else:
    #     r = requests.get(url = url.format(i),headers = headers)
    #     comment_page = r.json()[0]['card_group']
    r = requests.get(url = url.format(i),headers = headers)  #32-33行 爬时间排序评论
    comment_page = r.json()['data']
    if r.status_code ==200:
        try:
            print('正在读取第 %s 页评论：' % i)
            for j in range(0,len(comment_page)):
                print('第 %s 条评论' % comment_num)
                user = comment_page[j]
                comment_id = user['user']['id']
                print(comment_id)
                user_name = user['user']['screen_name']
                print(user_name)
                created_at = user['created_at']
                print(created_at)
                text = re.sub('<.*?>|回复<.*?>:|[\U00010000-\U0010ffff]|[\uD800-\uDBFF][\uDC00-\uDFFF]','',user['text'])
                print(text)
                likenum = user['like_counts']
                print(likenum)
                source = re.sub('[\U00010000-\U0010ffff]|[\uD800-\uDBFF][\uDC00-\uDFFF]','',user['source'])
                print(source + '\r\n')
                conn =pymysql.connect(host='服务器IP(默认是127.0.0.1)',user='服务器名(默认是root)',password='服务器密码',charset="utf8",use_unicode = False)    #连接服务器
                cur = conn.cursor()
                sql = "insert into nlp.love_guan(comment_id,user_name,created_at,text,likenum,source) values(%s,%s,%s,%s,%s,%s)"
                param = (comment_id,user_name,created_at,text,likenum,source)
                try:
                    A = cur.execute(sql,param)
                    conn.commit()
                except Exception as e:
                    print(e)
                    conn.rollback()
                comment_num+=1
            i+=1
            time.sleep(3)
        except:
            i+1
            pass
    else:
        break