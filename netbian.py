# -*- coding: UTF-8 -*-
'''
@Project ：spider_demo 
@File    ：netbian爬取.py
@IDE     ：PyCharm 
@Author  ：闻小文
@Date    ：2021/10/4 16:35 
@win_name   ：wzw
'''
import time
import random

import requests
import bs4
import threading



# lock = threading.Lock()


# url = 'http://www.netbian.com/meinv/index.htm'
def get_url_list(page):
    """
    获取指定页数的URL
    :param page: 页数最大值
    :return: 返回一个URL列表
    """
    url_list = ['http://www.netbian.com/meinv/index.htm']
    if int(page) <= 1:
        return url_list
    else:
        for i in range(2,int(page)+1):
            url = f'http://www.netbian.com/meinv/index_{i}.htm'
            url_list.append(url)
        return url_list


def get_html(url_):
    """
    获取每一个页面的每一张图片的详细URL
    :param url_:每一页的URL
    :return: none
    """
    jpg_urls = []
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'}

    response = requests.get(url=url_,headers=header)

    if response.status_code == 200:
        response.encoding = 'gbk'
        print(f'{url_} 开始解析')
        soup = bs4.BeautifulSoup(response.text,'lxml')
        tag_list = soup.find_all(name='div', attrs={'class': 'list'})
        jpg = tag_list[0].ul.contents
        for i in jpg:
            href = i.a['href']
            url2 = 'http://www.netbian.com' + href
            jpg_urls.append(url2)
        for i in jpg_urls:
            if i.rsplit('.')[-1] != 'htm':
                jpg_urls.remove(i)
            else:
                pass
        img = []
        for i in jpg_urls:
            print(i)
            response = requests.get(url=i, headers=header)
            response.encoding = 'gbk'
            # print(response.text)
            soup = bs4.BeautifulSoup(response.text, 'lxml')
            # print(soup.find_all(name='div', attrs={'class': 'pic'}))
            url = soup.find_all(name='div', attrs={'class': 'pic'})[0].p.a.img['src']

            img.append(url)
            time.sleep(0.2)
        if img != 0:
            print('开始下载图片')
            print(img)
            print(len(img))
            for i in img:
                response = requests.get(i,headers=header)
                if response.status_code == 200:
                    with open(i.rsplit('/')[-1],'wb') as fp:
                        fp.write(response.content)
                    time.sleep(0.2)
                else:
                    time.sleep(0.1)
        print(f'{url_} 解析成功')
    else:
        print(f'{url_} 获取失败')





def get_time(main):
    def n():
        str = time.time()
        main()
        end = time.time()
        time_ = end - str
        print(f'所用时间为 {time_}')
    return n

@get_time
def main():

    url_list = get_url_list(2)
    print(url_list)
    threads = []
    for i in url_list:
        thread_ = threading.Thread(target=get_html,args=(i,))
        threads.append(thread_)
        thread_.start()
    [thread.join() for thread in threads]

if __name__ == '__main__':
    main()







