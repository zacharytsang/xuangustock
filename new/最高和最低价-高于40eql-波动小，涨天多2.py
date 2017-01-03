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

#原理：从30个交易日往前找，可以设定一个范围，比如30个交易日到50个交易日。找到一个波浪的底部，然后从这个底部计算一浪高于一浪。且最后一个浪底和最近一个交易日的
#收盘价必须在40日均线之上。
exp_sig =1
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
 
#获取多少天的股票K线数据
def get_full_data(code , num):
       global this_year
       total_data=[]
       year = int(this_year)
       ii=0
       try:
           while 1:
               s = get_stock_data2(code,str(year))
               # print "================",str(year)
               if s=="w" or s=="" or type(s)!=str:
                  return []
               total_data =  s.split(";") +total_data
               
               #$print year   
               ii=ii+1
               if ii>8:
                    return []
               if len(total_data)>=num:
                       # print total_data
                       return total_data
               year = year -1
           
       except Exception,e:
            if exp_sig==1:
                print 'wrong! try: ', e,sys.exc_info()[2].tb_lineno
       return []


def datediff(beginDate): 
    # format="%Y%m%d"; 
    x = datetime.date.today() 
    y = datetime.date(int(beginDate[0:4]),int(beginDate[4:6]),int(beginDate[6:]))  
    count =0    
    count=(x-y).days
    return count

       
def get_stock_data2(code,this_year):
        wrong = 0
        #http://d.10jqka.com.cn/v2/line/16_1A0001/01/2016.js
        if code=="1A0001":
            url=r"http://d.10jqka.com.cn/v2/line/16_" + code + r"/01/" + this_year + ".js"
        else:
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
                            # print "=============================="
                            if wrong >8:
                                return "w"
                            r = br.open(url, timeout=8)
                            html = r.read()
                            if len(html)<50 or type(html)!=str:
                                continue
                            break
                  except Exception,e:
                            if exp_sig==1:
                                print 'someting wrong! try: ', e,sys.exc_info()[2].tb_lineno,wrong 
                            if wrong >8:
                                return "w"

        pos = html.find(':')
        html = html[pos+1:len(html)-3]
        # print html
        return html
        
#获取当天的股票实时数据
def get_realtime_data2(code):
        wrong = 0
        #http://d.10jqka.com.cn/v2/line/hs_601890/01/today.js
        url = r"http://d.10jqka.com.cn/v2/line/hs_" + code + r"/01/today.js"
        # url = "http://hq2fls.eastmoney.com/EM_Quote2010PictureApplication/Flash.aspx?Type=CR&ID="+code+"1&lastNum=3&csum=0&cnum=-1&ctype=0"
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
                            if wrong >8:
                                return -1
                            r = br.open(url, timeout=8)
                            html = r.read()
                            if len(html)<100 or type(html)!=str:
                                continue
                            break
                  except Exception,e:
                            if exp_sig==1:
                                print 'someting wrong! try: ',e,sys.exc_info()[2].tb_lineno,wrong                     
                            if wrong >8:
                                print 'I HAVE TRYED 4 TIMES, BUT ALL FAILED!!!!!'
                                return -1

        html = html.replace('"',"")
        # print "<<<",html
        if(len(html)<=25):
               return -1
        
        tmp_list=""
        a=html.replace('"',"")
        a=a.replace('{',"")
        a=a.replace('}',"")
        a = a.split(",")
        if len(a)<5:                    #如果当天停牌，数据元素个数只有4个
            return -1
        #print html
        a[0].split(":")[-1]
        tmp_list = tmp_list + a[0].split(":")[-1]+","
        tmp_list = tmp_list + a[1].split(":")[-1]+","
        tmp_list = tmp_list + a[2].split(":")[-1]+","
        tmp_list = tmp_list + a[3].split(":")[-1]+","
        tmp_list = tmp_list + a[4].split(":")[-1]+","
        tmp_list = tmp_list + a[5].split(":")[-1]+","
        tmp_list = tmp_list + "0,0"
        # print html
        return tmp_list

def get_percent_eq(date,num,ch):
    total_data=date
    n=num
    eq = 0.0
    start1 = 0.0
    l = total_data[len(total_data)-1].split(",")
    # start1 = l[1]
    stop = l[4]
    l = total_data[len(total_data)-n-1].split(",")
    start = l[1]   
    #print float(start1),start
    n=0
    tlong = len(total_data)
    # print total_data
    try:
        if float(start)-0.0>=0.01:
            price_up_down = (float(stop)-float(start))/float(start)
        else:
            price_up_down = 0.0 
            
        while 1:
            ll = total_data[tlong-n-ch-1].split(",")
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
    
