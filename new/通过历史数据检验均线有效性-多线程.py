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
                            r = br.open(url, timeout=15)
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
      

#获取均线值
def get_percent_eq(date,num,ch):
    total_data=date
    n=num
    eq = 0.0
    start1 = 0.0
    l = total_data[ch-1].split(",")
    # start1 = l[1]
    stop = l[4]
    l = total_data[ch-num-1].split(",")
    start = l[1]   
    #print float(start1),start
    n=0
    # print total_data
    try:
        if float(start)-0.0>=0.01:
            price_up_down = (float(stop)-float(start))/float(start)
        else:
            price_up_down = 0.0 
            
        while 1:
            ll = total_data[ch-n-1].split(",")
            start = ll[4]  
            # print start
            eq = eq + float(start)
            n=n+1
            if n>=num:
                break  

    except Exception,e:
        if exp_sig==1:
            print "dame get eql failed"
        return 0.0,10
    return eq/num,price_up_down 


    
def update_data(line,i):
    global now_c
    global lock
    global lock2
    lock.acquire()
    now_c=now_c +1
    lock.release() 
    
    it=0
    max_result = (0,0,0.0)   #短周期，长周期，回测结果
    while 1:
        try:
            #data = ["20150105,14.54,14.99,14.30,14.83,9047240,204847850.00,2.906","20150106,14.80,15.68,14.67,15.49,12682564,298067620.00,4.074","20150107,15.59,15.67,15.27,15.39,8602877,205040230.00,2.763","20150108,15.39,15.59,15.06,15.28,7247779,171583590.00,2.328","20150109,15.17,15.71,15.09,15.28,10831207,258771820.00,3.479"]
            data = get_full_data(line)
            print "let us start!!!!!!  check: ",line
            too_len = len(data)
            if(too_len<=80):
                break
            start_i = 10
            end_i = 60
            mini_step = 3      #两条均线周期最小差
            while start_i<=30:
                start_i_tmp = 0
                start_i_tmp = start_i + mini_step
                while start_i_tmp<=end_i:
                    temp_result = get_check_result(data,start_i,start_i_tmp,too_len)
                    if max_result[2]==0.0:                      #首次更新
                        max_result[2]=temp_result
                        max_result[0]=start_i
                        max_result[1]=start_i_tmp
                        start_i_tmp = start_i_tmp + 1
                        continue
                    if temp_result>max_result[2]:
                        max_result[2]=temp_result
                        max_result[0]=start_i
                        max_result[1]=start_i_tmp
                    start_i_tmp = start_i_tmp + 1
                start_i = start_i + 1
            break
        except Exception,e:
            print "damn!something wrong!!1" ,e,sys.exc_info()[0],sys.exc_info()[2].tb_lineno,"    ",it
            it=it+1
            if it>10:
                break    
    lock.acquire()
    now_c=now_c -1
    open("total_eql_check_result.txt","a").write(line+" :"+str(max_result[0])+","+str(max_result[1])+","+str(max_result[2])+"\n")
    lock.release() 
    thread.exit_thread()
    print "finished!",i 
    
    
#检验一个均线组合的回测结果    
def get_check_result(data,num_short,num_long,total_len):   #参数说明，所有样本数据，短均线周期，长均线周期，样本数据总长度
    y = 40
    start_price = 0.0
    end_price = 0.0
    in_or_out = 0
    total_earn = 0.0
    lowest_price=0.0
    highest_price=0.0
    while y<total_len:
        vol_1,per_1 = get_percent_eq(data,num_short,y)     #NUM,0几天的均线，往后跳几天
        vol_2,per_2 = get_percent_eq(data,num_long,y) 
        if vol_1!=0.0 and vol_2!=0.0 and vol_1>vol_2 and in_or_out == 0:   #还没有买入，短均线上穿长均线，没有出错
            highest_price = get_highest_price(data,y)
            if(highest_price==0.0):
                y = y +1
                continue
            start_price = highest_price             #保存一次完整交易的买入价格
            end_price = 0.0
            in_or_out = 1
        if vol_1!=0.0 and vol_2!=0.0 and vol_1<=vol_2 and in_or_out == 1:   #还没有卖出，短均线下穿长均线，没有出错
            highest_price = get_lowest_price(data,y)
            if(lowest_price==0.0):
                y = y +1
                continue
            end_price = lowest_price       #保存一次完整交易的卖出价格
            in_or_out = 0
            temp_earn = (end_price-start_price)/start_price
            total_earn = total_earn + temp_earn                #完成一个购买周期
        y = y +1
    return  total_earn  
    
        
#获取下一个交易日的最高价        
def get_highest_price(data,y):
    l = data[y].split(",") 
    try:
        highest_price = float(l[2])  
    except Exception,e:
        return 0.0;
    return highest_price
   
#获取下一个交易日的最低价        
def get_lowest_price(data,y):
    l = data[y].split(",") 
    try:
        lowest_price = float(l[3])  
    except Exception,e:
        return 0.0;
    return lowest_price  
    
    
    
if (os.path.isfile("log_update.txt")):
    os.remove("log_update.txt")  
th_count=1
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


