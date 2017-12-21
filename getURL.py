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


home_page = get_content(url, my_headers)
home_soup = BeautifulSoup(home_page, 'lxml')
ul_lists = home_soup.find_all('ul')

video_flag = 0
videos = list()
pictures = list()
pat_vn = re.compile('(.+?)\s')
pat_pn = re.compile('(.+?)\[(.+?)\]')
pat_mp4 = re.compile('http(.+?)mp4')
update_v,update_p=open('./last_update.txt','r').read().split(',')
update_flag=0
for lists in ul_lists:
    video_flag=not video_flag
    if video_flag:
        if lists.a.next_sibling.string==update_v:
            continue
        else:
            update_v=lists.a.next_sibling.string
            for a in lists.find_all('a'):
                sub_page = get_content(url + a['href'], my_headers)
                if sub_page:
                    temp_name = pat_vn.search(a.string)
                    filename = temp_name.group(1) if temp_name else a.string[:4]
                    url_mp4 = pat_mp4.search(sub_page)
                    if url_mp4:
                        videos.append('filename=' + filename +
                                      '&fileurl=' + url_mp4.group(0))
        f_video=open('./video.downlist','w')
        f_video.write('\n'.join(videos))
        f_video.close()
    else:
        if lists.a.next_sibling.string==update_p:
            continue
        else:
            update_p=lists.a.next_sibling.string
            for a in lists.find_all('a'):
                sub_page = get_content(url + a['href'], my_headers)
                if sub_page:
                    sub_soup=BeautifulSoup(sub_page,'lxml')
                    temp_name = pat_pn.search(a.string)
                    filename = temp_name.group(1) if temp_name else a.string[:4]
                    div_tag=sub_soup.h1.parent
                    pic_count=0
                    for img in div_tag.find_all('img'):
                        pic_count=pic_count+1
                        pictures.append(img['src']+'\t'+filename+str(pic_count)+'.jpg')


f_pic=open('./pic.scp','w')
f_pic.write('\n'.join(pictures))
f_pic.close()
f_update=open('./last_update.txt','w')
f_update.write(update_v+','+update_p)
f_update.close()
        
        
	        

	        
	        
	        
	        
		
        
			
				
			
					
					
					
						
						
				
					
				
				
					
                
	        
	            
				
				
	
    
        
	            
				
					
                
				   
                	
                        
                        
                
            
    
