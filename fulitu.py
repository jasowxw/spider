# -*- coding: UTF-8 -*-
'''
@Project ：spider_demo 
@File    ：demo.py
@IDE     ：PyCharm 
@Author  ：闻小文
@Date    ：2021/11/28 22:55 
@win_name   ：wzw
'''
from concurrent.futures import ThreadPoolExecutor

import requests
from bs4 import BeautifulSoup
import time


def put_page_url(num):
    """
    生成器，每次迭代返回一整页的URL
    :param num:最大页数
    :return:抛出一个URL
    """
    for i in range(1,num+1):
        yield f'https://www.fulitu.cc/category/jiaokong/{i}'


def get_html(url):
    """
    一个获取具体html页面的生成器，抛出每一份图片的URL
    :param url:
    :return:
    """
    response = requests.get(url=url)
    #创建soup对象
    soup = BeautifulSoup(response.text, 'lxml')
    #获取结点
    div_class_content = soup.html.body(name='div', attrs={'class': 'content'})[0]
    div_id_masonry = div_class_content.find_all(name='div', id='masonry', class_='archive row')[0]
    iterator_img = div_id_masonry.children
    #字典存储每页中的具体URL，和其对应的名字
    img_dict = []
    for i in iterator_img:
        if i != '\n':
            # name = i.img['alt']
            url = i.div.a['href']
            # img_dict[name] = url
            yield url



def get_img(html):

    # for i in img_dict.items():
    #对具体页面发起请求
    response = requests.get(url=html)
    #得到每一张图片的URL
    soup = BeautifulSoup(response.text, 'lxml')
    div_class_content = soup.body(name='div', class_='content')[0]
    div_id_masonry = div_class_content(name='div', class_='post row')[0]
    for i in div_id_masonry.children:
        if i != '\n':
            img_name = i.img['alt']
            img_url = 'https:' + i['data-src']
            #下载图片
            with open(img_name + '.jpg', mode='wb') as fp:
                fp.write(requests.get(img_url).content)


def get_time(fun):
    def wraaper():
        start = time.time()
        fun()
        end = time.time()
        print(f'用时：{end-start}')
    return wraaper

@get_time
def main():
    #创建一个线程池，最大线程数为8
    with ThreadPoolExecutor(max_workers=8) as pool:
        #一个获取没一大页的循环
        for page_url in put_page_url(4):
            print(page_url)
            #一个获取每一大页中具体的每一份图片的循环
            for html_url in get_html(page_url):
                print(html_url)
                #用来下载每一张图片
                pool.submit(get_img,html_url)


if __name__ == '__main__':
    main()

