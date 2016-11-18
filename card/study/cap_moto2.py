#coding=UTF-8
import urllib
import urllib2
import Queue
import threading
import re
import HTMLParser
import chardet
from BeautifulSoup import BeautifulSoup

import shelve
from contextlib import closing


#import sys
#question_word = "����"

html_parser = HTMLParser.HTMLParser()

#seed_url = r'http://www.dmoz.org'
#root_url = r'http://www.wikipedia.org'
root_url = r'http://www.cheapcycleparts.com/'
root_url_key = root_url.split('.')[-2]
print root_url_key
UserAgent  = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36'
#root_url = "http://www.news.baidu.com/ns?cl=2&rn=20&tn=news&word=" + urllib.quote(question_word.decode(sys.stdin.encoding).encode('gbk'))

q = Queue.Queue()
q2 = Queue.Queue()
all_list = [root_url]

def write_to_txt(str_text):
    tmp_file = open('cap_moto.txt','a')
    tmp_file.write(str_text)
    tmp_file.close
    
def pre_url(seed_url):
    
    
    
    #test = urllib.urlopen(seed_url)
    #html = test.read()
    
    
    request  = urllib2.Request(seed_url)
    request.add_header('Accept', "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp")
    request.add_header('Accept-Encoding', "*")
    request.add_header('User-Agent', UserAgent)
    try:
        html_1 = urllib2.urlopen(request).read()
    except Exception,ex:
        print Exception,':',ex
        return
    encoding_dict = chardet.detect(html_1)
    #print encoding
    web_encoding = encoding_dict['encoding']
    print "encoding ~~~~~~~~",web_encoding
    if web_encoding == 'utf-8' or web_encoding == 'UTF-8':
        
        html = html_1
    else :
        html = html_1.decode('gbk','ignore').encode('utf-8')
    return html
    #test.close()
    
    
def get_url(seed_url):
    global all_list
    url_list = []
    html =  pre_url(seed_url)
    soup = BeautifulSoup(html)
    [x.extract() for x in soup.findAll('script')] 
    #soup_text = BeautifulSoup(html,"lxml")
    #print soup
    tags1 = soup.findAll('ul',id="slider")
    print tags1
    #return
    
    #_text = soup.findAll('div', id="bodyContent")
    #_text = soup.findAll('div', attrs = {'class':'field-items'})
    #_text = soup.findAll('td', attrs = {'class':'t_f'})
    _text = soup.findAll('p')
    #print soup_text.get_text()
    #print len(_text)
    
    """
    if _text != []:
        #text_len = 0
        #for i in _text:
        #    print i.text.encode('utf8')
        text_all = "\n\r".join([i.text for i in _text])
        text_all = html_parser.unescape(text_all)
        pattern_no_html = re.compile(r'<[^>]+>')
        chinese_txt2 = ur".*?发表于.*\d:\d\d|.*编辑|http.*html"
        pattern_no_some = re.compile(chinese_txt2)
        text_all = pattern_no_html.sub('',text_all)
        text_all = pattern_no_some.sub('\n',text_all)
        print "current text_all size is:", len(text_all)
        if len(text_all)>1000:
            
            #print text_all
            write_to_txt(text_all)
            #print "~~~~~~~~~~~~~~~~~~~~~~~the len of text_all is ",len(text_all)
    """
            
    #tags2 = soup.findAll('a', {'target':  '_blank'}) 
    #tags3 = soup.findAll('tr', {'class':  'bg'}) 
    pattern = re.compile(r'href="([^"]*)"')
    pattern_2 = re.compile(root_url)
    #pattern_2 = re.compile(r'^http')
    pattern_3 = re.compile(r'^/[^/]')
    pattern_4 = re.compile(r'^//')
    pattern_5 = re.compile(r'http.*%s'%root_url_key)
    for i in tags1:
        #print i
        result_all = pattern.findall(str(i))
        if result_all !=[]:
            for j in result_all:
                #print "the j is~~~~~~~~~",j
                if pattern_2.search(j):
                    #print "!!!!!!!!!!!!!!"
                    #print j
                    #print "~!!!!!!!!!!!!!!!!"
                    whole_url = j
                elif pattern_3.search(j):
                    whole_url =   root_url +j
                    #print whole_url
                elif pattern_4.search(j):
                    whole_url =   "http:" +j
                    #print whole_url
                elif pattern_5.search(j):
                    #print "~~~~~~~~~~~~~~~~"
                    #print j
                    whole_url = j
                    #print "~~~~~~~~~~~~~~~~"
                    
                    #whole_url =   root_url + j
                else:
                    continue
                url_list.append((whole_url,1))
                url_list = list(set(url_list))
                #url_list1 = list({(i,1) for i in url_list})
                
    print url_list
    creat_shelf(seed_url,url_list)
    #return
    #print "current urllist size is:", len(url_list)
    push_queue(url_list)
    all_list.extend(url_list)
    all_list = list(set(all_list))
    #print "all list size is:", len(all_list)
    #return url_list

