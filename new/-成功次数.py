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
                            if wrong >10:
                                return "w"
                            r = br.open(url, timeout=15)
                            html = r.read()
                            if type(html)!=str:
                                html = ""
                                continue
                            if len(html)<50 :
                                time.sleep(10)
                                continue
                            break
                  except Exception,e:
                            print 'someting wrong! try: ', e,sys.exc_info()[2].tb_lineno,wrong 
                            if wrong >10:
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
    total_str =""
    it=0
    max_result = (0,0,0.0)   #短周期，长周期，回测结果
    data=[]
    while 1:
        try:
            #data = ["20150105,14.54,14.99,14.30,14.83,9047240,204847850.00,2.906","20150106,14.80,15.68,14.67,15.49,12682564,298067620.00,4.074","20150107,15.59,15.67,15.27,15.39,8602877,205040230.00,2.763","20150108,15.39,15.59,15.06,15.28,7247779,171583590.00,2.328","20150109,15.17,15.71,15.09,15.28,10831207,258771820.00,3.479"]
            if len(data)<30:
                data = get_full_data(line)
            too_len = len(data)
            print "let us start!!!!!!  check: ",line,too_len
            if(too_len<=70):
                break
            start_i = 7    #均线最小周期
            end_i = 20     #均线大小周期
            already_buy = 0
            max_total_income = 0        #保存最大成功交易次数
            best_cycle = 0
            while start_i<=end_i:
                buy_price = 0.0
                sell_price = 0.0
                temp_total_income = 0      #此算法第一版本为了简便期间，先计算成功次数，也就是满足买入条件则买入，如果接下来20个交易日内，价格上涨
                #超过10%，则表示一次正确的交易，temp_total_income加1
                y=50
                total_res=[];
                failed_cnt=0
                good_cnt = 0
                while y<too_len:
                    if already_buy == 0:          #如果当前状态是未买入状态，则判断是否满足买入条件
                        temp_res = -1 
                        temp_res = get_check_buy(data,start_i,y)
                        if temp_res == -1:
                            y = y +1
                            continue
                        buy_price = temp_res      #满足买入条件，则记录买入价格以及标记买入状态
                        #already_buy = 1
                        check_temp = 1
                        check_total = 20
                        while check_temp<=check_total:
                            try:
                                l = data[y+check_temp].split(",") 
                                l_start = data[y].split(",") 
                                temp_price = 0.0
                                temp_price = float(l[4])  #收盘价
                                if buy_price>0.0 and ((temp_price-buy_price)/buy_price)>0.15:
                                    temp_total_income = temp_total_income + 1 
                                    print "buy_price ,temp_price, result, cycle",buy_price,temp_price,(temp_price-buy_price)/buy_price,start_i
                                    #open("total_check_result_single_detail.txt","a").write(line+"\t"+l_start[0]+"\t"+str(start_i)+"\t"+str(buy_price)+"\t"+str(check_temp)+"\t"+str(temp_price)+"\n")
                                    good_cnt = good_cnt +1
                                    y = y + check_temp
                                    break
                            except Exception,e:
                                check_temp = check_temp + 1   
                                continue
                            check_temp = check_temp + 1 
                        if check_temp>=check_total:                     #买入信号出现后并没有在后面的20个交易日上涨超过20%
                            failed_cnt = failed_cnt + 1
                    y = y +1
                    
                if temp_total_income>max_total_income:
                    max_total_income = temp_total_income   #保存最好的命中次数和此时的周期
                    best_cycle=start_i
                start_i = start_i + 1
                if good_cnt>0:
                    total_str = total_str +line+"\t cycle: \t"+str(start_i-1)+"\t failed: \t"+str(failed_cnt)+"\t success: \t"+str(good_cnt)+"\n"
                    #open("total_check_result_single_detail.txt","a").write(line+"\t cycle: \t"+str(start_i-1)+"\t failed: \t"+str(failed_cnt)+"\t success: \t"+str(good_cnt)+"\n")
                print "to next cycle: ",start_i
            print line,"done!!!!!!!!!!"
            break
        except Exception,e:
            print "damn!something wrong!!1" ,e,sys.exc_info()[0],sys.exc_info()[2].tb_lineno,"    ",it
            it=it+1
            if it>10:
                break    
    lock.acquire()
    now_c=now_c -1
    if max_total_income>0:
        open("total_cycle_check_result_single.txt","a").write(line+"\t"+str(max_total_income)+"\t"+str(best_cycle)+"\n")
        
    open("total_check_result_single_detail.txt","a").write(total_str)
    open("total_check_result_single_detail.txt","a").write("\n\n\n")
    lock.release() 
    thread.exit_thread()
    print "finished!",i 
 

 
#检验卖出条件    
def get_check_sell(data,cycle,position):   #y为当时状况下是否满足买入条件  
    pass
    
    
    
#检验一个均线组合的回测结果，满足买入条件则返回买入价格（下一个交易日的最高价），否则返回-1   
def get_check_buy(data,cycle,position):   #y为当时状况下是否满足买入条件
    too_len=40
    y=0
    total_res=[]
    while y<too_len:
        vol_1 = 0
        vol_2 = 0
        vol_3 = 0
        vol_1,per_1 = get_percent_eq(data,cycle,position-y-4)     #NUM,0几天的均线，往后跳几天
        vol_2,per_2 = get_percent_eq(data,cycle,position-y-2)     
        vol_3,per_3 = get_percent_eq(data,cycle,position-y)    
        if vol_2<vol_1 and vol_3>vol_2:               #依次取10日均线，然后取两天前和两天后的10日均线。比较中间的点是最低点。也就是回调的最低点。
            total_res.append(vol_2)                    #如果y这点是回调的最低点，则保存这是的均线值。
        y = y + 1
    len_t = len(total_res)
    y=0
    my_res=0
    res = -1
    if len_t>=2 and total_res[0]>total_res[1]:
        while y<len_t -1:
            try:
                high = total_res[y]
                low = total_res[y+1]
                if high>low:                              #每次回调的最低点进行比较。也就是最近的回调最低点高于上一次的回调最低点
                    my_res = my_res+1         #越接近当前的，权重越高
                y = y + 1 
            except Exception,e:
                break
        #print "--------------",my_res,0.4*len_t
        if my_res > 0.6*len_t:
            x = 0
            while 1:
                res = get_highest_price(data,position+x)
                if res != -1:
                    break
                x = x + 1 
    return  res  
    
        
#获取下一个交易日的最高价        
def get_highest_price(data,y):
    l = []
    try:
        l = data[y].split(",") 
        highest_price = float(l[2])  
    except Exception,e:
        return -1;
    return highest_price
   
#获取下一个交易日的最低价        
def get_lowest_price(data,y):
    l = [] 
    try:
        l = data[y].split(",") 
        lowest_price = float(l[3])  
    except Exception,e:
        return -1;
    return lowest_price  
    
    
   



for line in open('proxy.txt','r'):
    line = line.strip()
    if line!="":
        proxys.append(line) 
th_count=20
lock = thread.allocate_lock()
this_year = time.strftime('%Y',time.localtime(time.time())) 
now_c=0

for line in open('code.txt','r'):
    line = line.strip()
    if line =="":
        continue
    if now_c>th_count:
        print "++++++++++th_count",th_count,now_c
        time.sleep(random.uniform(60, 100))
    thread.start_new_thread (update_data,(line,now_c))
    time.sleep(random.uniform(1, 3))



