#coding:utf-8 
# import MySQLdb
import urllib2
import string
import sys, getopt
import os
import random
import time
import thread 
import re
import gzip
import StringIO
import json
import ConfigParser
import time
import random
import copy
import socket
import threading
import codecs
import mechanize
import cookielib
import datetime
import datetime,time



reload(sys)
sys.setdefaultencoding('utf-8')

proxys = []
user_agent_list = [\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"\
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",\
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",\
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",\
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",\
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",\
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",\
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER) ",\
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",\
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E) ",\
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400) ",\
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E) ",\
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",\
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E) ",\
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E) ",\
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",\
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E) ",\
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E) ",\
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E) ",\
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",\
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0) " ,\
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:16.0) Gecko/20121026 Firefox/16.0",\
        "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",\
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",\
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",\
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",\
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",\
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)",\
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",\
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",\
        "Mozilla/5.0 (Linux; U; Android 2.2.1; zh-cn; HTC_Wildfire_A3333 Build/FRG83D) AppleWebKit/533.1 (KHTML,  like Gecko) Version/4.0 Mobile Safari/533.1"\
       ]
 






 
def get_total_raw_data(code,y):
    global proxys
    global fname
    global lock
    global now_c 
    
    # lock.acquire()
    
    if code =="":
        lock.acquire()
        now_c=now_c -1
        lock.release() 
        return
    tmp = code
    good=0
    url2 = "http://data.eastmoney.com/zjlx/"+tmp+".html"
    url3 = "http://data.eastmoney.com/zjlx/graph/his_"+tmp+".html"
    br = mechanize.Browser()
    # Cookie Jar
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
    # Browser options
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    html = ""
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    i=1
    while 1:
        try:
            ua2 = random.choice(proxys)
            br.set_proxies({"http": ua2}) 
            xc =random.uniform(1, 8)
            # if xc>=7:
                # r = br.open(url2, timeout=8)
            r = br.open(url3, timeout=8)
            html = r.read()
            break
        except Exception,e:
            print code ,"get his failed!",e,code
            time.sleep(random.uniform(0.5, 1))
            i = i + 1
            if i>15:
                break
                
                
    if -1==html.find("DataCenter"):
        print code,good,"--++--"  
        lock.acquire()
        now_c=now_c -1
        lock.release() 
        return 0
    try:
        tmp2 = html.split("\r\n")[2:]
        tmp2.reverse()
        ii=1
        total2=0.0
        for cc in tmp2:
            if cc!="":
                t = cc.split(";")
                tt = int(float(t[1]))
                if tt>0 and ii<=6:
                    good=good+1
                if ii<=12:
                   total2=total2+abs(tt)
                ii=ii+1
                if ii>12:
                   break
        ch = total2/ii
        
        if good<3:
            lock.acquire()
            now_c=now_c -1
            lock.release() 
            return 0
            
        sig=0
        i=1
        total=0
        all_vol=[]
        for src in tmp2:
            t = src.split(";")
            try:
                xr=float(t[1])
            except Exception,e:
                # print e,xr
                continue
            all_vol.append(xr)
            total=total+xr
            # if xr>0 and i<=7:
               # good =good+1
            # print "ch*1.5,good,total",ch*1.5,good,total
            if i>1:
                if ch*1.5>total:
                    i=i+1
                    continue
                if total>800.0:
                    if sig<1:
                        sig=1
                if total>3500.0:
                    if sig<2:
                        sig=2
                if total>8000.0:
                    if sig<3:
                        sig=3
                if total>12000.0:
                    if sig<4:
                        sig=4
            i=i+1
            if i>15:
                break
        all_vol.sort()
        if abs(all_vol[0])>all_vol[-1] and all_vol[0]<0 and sig>1:   
            sig==1       
        if good>=4:
            sig==5        
        lock.acquire()    
        tt=""
        if sig==1 or sig==2:
            tt="3"
        if sig==3:
            tt="2"
        if sig==4:
            tt="1"
        if sig==5:
            tt="0"
          
        if tt!="":
            # print tt,"lllllllllllll" 
            open(fname,"a").write(tt+code+"\n")
            now_c=now_c -1
            lock.release() 
            return
        now_c=now_c -1
        lock.release() 
        thread.exit_thread()
    except Exception,e:
        print code ,"anly his failed!",e
        lock.acquire()  
        now_c=now_c -1
        lock.release() 
        thread.exit_thread()
        

    
