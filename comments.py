#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# 原始代码借鉴于知乎专栏 https://zhuanlan.zhihu.com/p/32547780

import aiohttp
import asyncio
import json
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import time
from random import choice
import motor.motor_asyncio


questionId = 267189851
num = 1

f = open('comments%d.txt' % questionId, 'w', encoding='utf-8')


async def get_answers(question_id):
    headers = {
        'Cookie': '将自己的cookie复制到这里'
    }
    data = {
        'include':
'data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annot\
ation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_commen\
t,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_ti\
me,updated_time,review_info,question,excerpt,relationship.is_authorized,is_author,voting,i\
s_thanked,is_nothelp,upvoted_followees;data[*].mark_infos[*].url;data[*].author.follower_c\
ount,badge[?(type=best_answerer)].topics',
        'offset': '0',
        'limit': '20',
        'sort_by': 'default'
    }
    next_url = 'https://www.zhihu.com/api/v4/questions/{}/answers?'.format(
        question_id) + urlencode(data)
    while next_url:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(next_url) as response:
                if response.status == 200:
                    next_url = await parse(await response.text())
                    time.sleep(choice(range(1, 6)))
                else:
                    print(response.status)


async def parse(response):
    json_data = json.loads(response)
    next_url = json_data['paging']['next']
    for data in json_data['data']:
        bsobj = BeautifulSoup(data['content'], 'lxml')
        document = {
            'content': bsobj.get_text()
        }
        await do_insert(document)
    return next_url


async def do_insert(document):
    global num
    piece_word = '%04d' % num + document['content'] + '\n'
    f.write(piece_word)
    f.flush()
    print(piece_word)
    num += 1


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    tasks = [get_answers(questionId)]
    try:
        loop.run_until_complete(asyncio.wait(tasks))
    except SystemExit:
        print("caught SystemExit!")
        task.exception()
        raise
    finally:
        f.close()
        loop.close()
