#coding:utf-8 
import MySQLdb
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

       
#获取一只股票的K线数据
def get_full_data(code):
       global this_year
       total_data=[]
       year = int(this_year)
       ii=0
       try:
           while 1:
               s = get_stock_data_year(code,str(year))
               pos_start = s.find('data":"')
               s = s[pos_start+len('data":"'):]
               if s=="w" or s=="" or type(s)!=str:
                  break
               total_data =  s.split(";") +total_data
               year = year -1
           return total_data
       except Exception,e:
            print 'wrong! try: ', e,sys.exc_info()[2].tb_lineno
       return []
    
#获取单年的股票K线数据
def get_stock_data_year(code,this_year):
        wrong = 0
        url = r"http://d.10jqka.com.cn/v2/line/hs_" + code + r"/01/" + this_year + ".js"
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
        ua = random.choice(user_agent_list)
        br.addheaders = [('User-agent', ua)]
        html = ""
        while True:
                  try:
                            ua3 = random.choice(proxys)
                            br.set_proxies({"http": ua3}) 
                            wrong = wrong +1
                            if wrong >15:
                                return "w"
                            r = br.open(url, timeout=8)
                            html = r.read()
                            if type(html)!=str:
                                html = ""
                                continue
                            if len(html)<50 :
                                continue
                            break
                  except Exception,e:
                            print 'someting wrong! try: ', e,sys.exc_info()[2].tb_lineno,wrong 
                            if wrong >15:
                                return "w"

        pos = html.find(':')
        html = html[pos+1:len(html)-3]
        return html
        
    
def update_data(line,i):
    global now_c
    global lock
    global lock2
    lock.acquire()
    now_c=now_c +1
    lock.release() 
    this_year = time.strftime('%Y',time.localtime(time.time())) 
    conn=MySQLdb.connect(host='localhost',user='root',passwd='',port=3306);
    conn.select_db("stock");
    cur=conn.cursor(); 
    it=0
    while 1:
        try:
            #data = ["20150105,14.54,14.99,14.30,14.83,9047240,204847850.00,2.906","20150106,14.80,15.68,14.67,15.49,12682564,298067620.00,4.074","20150107,15.59,15.67,15.27,15.39,8602877,205040230.00,2.763","20150108,15.39,15.59,15.06,15.28,7247779,171583590.00,2.328","20150109,15.17,15.71,15.09,15.28,10831207,258771820.00,3.479"]
            data = get_full_data(line)
            print "let us start!!!!!!"
            if(len(data)<=30):
                break
            for cc in data:
                cc=cc.strip()
                if cc=="":
                    break
                data_tamp = cc.split(',')
                if(len(data_tamp)>=8):
                    if(line[0]=='0'):
                        cur.execute('insert into shenzhen1(code,date,start_pricec,high_price,low_price,end_price,volume1,volume2,unkown_num) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)',(line,data_tamp[0],data_tamp[1],data_tamp[2],data_tamp[3],data_tamp[4],data_tamp[5],data_tamp[6],data_tamp[7]));
                        conn.commit()
                    else:
                        cur.execute('insert into shanghai1(code,date,start_pricec,high_price,low_price,end_price,volume1,volume2,unkown_num) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)',(line,data_tamp[0],data_tamp[1],data_tamp[2],data_tamp[3],data_tamp[4],data_tamp[5],data_tamp[6],data_tamp[7]));
                        conn.commit()
            break
        except Exception,e:
            print "damn!something wrong!!1" ,e,sys.exc_info()[0],sys.exc_info()[2].tb_lineno,"    ",it
            cur.close()
            conn.close()
            conn=MySQLdb.connect(host='localhost',user='root',passwd='',port=3306);
            conn.select_db("stock");
            cur=conn.cursor();
            it=it+1
    lock.acquire()
    now_c=now_c -1
    open("progress_update.txt","a").write(line+"\n")
    lock.release() 
    cur.close()
    conn.close()
    thread.exit_thread()
    print "finished!",i 
    
    
    
if (os.path.isfile("log_update.txt")):
    os.remove("log_update.txt")  
th_count=30
lock = thread.allocate_lock()
sig="0" 
now_code=""

this_year = time.strftime('%Y',time.localtime(time.time())) 
if now_code!="":
    sig="1"
for line in open('proxy.txt','r'):
    line = line.strip()
    if line!="":
        proxys.append(line) 

now_c=0
for line in open('code.txt','r'):
    line = line.strip()
    if line =="":
        continue
    if -1!=now_code.find(line):
        continue
    thread.start_new_thread (update_data,(line,now_c))
    if now_c>th_count:
        print "++++++++++th_count",th_count,now_c
        time.sleep(random.uniform(20, 25))


