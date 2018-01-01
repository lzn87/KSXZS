#!/usr/bin/python3
#encoding:utf8

from wxpy import *
import re
import sqlite3
import time

class select():
    dict = {'0417': 'ict', '0450': 'ibiz', '0455': 'iecon', '0500': 'eng1', '0511': 'eng2', '0580': 'imath',
            '0610': 'ibio', '0620': 'ichem', '0625': 'iphy', '9231': 'fm', '9608': 'cs', '9609': 'abiz',
            '9695': 'lit', '9698': 'psy', '9700': 'abio', '9701': 'achem', '9702': 'aphy', '9708': 'aecon',
            '9709': 'amath'}
    #判断输入的指令是否合法
    def legal(self,data):
        inputs = data.split(' ')
        if re.match(u'^建议', data, re.U) :
            return None
        else:
            for input in inputs:
                if len(input) == 4 and input.isdigit():
                    continue
                elif (len(input) == 2 or len(input) == 1) and input.isdigit():
                    continue
                elif input.lower() in dict.values():
                    continue
                elif input in ['ms', 'qp', 's', 'w','S','W']:
                    continue
                elif re.match('^[0-9]{4}[_]{1}.[0-9]{2}[_]{1}[a-z]{2}[_]{1}[0-9]{2}', input):
                    continue
                else:
                    return False

    def search(self, input):
        lzn = select()

        if lzn.legal(input) == False:
            return None
        elif re.match(u'^建议', input, re.U) or re.match(u'谢', input, re.U):
            return None

        conditions = input.split(' ')
        conn = sqlite3.connect('file_location.sqlite')
        cur = conn.cursor()
        command = ["SELECT location FROM File where"]

        for condition in conditions:
            if len(condition) == 4 and condition.isdigit():
                #year
                if condition.startswith('2'):
                    year = int(condition)
                    command.append('year = %d' % year)
                #syallbus
                elif re.match('^[0][0-9]{3}', condition) or re.match('^[9][0-9]{3}', condition):
                    syllabus = int(condition)
                    command.append('syllabus = %d' % syllabus)
            #month
            elif condition.lower() in ['s','w']:
                month = condition.lower()
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
        print (order)
        cur.execute(order)

        result = []

        rows = cur.fetchall()
        if len(rows) == 0:
            return '小助手在你给的条件下没有找到一张卷子...😅'
        elif len(rows) > 10:
            return '符合你要求的卷子太多了[捂脸]...请你再多加些条件...'
        else:
            for row in rows:
                for paper in row:
                    result.append(paper)
            return result

bot = Bot(cache_path=True, console_qr=-2)
group = bot.groups()
friends = bot.friends(update=True)
None_group = bot.groups().search(None)

@bot.register(friends,except_self=True)
def return_pdf(msg):
    content = msg.text
    lzn = select()
    if lzn.legal(content) is None and lzn.search(content) is not None:
        results = lzn.search(content)
        if lzn.legal(content) is None and len(results) < 10:
            msg.reply('在你给的条件下我一共找到了%d张卷子，给你( つ•̀ω•́)つ'%len(results))
            for result in results:
                msg.reply_file(result)
        elif lzn.legal(content) is None and len(results) >= 10:
            msg.reply(lzn.search(content))
    elif re.match('谢', content):
        msg.reply('和机器人客气什么[嘿哈]')
    elif re.match('建议',content):
        conn = sqlite3.connect('feedbacks.db')
        conn.text_factory=str
        cur = conn.cursor()
        cur.execute('''INSERT INTO feedback (user_name, time, content)
                                VALUES ( ?, ?, ?)''', (str(msg.chat), int(time.time()), content))
        conn.commit()
        msg.reply('谢谢你的反馈😁小(cheng)助(xu)手(yuan)会尽快做出调整的')
    elif lzn.legal(content) == False:
        msg.reply( '看不懂你的要求啊😢请你再检查一下你输入的条件...')

@bot.register(group)
def ignore(msg):
    return

@bot.register(msg_types=FRIENDS)
def auto_accept_friends(msg):
    global friends
    new_friend = bot.accept_friend(msg.card)
    new_friend.send('同学你好～下面是考试小助手的使用指南')
    new_friend.send_file('ksxzs.pdf')
    new_friend.send('刚加小助手的同学需要等它好友列表更新后才能得到回复，抱歉[捂脸]')
    friends = bot.friends(update = True)

embed()