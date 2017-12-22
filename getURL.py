# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 11:49:06 2017

@author: FAGE
"""

import urllib2
import random
from bs4 import BeautifulSoup
import re
# encoding=utf8  

import sys  

reload(sys)  

sys.setdefaultencoding('utf8') 

url = "https://3344rq.com/"

my_headers = ["Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
              "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
              "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0"
              "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
              "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"

              ]


def get_content(url, headers):
    ''''' 
    @获取403禁止访问的网页 
    '''
    randdom_header = random.choice(headers)

    req = urllib2.Request(url)
    req.add_header("User-Agent", randdom_header)
    try:
    	content = urllib2.urlopen(req, timeout=3).read(10000000)
    except :
    	content=None
    return content

class Media:
    num=0
    updated=0
    def __init__(self,name=None):
        self.lists=[]
        Media.num+=1
        self.num=Media.num
        if name:
            self.filename=name
        else:
            self.filename=str(Media.num)+'.scp'
    def save(self):
        f=open('./'+self.filename,'w')
        f.write('\n'.join(self.lists))
        f.close()
        
        
        
        
        
home_page = get_content(url, my_headers)
home_soup = BeautifulSoup(home_page, 'lxml')
media=home_soup.find_all('h2')

video=Media('video.downlist')
pic=Media('pic.scp')

#检查更新
video.last_update,pic.last_update=open('./last_update.txt','r').read().split(',')
video.new_update=media[0].find_next('li').span.string
pic.new_update=media[1].find_next('li').span.string
if video.last_update!=video.new_update : video.updated=1
if pic.last_update!= pic.new_update: pic.updated=1

#保存更新
f_update=open('./last_update.txt','w')
f_update.write(video.new_update+','+pic.new_update)
f_update.close()

#定义资源匹配模板
video.pat_name = re.compile('(.+?)\s')
pic.pat_name = re.compile('(.+?)\[(.+?)\]')
pic.pat = re.compile('http(.+?)mp4')

#将更新的video提取出来
if video.updated:
    ul=media[0].find_next('ul')
    for a in ul.find_all('a'):
        if a.find_next('span').string==video.last_update: 
            video.save()
            break
        sub_page = get_content(url + a['href'], my_headers)
        if sub_page:
            temp_name = video.pat_name.search(a.string)
            filename = temp_name.group(1) if temp_name else a.string[:4]
            url_mp4 = pic.pat.search(sub_page)
            if url_mp4:
                video.lists.append('filename=' + filename +
                              '&fileurl=' + url_mp4.group(0))
    video.save()

#将更新的picture提取出来    
if pic.updated:
    ul=media[1].find_next('ul')
    for a in ul.find_all('a'):
        if a.next_sibling.string==pic.last_update: 
            pic.save()
            break
        sub_page = get_content(url + a['href'], my_headers)
        if sub_page:
            sub_soup=BeautifulSoup(sub_page,'lxml')
            temp_name = pic.pat_name.search(a.string)
            filename = temp_name.group(1) if temp_name else a.string[:4]
            div_tag=sub_soup.h1.parent
            pic_count=0
            for img in div_tag.find_all('img'):
                pic_count=pic_count+1
                pic.lists.append(img['src']+'\t'+filename+str(pic_count)+'.jpg')
    pic.save()
            


    

        
        
	        

	        
	        
	        
	        
		
        
			
				
			
					
					
					
						
						
				
					
				
				
					
                
	        
	            
				
				
	
    
        
	            
				
					
                
				   
                	
                        
                        
                
            
    