def get_url_2(seed_url):
    global all_list
    url_list = []
    html =  pre_url(seed_url)
    #print html
    soup = BeautifulSoup(html)

    tags1 = soup.findAll('div', attrs = {'class':'fiche_link'})
    print tags1
    
    pattern = re.compile(r'href="([^"]*)"')
    pattern_2 = re.compile(root_url)
    #pattern_2 = re.compile(r'^http')
    pattern_3 = re.compile(r'^/[^/]')
    pattern_4 = re.compile(r'^//')
    pattern_5 = re.compile(r'http.*%s'%root_url_key)
    for i in tags1:
        #print i
        result_all = pattern.findall(str(i))
        if result_all !=[]:
            for j in result_all:
                #print "the j is~~~~~~~~~",j
                if pattern_2.search(j):
                    #print "!!!!!!!!!!!!!!"
                    #print j
                    #print "~!!!!!!!!!!!!!!!!"
                    whole_url = j
                elif pattern_3.search(j):
                    whole_url =   root_url +j
                    #print whole_url
                elif pattern_4.search(j):
                    whole_url =   "http:" +j
                    #print whole_url
                elif pattern_5.search(j):
                    #print "~~~~~~~~~~~~~~~~"
                    #print j
                    whole_url = j
                    #print "~~~~~~~~~~~~~~~~"
                    
                    #whole_url =   root_url + j
                else:
                    continue
                url_list.append((whole_url,2))
                url_list = list(set(url_list))
                #url_list1 = list({(i,1) for i in url_list})
                
    print url_list
    creat_shelf(seed_url,url_list)
    #print "current urllist size is:", len(url_list)
    push_queue(url_list)
    all_list.extend(url_list)
    all_list = list(set(all_list))    



def get_url_3(seed_url):
    global all_list
    url_list = []
    html =  pre_url(seed_url)
    #print html
    soup = BeautifulSoup(html)
    print "oooooooooooo0000000000000000000000000000000000oooooo",html
    tags1 = soup.findAll('ul', attrs = {'class':'partsubselect'})
    print tags1
    
    pattern = re.compile(r'href="([^"]*)"')
    pattern_2 = re.compile(root_url)
    #pattern_2 = re.compile(r'^http')
    pattern_3 = re.compile(r'^/[^/]')
    pattern_4 = re.compile(r'^//')
    pattern_5 = re.compile(r'http.*%s'%root_url_key)
    for i in tags1:
        #print i
        result_all = pattern.findall(str(i))
        if result_all !=[]:
            for j in result_all:
                #print "the j is~~~~~~~~~",j
                if pattern_2.search(j):
                    #print "!!!!!!!!!!!!!!"
                    #print j
                    #print "~!!!!!!!!!!!!!!!!"
                    whole_url = j
                elif pattern_3.search(j):
                    whole_url =   root_url +j
                    #print whole_url
                elif pattern_4.search(j):
                    whole_url =   "http:" +j
                    #print whole_url
                elif pattern_5.search(j):
                    #print "~~~~~~~~~~~~~~~~"
                    #print j
                    whole_url = j
                    #print "~~~~~~~~~~~~~~~~"
                    
                    #whole_url =   root_url + j
                else:
                    continue
                url_list.append((whole_url,3))
                url_list = list(set(url_list))
                #url_list1 = list({(i,1) for i in url_list})
                
    print url_list
    creat_shelf(seed_url,url_list)
    #print "current urllist size is:", len(url_list)
    push_queue(url_list)
    all_list.extend(url_list)
    all_list = list(set(all_list))  


