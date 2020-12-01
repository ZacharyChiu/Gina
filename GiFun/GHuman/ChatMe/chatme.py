# -*- coding = utf-8 -*-
# Author: Zachary
# @Time: 2020/10/4 16:47

import os
import requests
import random
import json
import urllib.request


#加载我的自制语料库
Q_s = []
dic_re = {}
f = open('D:\\#My\\GiData\\Creation\\Projects\\Python\\Gina\\GiFun\\GShow\\Gina_tkinter\\YumLnu\\Dictionary.txt')
total = f.read()
Q_bag = total.split('\nQ:\n')
for i in range(1,len(Q_bag)):	#以问题包为单位打开
    q_and_a = Q_bag[i].split('[;]')
    questions = q_and_a[0].split('[,]')#相似问题集
    Q_s.append(questions)#总问题集
    answers = q_and_a[1].split('[.]')#回答集
    dic_re[questions[0]] = answers


tuling='e801dc91c11f4f75ae790d120c1c1fee'
api_url = "http://openapi.tuling123.com/openapi/api/v2"
userid = 'Zachary'
def get_message(message,userid):
    req = {
    "reqType":0,
    "perception": {
        "inputText": {
            "text": message
        },
        "inputImage": {
            "url": "imageUrl"
        },
        "selfInfo": {
            "location": {
                "city": "宜兴",
                "province": "江苏",
                "street": ""
            }
        }
    },
    "userInfo": {
        "apiKey": tuling,
        "userId": userid
    }
}
    req = json.dumps(req).encode('utf8')
    http_post = urllib.request.Request(api_url, data=req, headers={'content-type': 'application/json'})
    response = urllib.request.urlopen(http_post)
    response_str = response.read().decode('utf8')
    response_dic = json.loads(response_str)
    results_text = response_dic['results'][0]['values']['text']
    return results_text

#本地语料
def chat(order):
    answer = ''
    for questions in Q_s:
        if order in questions:
            order = questions[0]
            choice = random.sample(range(0,len(dic_re[questions[0]])),1)#摇号
            choice = choice[0]#获得答案编号
            answer = dic_re[questions[0]][choice]
    if answer == '':
        answer = get_message(order,userid)
    return(answer)
# ask = input('$ Zachary：')
# re = chat(ask)
# print('$ 姬娜：'+re)