def get_total_raw_data(line,i):
    global fname
    global lock
    global now_c
    # global total_data
    global n
    global statics_days
    global useful_data_len

    global count_days
    # print "++++++",now_c,"++++++3"
    total_data=[]
    lock.acquire()
    # now_c=now_c +1
    lock.release() 
    end_price = 0.0
    end_price_single = 0.0
    end_vol = 0
    # print "++++++",now_c,"++++++4"
    # vol_day = 2   #统计最近多少天的交易量
    temp_total_len = 0
    total_res=[]
    total_price=[]
    up_days = 0
    all_go_updown = []
    all_stop_price =[]
    try:
        total_data=get_full_data(line, statics_days)
        checks = total_data[-1]
        ss = checks.split(",")
        
        # fname = time.strftime('%Y%m%d',time.localtime(time.time()))
        if datediff(ss[0])>10:
            lock.acquire()
            now_c=now_c -1
            lock.release() 
            return
        temp_total_len = len(total_data)
        if temp_total_len<statics_days:
            lock.acquire()
            now_c=now_c -1
            lock.release() 
            return
        checks = total_data[-1]
        end_price_single = float(ss[4])
        end_vol = float(ss[5])
        eql40 = get_percent_eq(total_data,13,1)    #4日均线在4日均线以下，直接返回，不满足条件
        eql4 = get_percent_eq(total_data,2,1)    #4日均线
        if eql40>eql4:
            lock.acquire()
            now_c=now_c -1
            lock.release() 
            return
        #计算，下跌时比指数跌的少，长时比指数长的多
        x =0
        NUM=7
        xx = 0
        final_days = 0
        
        while x<=10:
            vol_1 = total_data[temp_total_len-1-x] 
            ss1 = vol_1.split(",")
            total_price.append(float(ss1[3]))
            total_price.append(float(ss1[2]))
            all_stop_price.append(float(ss1[4]))
            if(float(ss1[4])>float(ss1[1])):
                up_days = up_days + 1
            x=x+1
        while x<count_days:                                            #check 15 days to 20 days
            vol_1 = total_data[temp_total_len-1-x] 
            ss1 = vol_1.split(",")
            total_price.append(float(ss1[3]))
            total_price.append(float(ss1[2]))
            all_stop_price.append(float(ss1[4]))
            if(float(ss1[4])>float(ss1[1])):
                up_days = up_days + 1
            
            price_len = len(all_stop_price)-1
            i = 0
            all_swag = []
            while i<price_len:
                temp_swag = (all_stop_price[i]-all_stop_price[i+1])/all_stop_price[i+1]
                #print temp_swag#,"00000000000000000000000000000"
                all_swag.append(temp_swag)
                i = i +1 
            temp_min = min(all_swag);
            print "up_days>0.65*count_days , temp_min",up_days,x,line,temp_min
            if up_days>0.65*x and temp_min>-0.03:
                sorted_price = sorted(total_price)
                start_price = sorted_price[0]
                end_price = sorted_price[len(sorted_price)-1]
                c_res = (end_price - start_price)/start_price 
                if(c_res>=0.015 and c_res<=0.12) and ((end_price_single-start_price)/start_price)>0.02:
                    lock.acquire()
                    open(fname,"a").write(str(0)+line+"\n") 
                    now_c=now_c -1
                    lock.release() 
                    return
            x = x + 1
                
    except Exception,e:
        if exp_sig==1:
            print e,sys.exc_info()[2].tb_lineno
        lock.acquire()
        now_c=now_c -1
        lock.release() 
        return
    print "=============",i,">",now_c,"================="

    print "vol check not pass!!!",line
    lock.acquire()
    now_c=now_c -1
    lock.release() 
        
    return


#http://d.10jqka.com.cn/v2/line/hs_600202/01/2016.js    上证http://d.10jqka.com.cn/v2/line/16_1A0001/01/2016.js
#20161020,11.80,11.80,11.57,11.66,4818603,56246662.00,1.257
    
    
for line in open('proxy.txt','r'):
    line = line.strip()
    if line!="":
        proxys.append(line) 
        
this_year = time.strftime('%Y',time.localtime(time.time()))
statics_days = 50  #统计多少天的交易量
count_days = 20    #做比较的天数

useful_data_len = int(0.4*statics_days)  #取最小交易量的多少天
lock2 = thread.allocate_lock()
#ss= get_stock_data("601933",this_year)
up_down_day = 3  #统计最近多少天的涨跌幅
i=0
n=0
now_c=0
th_count=40
lock = thread.allocate_lock()
# lock2 = thread.allocate_lock()
fnamet = time.strftime('%Y-%m-%d',time.localtime(time.time()))+".txt"
fname ="higher40-movelittle-highest-lowest"+fnamet
# fname2 =fnamet+"_buy_vol_plus.txt"
# print fname2
if (os.path.isfile(fname)):
    os.remove(fname)


now_c=0
i=0
check_point = 0
for line in open('code.txt','r'):#fname2
    line = line.strip()
    if line =="":
        continue
    while now_c>th_count:
        print "++++++++++th_count",now_c,th_count,i
        check_point = check_point + 1
        if check_point>5:
            now_c = now_c-10
        time.sleep(random.uniform(20, 40))
    i = i +1
    lock.acquire()
    now_c=now_c +1
    lock.release() 
    print "create new thread!!!!",line
    thread.start_new_thread(get_total_raw_data,(line[0:6],i))
    # time.sleep(random.uniform(10, 15))

while now_c>0:
    print "wait all done",now_c
    time.sleep(random.uniform(5, 15)) 
    
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