def get_url_4(seed_url):
    global all_list
    url_list = []
    html =  pre_url(seed_url)
    soup = BeautifulSoup(html)
    tags1 = soup.findAll('ul', attrs = {'class':'partsubselect'})
    print tags1
    
    pattern = re.compile(r'href="([^"]*)"')
    pattern_2 = re.compile(root_url)
    #pattern_2 = re.compile(r'^http')
    pattern_3 = re.compile(r'^/[^/]')
    pattern_4 = re.compile(r'^//')
    pattern_5 = re.compile(r'http.*%s'%root_url_key)
    for i in tags1:
        #print i
        result_all = pattern.findall(str(i))
        if result_all !=[]:
            for j in result_all:
                #print "the j is~~~~~~~~~",j
                if pattern_2.search(j):
                    #print "!!!!!!!!!!!!!!"
                    #print j
                    #print "~!!!!!!!!!!!!!!!!"
                    whole_url = j
                elif pattern_3.search(j):
                    whole_url =   root_url +j
                    #print whole_url
                elif pattern_4.search(j):
                    whole_url =   "http:" +j
                    #print whole_url
                elif pattern_5.search(j):
                    #print "~~~~~~~~~~~~~~~~"
                    #print j
                    whole_url = j
                    #print "~~~~~~~~~~~~~~~~"
                    
                    #whole_url =   root_url + j
                else:
                    continue
                url_list.append((whole_url,4))
                url_list = list(set(url_list))
                #url_list1 = list({(i,1) for i in url_list})
                
    print url_list
    creat_shelf(seed_url,url_list)
    #print "current urllist size is:", len(url_list)
    push_queue(url_list)
    all_list.extend(url_list)
    all_list = list(set(all_list))  


def get_url_5(seed_url):
    global all_list
    url_list = []
    html =  pre_url(seed_url)
    soup = BeautifulSoup(html)
    print "5555555555555555555555555555555555555555555555"
    #print html
    tags1 = soup.findAll('ul', attrs = {'class':'partlistrow'})
    print tags1
    tag_pic = soup.findAll('div',id = 'diagram')
    print tag_pic
    
    pattern = re.compile(r'src="([^"]*)"')
    pattern_2 = re.compile(root_url)
    pattern_3 = re.compile(r'^/[^/]')
    pattern_4 = re.compile(r'^//')
    pattern_5 = re.compile(r'http.*%s'%root_url_key)
    for i in tags1:
        result_all = pattern.findall(str(i))
        if result_all !=[]:
            for j in result_all:
                #print "the j is~~~~~~~~~",j
                if pattern_2.search(j):
                    #print "!!!!!!!!!!!!!!"
                    #print j
                    #print "~!!!!!!!!!!!!!!!!"
                    whole_url = j
                elif pattern_3.search(j):
                    whole_url =   root_url +j
                    #print whole_url
                elif pattern_4.search(j):
                    whole_url =   "http:" +j
                    #print whole_url
                elif pattern_5.search(j):
                    #print "~~~~~~~~~~~~~~~~"
                    #print j
                    whole_url = j
                    #print "~~~~~~~~~~~~~~~~"
                    
                    #whole_url =   root_url + j
                else:
                    continue
                url_list.append((whole_url,5))
                url_list = list(set(url_list))
                #url_list1 = list({(i,1) for i in url_list})
                
    print url_list
    
    creat_shelf(seed_url,url_list)
    #print "current urllist size is:", len(url_list)
    #push_queue(url_list)
    #all_list.extend(url_list)
    #all_list = list(set(all_list))  
    


def creat_shelf(key,value):
    with closing(shelve.open('test_shelf.db')) as s:
        s[key]=value
def print_shelf():
    with closing(shelve.open('test_shelf.db')) as s:
        print [a for a in s]
        print [s[a] for a in s]

def push_queue(url_list):
    for i in url_list:
        if i not in all_list:
            q.put(i)
            
             
def work_process():
    while 1:
        next_url = q.get()
        print "the q next url is: ", next_url[0]
        print "the q next url id: ", next_url[1]
        print "queue number is:", q.qsize()
        q.task_done()
        if next_url[1] == 1:
            get_url_2(next_url[0])
            print "1111111111111111111"
        elif next_url[1] == 2:
            get_url_3(next_url[0])
            print "222222222222222222222"
        elif next_url[1] == 3:
            get_url_4(next_url[0])
            print "3333333333333333"
        elif next_url[1] == 4:
            get_url_5(next_url[0])
            print "44444444444444444"
        elif next_url[1] == 5:
            #get_url_5(next_url[0])
            print "the last~~~~~~~~"
            
#print_shelf()
 

get_url(root_url)
thread_list = [threading.Thread(target = work_process),
                    threading.Thread(target = work_process), 
                    threading.Thread(target = work_process), 
                    threading.Thread(target = work_process), 
                    threading.Thread(target = work_process), 
                    threading.Thread(target = work_process), 
                    threading.Thread(target = work_process), 
                    threading.Thread(target = work_process), 
                    threading.Thread(target = work_process)]
#new_thread = threading.Thread(target = get_url, args=(next_url,))
for i in thread_list:
    i.setDaemon(True)
    i.start()
   # i.join()



q.join()
