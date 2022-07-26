#coding:utf-8
import urllib.request
import urllib.parse
import re
from queue import Queue
from bs4 import BeautifulSoup
import concurrent.futures





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
             tu = re.finditer(pattern=r'<a href="(.+?)".+?<p class="name">(.+?)\s*</p>',string=response_text,flags=re.DOTALL)
             for i in tu:
                 queue.put((urllib.parse.urljoin(base=self.base_url, url=i.groups()[0]),i.groups()[1]),timeout=2)
        else:
            print(self.base_url+'     error!!!')



class DisplayDetails():
    """输出details到控制台"""
    def __init__(self):
        self.url_queue = Queue()
        # self.url = r'http://www.ultramanclub.com/allultraman/80/'


    def make_queue(self):
        UrlQueue().process_url(self.url_queue)


    def get_details(self,url):

        response_text=Request_(url = url).get()
        soup = BeautifulSoup(response_text,'lxml')
        altraheros_contents_details = soup.find_all(name='div',class_='ultraheros-Contents_Detail') #altraheros的详细介绍页面，有的altraheros有多个形态，对应多个详情页

        for tag in altraheros_contents_details:
            #introduction节点获取
            tag_string=tag.find_all(name='p',class_='introduction')[0].get_text()
            string_ = re.sub(pattern=r'\s*', repl='', string=tag_string)

            print(string_)   #控制台打印introduction
                
            for details in tag.find_all(name='tbody'):
                #详细介绍
                for tr_tag in details.find_all(name='tr'):
                    print((tr_tag.th.string,tr_tag.td.string.strip()))
                    # print(tr_tag.td.string)
        
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
            # executor.submit(fn=self.thread_)
            # executor.submit(fn=self.thread_)
            # executor.submit(fn=self.thread_)
        # self.make_queue()
        # self.thread_()



# if '__name__'=='__main__':
n = DisplayDetails()
n.main()