def update_data(line,i):
    global now_c
    global lock
    global lock2
    lock.acquire()
    now_c=now_c +1
    lock.release() 
    this_year = time.strftime('%Y',time.localtime(time.time())) +"b"
    conn=MySQLdb.connect(host='localhost',user='root',passwd='root',port=3306);
    conn.select_db(this_year);
    cur=conn.cursor(); 
    it=0
    while 1:
        try:
            data = get_total_raw_data(line)
            if len(data) <=0 and it>2:
                open("log_update.txt","a").write(line+"\n") 
                time.sleep(random.uniform(5, 10))
                break
            # data=data.replace(";","~")
            # tmp = data.split("\r\n")[2:]  
            tmp = data[0:4]
            for cc in tmp:
                cc=cc.strip()
                if cc=="":
                    break
                print "insert: ",cc,line
                pp=0
                if -1!=cc.find("<") or -1!=cc.find("<") or -1!=cc.find("/") or len(cc)<15:
                    x=15/pp
                count=cur.execute('select * from stocks where data=%s',cc)
                # if count>0:
                    # continue
                tmp_c =0 
                while count<=0:
                    cur.execute('insert into stocks(code,data) values(%s,%s)',[line,cc]);
                    conn.commit()
                    tmp_c =tmp_c+1
                    time.sleep(random.uniform(0.5, 1))
                    count=cur.execute('select * from stocks where data=%s',cc)
                    if tmp_c>3:
                        break
            count = 0
            break
        except Exception,e:
            print "damn!something wrong!!1" ,e,sys.exc_info()[0],sys.exc_info()[2].tb_lineno,"    ",it
            # this_year = time.strftime('%Y',time.localtime(time.time())) 
            cur.close()
            conn.close()
            conn=MySQLdb.connect(host='localhost',user='root',passwd='root',port=3306);
            conn.select_db(this_year);
            cur=conn.cursor();
            it=it+1
    lock.acquire()
    now_c=now_c -1
    lock.release() 
    lock2.acquire()
    open("progress_update.txt","a").write(line+"\n")
    lock2.release() 
    cur.close()
    conn.close()
    thread.exit_thread()
    print "finished!",i     
    
    
    


th_count=20
lock = thread.allocate_lock()
# lock2 = thread.allocate_lock()
fnamet = time.strftime('%Y-%m-%d',time.localtime(time.time()))
fname2 ="10jqka_eql"+fnamet+".txt"
fname =fname2+"_buy_vol_plus.txt"

print fname2
if (os.path.isfile(fname)):
    os.remove(fname)

for line in open('proxy.txt','r'):
    line = line.strip()
    if line!="":
        proxys.append(line) 

now_c=0
i=0
for line in open(fname2,'r'):#fname2
    line = line.strip()
    if line =="":
        continue
    while now_c>th_count:
        print "++++++++++th_count",now_c,th_count,i
        time.sleep(random.uniform(10, 15))
    i = i +1
    lock.acquire()
    now_c=now_c +1
    lock.release() 
    thread.start_new_thread(get_total_raw_data,(line[0:6],i))
    # time.sleep(random.uniform(10, 15))

while now_c>0:
    print "wait all done",now_c
    time.sleep(random.uniform(2, 5)) 
    
total_result  = []   
stock_name = []
for line in open("info.txt",'r'):
        line = line.strip()
        stock_name.append(line)  
        
for line in open(fname,'r'):
        line = line.strip()

        total_result.append(line)
total_result.sort()  
if (os.path.isfile(fname)):
    os.remove(fname)  

for t in total_result:
    for name in stock_name:
        
        if name[0:6]==t[1:]:
            tmp = name.split(",")
            open(fname,"a").write(name+"__"+t[0:1]+"\n")  
            break  


