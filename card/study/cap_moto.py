#coding=UTF-8
import urllib
import urllib2
import Queue
import threading
import re
import HTMLParser
import chardet
from BeautifulSoup import BeautifulSoup





html_parser = HTMLParser.HTMLParser()

#seed_url = r'http://www.dmoz.org'
#root_url = r'http://www.wikipedia.org'
root_url = r'http://www.cheapcycleparts.com/oemparts/a/suz/50d3ab71f8700220d0b7222f/air-cleaner'
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
        html_1 = urllib2.urlopen(request,data=None, timeout=2).read()
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
    
    
def get_url_5(seed_url):
    global all_list
    url_list = []
    html =  pre_url(seed_url)
    
    #print html
    #return
    soup = BeautifulSoup(html)
    print "5555555555555555555555555555555555555555555555"
    #print html
    #tags1 = soup.findAll('ul', attrs = {'class':'partlistrow'})
    tags_partlist = soup.findAll('div',attrs = {'class':'partlistrow'})
    
    
    #print tags_partlist
    print len(tags_partlist)
    
    
    #tag_pic = soup.findAll('div',id = 'diagram')
    tag_pic = soup.findAll('div',attrs = {'class':'ammimg'})
    #print len(tag_pic)
    pattern = re.compile(r'src="([^"]*)"')
    pattern_1 = re.compile(r'http.*png')
    pattern_2 = re.compile(root_url)
    pattern_3 = re.compile(r'^/[^/]')
    pattern_4 = re.compile(r'^//')
    pattern_5 = re.compile(r'http.*%s'%root_url_key)

    for i in tags_partlist:
        #print i
        #print type(i)
        soup1 = BeautifulSoup(str(i))
        
        par_name = soup1.find('span',attrs = {'class':'ellipsis_text'})
        if par_name != None:
            print par_name.string
            
        part_item = soup1.find('span',attrs = {'class':'itemnum'})
        if part_item != None:
            print part_item.string
         
        part_dbl = soup1.find('span',attrs = {'class':'dbl'})
        if part_dbl != None:
            print part_dbl.string
           
        part_qty = soup1.find('input',type="text")
        if part_qty != None:
            print part_qty['value']
    for i in tag_pic:   

        
        result_all = pattern.findall(str(i))
        
        if result_all !=[]:
            #print result_all
            for j in result_all:
                print j
                #print "the j is~~~~~~~~~",j
                if pattern_1.search(j):
                    whole_url = j
                elif pattern_2.search(j):
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
    for i in url_list:
        local = "d:\\%s.png"%i[0].split('/')[-3]
        urllib.urlretrieve(i[0], local)
    
    #creat_shelf(seed_url,url_list)
    #print "current urllist size is:", len(url_list)
    #push_queue(url_list)
    #all_list.extend(url_list)
    #all_list = list(set(all_list))  
    





get_url_5(root_url)






