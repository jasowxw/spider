# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import re
from bs4 import BeautifulSoup
from queue import Queue
import concurrent.futures
from pymongo import MongoClient

class Request_():
    """一个用于请求的类"""
    def __init__(self,url):
        self.url =url 
    def get(self):
        response = urllib.request.urlopen(url=self.url)
        if response.status==200:
            print(response.url+'      ok')
            return response.read().decode('gbk')
        else:
            return None

class UrlQueue():
    """一个用于构造urlqueue的类"""
    def __init__(self):
        self.base_url=r'http://www.ultramanclub.com/allultraman/'  #爬取的URL，从中找出全部奥特曼的详情页url
    def process_url(self,queue):
        """处理url，并把组合好的URL放入队列中"""
        response_text = Request_(url=self.base_url).get()
        if response_text:
             soup = BeautifulSoup(response_text,"lxml")
             ultraheros_Content= soup.find_all(name='div',class_="ultraheros-Contents_Lists")
             ultranheros_lists = ultraheros_Content[0].find_all(name="ul",class_='lists')
            #  print(len(ultranheros_lists))

             for i in ultranheros_lists[0].find_all(name='li',class_='item'):
                #('http://www.ultramanclub.com/allultraman/ultraman/', '奥特曼') 以这种形式放入队列
                queue.put((urllib.parse.urljoin(base=self.base_url, url=i.a['href']),i.a.p.string.strip()),timeout=2)
                
        else:
            print(self.base_url+'     error!!!')
        # for i in ultranheros_lists:
        #     # print(len(i))
        #     print(i)
        #     print('-'*10)


class DisplayDetails():
    """输出details到控制台"""
    def __init__(self):
        self.url_queue = Queue()
        self.collections=MongoClient().altraheros.a1
        # self.url = r'http://www.ultramanclub.com/allultraman/80/'


    def make_queue(self):
        UrlQueue().process_url(self.url_queue)


    def get_details(self,url):

        response_text=Request_(url = url).get()
        soup = BeautifulSoup(response_text,'lxml')
        altraheros_contents_details = soup.find_all(name='div',class_='ultraheros-Contents_Detail') #altraheros的详细介绍页面，有的altraheros有多个形态，对应多个详情页

        details_dict = {'name':url.split('/')[4],'details':[]}
        for tag in altraheros_contents_details:
            dict_ = {} #用来存续详细的信息，以后放入上边的details中
            #introduction节点获取
            tag_string=tag.find_all(name='p',class_='introduction')[0].get_text()
            string_ = re.sub(pattern=r'\s*', repl='', string=tag_string)
            dict_['introduction']=string_   #介绍信息

            for details in tag.find_all(name='tbody'):
                #详细介绍
                for tr_tag in details.find_all(name='tr'):
                    dict_[tr_tag.th.get_text()]=tr_tag.td.get_text().strip()    #详细信息，包括姓名，高度，重量。。。。。。
            details_dict['details'].append(dict_)
        self.collections.insert_one(details_dict)
    def thread_(self):
        while True:
            try:
                hero_url = self.url_queue.get(timeout=3)
                self.get_details(url=hero_url[0])
                # print(hero_url)

            except:
                if self.url_queue.empty():
                    print('queue empty!')
                    break
        

    
    def main(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            executor.submit(fn=self.make_queue)
            executor.submit(fn=self.thread_)
            # executor.submit(fn=self.thread_)
            # executor.submit(fn=self.thread_)
        # self.make_queue()
        # self.thread_()


if __name__=="__main__":  
    n = DisplayDetails()
    n.main()
