#!/usr/bin/env python
# -*- coding: utf-8 -*-
#@Author : Aixiu

import json
import os
import random
from datetime import datetime

import requests
from flask import Flask, jsonify, request

import config

'''
参考文件：https://zhuanlan.zhihu.com/p/425971516
'''

app = Flask(__name__)

# 路由解析，通过用户访问的路径，匹配相应的函数
# @app.route('/')
# def home():
#     # 模拟访问豆瓣
#     url = request.args.get('name')
     
#     return url

# 解决浏览器中json数据，中文无法展示的问题
app.config['JSON_AS_ASCII']=False   # 中文正常化，解决乱码
app.config['JSON_SORT_KEYS']=False   # json不排序
app.config['JSONIFY_PRETTYPRINT_REGULAR']=True  # 输出json格式化完美显示
app.config["JSONIFY_MIMETYPE"] = "application/json;charset=utf-8"   # 指定浏览器渲染的文件类型，和解码格式；

@app.route('/')
def home():
    vod_douban_id  = request.args.get('id')
    
    if vod_douban_id is None or vod_douban_id == '':
        error_data = {
            'code': 400,
            'msg': '非法请求',
            'info': '本是清灯不归客，却因浊酒恋红尘。',
            'date': datetime.now().strftime(r"%Y-%m-%d %H:%M:%S")
        }
        return jsonify(error_data)

    url = f'https://movie.douban.com/subject/{vod_douban_id}/'
    
    flie_path = f'./douban'
    
    # 创建一个文件夹，保存所有的图片
    if not os.path.exists(flie_path):
        os.mkdir('./douban/')
    
    # 获取文件夹下所有文件名
    file_name_list = os.listdir(flie_path)    


    #判读豆瓣ID文件是否存在如果存在，直接读文件，如果不存在爬取数据并保存
    if f'{vod_douban_id}.json' in file_name_list:
        with open(f'{flie_path}/{vod_douban_id}.json', mode='r', encoding='utf-8') as fp:
            json_data = json.load(fp=fp)            
        return jsonify(json_data)   
        # jsonify将字典转为json,并返回给前端content-type：application/json
    else:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53'
            }
            page_text = requests.post(url=url, headers=headers, timeout=20)
            page_text_data = requests.post(url=url, headers=headers, timeout=20)
            page_text_data.raise_for_status()
            page_text_data.encoding = page_text_data.apparent_encoding
            page_text = page_text_data.text
            
            vod_name = config.vod_name(page_text=page_text)
            vod_year = config.vod_year(page_text=page_text)
            vod_lang = config.vod_lang(page_text=page_text)
            vod_sub = config.vod_sub(page_text=page_text)
            vod_pic = config.vod_pic(page_text=page_text)
            vod_class = config.vod_class(page_text=page_text)
            vod_actor = config.vod_actor(page_text=page_text)
            vod_writer = config.vod_writer(page_text=page_text)
            vod_score = config.vod_score(page_text=page_text)                
            vod_content = config.vod_content(page_text=page_text)
            vod_area = config.vod_area(page_text=page_text)
            vod_director = config.vod_director(page_text=page_text)
            vod_pubdate = config.vod_pubdate(page_text=page_text)
            vod_duration = config.vod_duration(page_text=page_text)
            vod_remarks = config.vod_remarks(page_text=page_text)
    
            
            # 国语或英文中字
            # if '中国' or '台湾' in vod_area:
            #     vod_remarks = "高清国语"   
            # else:
            #     vod_remarks = "高清中字"            
            
            vod_total =  vod_remarks
            vod_score_num =  random.randint(100, 1000)
            vod_score_all =  random.randint(200, 500)
            vod_douban_score =  vod_score        
            vod_reurl = url   # 豆瓣地址
            
            vod_data = {
                "vod_name": vod_name,
                "vod_sub": vod_sub,
                "vod_pic": vod_pic,
                "vod_year": vod_year,
                "vod_lang": vod_lang,
                "vod_class": vod_class,
                "vod_actor": vod_actor,
                "vod_content": vod_content,
                "vod_writer": vod_writer,
                "vod_area": vod_area,
                "vod_remarks": vod_remarks,
                "vod_director": vod_director,
                "vod_pubdate": vod_pubdate,
                "vod_total": vod_total,
                "vod_score": vod_score,
                "vod_douban_score": vod_douban_score,
                "vod_score_num": vod_score_num,
                "vod_score_all": vod_score_all,
                "vod_duration": vod_duration,
                "vod_reurl": vod_reurl,
                "vod_douban_id": vod_douban_id,        
            }        
    
            with open(f'{flie_path}/{vod_douban_id}.json', mode='w', encoding='utf-8') as fp:
                json.dump(vod_data, fp=fp, ensure_ascii=False, indent=4)
            
            return jsonify(vod_data)
            
        except Exception :
            error_data = {
                'code': 404,
                'msg': 'ID不合法',
                'info': '一切有为法，如梦幻泡影，如露亦如电，当作如是观。',
                'date': datetime.now().strftime(r"%Y-%m-%d %H:%M:%S")
            }
            return jsonify(error_data)



if __name__ == '__main__':
    app.run()
