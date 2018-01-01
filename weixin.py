#coding=utf-8
import sys
import web
import hashlib
import xml.etree.ElementTree as ET
import time
import sqlite3
import re
from sqlite3 import Error as e

reload(sys)
sys.setdefaultencoding('utf8')

urls = (
    '/', 'index'
)
render = web.template.render('templates/')

class select():
    #判断输入的指令是否合法
    def legal(self,data):
        dict = {'0417': 'ict', '0450': 'ibiz', '0455': 'iecon', '0500': 'eng1', '0511': 'eng2', '0580': 'imath',
                '0610': 'ibio', '0620': 'ichem', '0625': 'iphy', '9231': 'fm', '9608': 'cs', '9609': 'abiz',
                '9695': 'lit', '9698': 'psy', '9700': 'abio', '9701': 'achem', '9702': 'aphy', '9707':'abiz','9708': 'aecon',
                '9709': 'amath'}
        inputs = data.split(' ')
        if re.match(u'^建议', data, re.U):
            return None
        else:
            for input in inputs:
                if len(input) == 4 and input.isdigit():
                    continue
                elif (len(input) == 2 or len(input) == 1) and input.isdigit():
                    continue
                elif input.lower() in dict.values():
                    continue
                elif input in ['ms', 'qp', 's', 'w']:
                    continue
                elif re.match('^[0-9]{4}[_]{1}.[0-9]{2}[_]{1}[a-z]{2}[_]{1}[0-9]{2}', input):
                    continue
                else:
                    return False

    def search(self, input):
        lzn = index()
        dict = {'0417': 'ict', '0450': 'ibiz', '0455': 'iecon', '0500': 'eng1', '0511': 'eng2', '0580': 'imath',
                '0610': 'ibio', '0620': 'ichem', '0625': 'iphy', '9231': 'fm', '9608': 'cs', '9609': 'abiz',
                '9695': 'lit', '9698': 'psy', '9700': 'abio', '9701': 'achem', '9702': 'aphy', '9707':'abiz','9708': 'aecon',
                '9709': 'amath'}

        if lzn.legal(input) == False:
            return None
        elif re.match(u'^建议', input, re.U):
            return None
        try:
            conditions = input.split(' ')

            conn = sqlite3.connect('file_location.sqlite')
            cur = conn.cursor()
            command = ["SELECT location FROM File where"]

            for condition in conditions:
                if len(condition) == 4 and condition.isdigit():
                    #year
                    if condition in ['2010','2011','2012','2013','2014','2015','2016']:
                        year = int(condition)
                        command.append('year = %d' % year)
                    #syallbus
                    elif re.match('^[0][0-9]{3}', condition) or re.match('^[9][0-9]{3}', condition):
                        syllabus = int(condition)
                        command.append('syllabus = %d' % syllabus)
                #month
                elif condition in ['s','w']:
                    month = condition
                    command.append('month = %s' % '"'+month+'"')
                #p_
                elif condition == '1' or condition == '2' or condition == '3' or condition == '4' \
                        or condition == '5' or condition == '6' or condition == '7':
                    paper_number = int(condition)
                    command.append('paper_number = %d' % paper_number)
                #p__
                elif condition.isdigit() and len(condition) == 2 and condition[0] in ['1','2','3','4','5','6','7']\
                        and condition[1] in ['1','2','3']:
                    component = int(condition)
                    command.append('component = %d'%component)
                #type:ms or qp
                elif condition == 'ms':
                    type = 'ms'
                    command.append('type = %s' % '"' + type + '"')
                elif condition == 'qp':
                    type = 'qp'
                    command.append('type = %s' % '"' + type + '"')
                #subject
                elif condition.lower() in dict.values():
                    convert = {'ict': 'ICT', 'ibiz': 'IBiz', 'iecon': 'IEcon', 'eng1': 'Eng1', 'eng2': 'Eng2', 'imath': 'IMath',
                     'ibio': 'IBio', 'ichem': 'IChem', 'iphy': 'IPhy', 'fm': 'FM', 'cs': 'CS', 'abiz': 'ABiz',
                     'lit': 'Lit', 'psy': 'Psy', 'abio': 'ABio', 'achem': 'AChem', 'aphy': 'APhy', 'aecon': 'AEcon',
                     'amath': 'AMath'}
                    subject = convert[condition.lower()]
                    command.append('subject = %s' % '"' + subject + '"')
                elif re.match('^[0-9]{4}[_]{1}.[0-9]{2}[_]{1}[a-z]{2}[_]{1}[0-9]{2}', condition):
                    file_name = condition
                    command.append('file_name = %s' % '"'+file_name+'"')
            order = ' and '.join(command).replace(' and', '', 1)
            print order
            cur.execute(order)

            result = []

            rows = cur.fetchall()
            if len(rows) == 0:
                return '哎呀，小助手在你给的条件下没有找到一张卷子...😅'
            elif len(rows) > 20:
                return '符合你要求的卷子太多了[捂脸]...请你再多加些条件...'
            else:
                for row in rows:
                    for paper in row:
                        result.append(paper)
                return result

        except e:
            print "Error: %s" % e.args[0]

class index(select):

    def GET(self):
        data = web.input()
        signature = data.signature
        timestamp = data.timestamp
        nonce = data.nonce
        echostr = data.echostr
        token = "lzn"
        list = [token, timestamp, nonce]
        list.sort()
        sha1 = hashlib.sha1()
        map(sha1.update, list)
        hashcode = sha1.hexdigest()

        if hashcode == signature:
            return echostr

    def POST(self):
        lzn = index()
        str_xml = web.data()  # 获得post来的数据
        xml = ET.fromstring(str_xml)  # 进行XML解析
        content = xml.find("Content").text  # 获得用户所输入的内容
        msgType = xml.find("MsgType").text
        fromUser = xml.find("FromUserName").text
        toUser = xml.find("ToUserName").text
        if lzn.legal(content) is None and lzn.search(content) is not None:
            results = lzn.search(content)
            if lzn.legal(content) is None and len(results) < 20:
                reply = "在你给的条件下我一共找到了%d张卷子，给你( つ•̀ω•́)つ\n"%len(results)
                for result in results:
                    reply += result + "\n"
                return render.reply_text(fromUser, toUser, int(time.time()), reply)
            elif lzn.legal(content) is None and len(results) >= 20:
                reply = lzn.search(content)
                return render.reply_text(fromUser, toUser, int(time.time()), reply)
        elif re.match(u'^建议', content, re.U):
            conn = sqlite3.connect('feedbacks.db')
            conn.text_factory = str
            cur = conn.cursor()
            cur.execute('''INSERT INTO feedback (user_name, time, content)
                        VALUES ( ?, ?, ?)''', (str(toUser),int(time.time()),content))
            conn.commit()
            return render.reply_text(fromUser, toUser, int(time.time()), '谢谢你的反馈😁小(cheng)助(xu)手(yuan)会尽快做出调整的')
        elif lzn.legal(content) == False:
            return render.reply_text(fromUser, toUser, int(time.time()), '小助手看不懂你要求啊😢请你再检查一下你输入的条件...')
        else:
            return 'success'


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

