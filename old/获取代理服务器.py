#coding:utf-8 
import urllib2
import string
import sys, getopt
import os
import random
import time
import thread 
import re
import json
import time
import random
import copy
import socket
import threading
import codecs
import mechanize
import cookielib
import datetime
#from data import *
reload(sys)
sys.setdefaultencoding('utf-8')

#获取网络股票数据
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

def get_urls(url):
    uu =["http://www.youdaili.net/Daili/http/","http://www.youdaili.net/Daili/QQ/","http://www.youdaili.net/Daili/guonei/","http://www.youdaili.net/Daili/guowai/"]
    url2 = url
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
    # br.set_proxies({"http": "60.191.156.83:3128"}) 
    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    html = ""
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    i=1

    try:
        r = br.open(url2, timeout=15)
        html = r.read()
    except Exception,e:
        print "get web failed!2",e
    if len(html)<100:
        return ""
    #print html
    total_urls=[]
    for ut in uu: 
        pos = html.find(ut)
        #print pos
        while pos!=-1:
            pos = pos +len(ut)
            tmp= html[pos+4:pos+9]
            #print tmp
            if tmp ==".html":
                #print ut+html[pos:pos+9]
                total_urls.append(ut+html[pos:pos+9])
            pos = html.find(ut,pos)
        pos = 0
    #print total_urls
    #print len(total_urls),"==================="
    return total_urls


    
def get_all_data(url):

    url2 = url
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
    # br.set_proxies({"http": "60.191.156.83:3128"}) 
    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    html = ""
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    i=1

    try:
        r = br.open(url2, timeout=15)
        html = r.read()
    except Exception,e:
        print "get web failed!2",e
    if len(html)<100:
        return []
    pos = html.find("<p>")
    pos2 =html.find("/p>",pos)
    html = html[pos+3:pos2]
    html=html.split("\r\n")
    #print html
    ips=[]
    for x in html:
        t= x.split("@")
        ips.append(t[0])
    #print ips
    #print len(ips),"==================="
    return ips
    
def get_all_data2(url):

    url2 = "http://www.xicidaili.com/nn/"+url
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
    # br.set_proxies({"http": "60.191.156.83:3128"}) 
    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    html = ""
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    i=1

    try:
        r = br.open(url2, timeout=15)
        html = r.read()
    except Exception,e:
        print "get web failed!2",e
    if len(html)<100:
        return []
    pos = html.find("http://fs.xicidaili.com/images/flag/")
    ips=[]
    while pos!=-1:
        pos2 =html.find("<td>",pos)
        pos3 =html.find("</td>",pos2)
        pos4 =html.find("<td>",pos3)
        pos5 =html.find("</td>",pos4)
        ips.append(html[pos2+4:pos3]+":"+html[pos4+4:pos5])
        pos = html.find("http://fs.xicidaili.com/images/flag/",pos5)

    #print html
    
    print ips
    #print len(ips),"==================="
    return ips

def get_all_data3(url):

    url2 = "http://www.xicidaili.com/nt/"+url
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
    # br.set_proxies({"http": "60.191.156.83:3128"}) 
    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    html = ""
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    i=1

    try:
        r = br.open(url2, timeout=15)
        html = r.read()
    except Exception,e:
        print "get web failed!2",e
    if len(html)<100:
        return []
    pos = html.find("http://fs.xicidaili.com/images/flag/")
    ips=[]
    while pos!=-1:
        pos2 =html.find("<td>",pos)
        pos3 =html.find("</td>",pos2)
        pos4 =html.find("<td>",pos3)
        pos5 =html.find("</td>",pos4)
        ips.append(html[pos2+4:pos3]+":"+html[pos4+4:pos5])
        pos = html.find("http://fs.xicidaili.com/images/flag/",pos5)

    #print html
    
    print ips
    #print len(ips),"==================="
    return ips

def get_all_data4(url):
    url2 = "http://www.66ip.cn/"+url+".html"
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
    # br.set_proxies({"http": "60.191.156.83:3128"}) 
    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    html = ""
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    i=1

    try:
        r = br.open(url2, timeout=15)
        html = r.read()
    except Exception,e:
        print "get web failed!2",e
    if len(html)<100:
        return []
    pos = html.find("<td>ip</td>")
    pos =html.find("<tr>",pos)
    ips=[]
    while pos!=-1:   
        pos3 =html.find("<td>",pos)
        pos4 =html.find("</td>",pos3)
        pos5 =html.find("<td>",pos4)
        pos6 =html.find("</td>",pos5)
        ips.append(html[pos3+4:pos4]+":"+html[pos5+4:pos6])
        pos = html.find("<tr>",pos6)

    #print html
    
    print ips
    #print len(ips),"==================="
    return ips    
    
def get_all_data5():
    url2 = "http://proxy.ipcn.org/proxylist2.html"
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
    # br.set_proxies({"http": "60.191.156.83:3128"}) 
    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    html = ""
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    i=1

    try:
        r = br.open(url2, timeout=15)
        html = r.read()
    except Exception,e:
        print "get web failed!2",e
    if len(html)<100:
        return []
    pos = html.find("World Proxy List, Powered by proxy.ipcn.org")
    pos =html.find(".",pos+len("World Proxy List, Powered by proxy.ipcn.org"))
    pos2 = html.find("</pre>",pos)
    html=html[pos-2:pos2]
    all=html.split("\n")
    ips=[]
    for alls in all:   
        alls=alls.strip()
        if alls!="":
            ips.append(alls)

    #print html
    
    print ips
    #print len(ips),"==================="
    return ips        

def get_all_data6(url):
    url2 = "http://www.004388.com/"+url
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
    # br.set_proxies({"http": "60.191.156.83:3128"}) 
    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    html = ""
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    i=1

    try:
        r = br.open(url2, timeout=15)
        html = r.read()
    except Exception,e:
        print "get web failed!2",e
    if len(html)<100:
        return []
    pos = html.find("info_list")
    pos =html.find("<tr>",pos)
    ips=[]
    while pos!=-1:   
        pos3 =html.find('width="180">',pos)
        pos4 =html.find("</td>",pos3)
        pos5 =html.find('width="80">',pos4)
        pos6 =html.find("</td>",pos5)
        if pos3==-1:
            break
        ttx1=html[pos3+12:pos4]
        ttx2=html[pos5+11:pos6]
        # print ttx1+":"+ttx2
        # time.sleep(random.uniform(1, 3))
        if ttx1!="" and ttx2!="":
            ips.append(ttx1+":"+ttx2)
        pos = html.find("<tr>",pos6+30)

    #print html
    
    print ips
    # print "==================="
    return ips    
 
def get_all_data7(url,i):
    url2 = "http://www.004388.com/"+url+"/index_"+str(i)+".html"
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
    # br.set_proxies({"http": "60.191.156.83:3128"}) 
    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    html = ""
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    i=1

    try:
        r = br.open(url2, timeout=15)
        html = r.read()
    except Exception,e:
        print "get web failed!2",e
    if len(html)<100:
        return []
    pos = html.find("info_list")
    pos =html.find("<tr>",pos)
    ips=[]
    while pos!=-1:   
        pos3 =html.find('width="180">',pos)
        pos4 =html.find("</td>",pos3)
        pos5 =html.find('width="80">',pos4)
        pos6 =html.find("</td>",pos5)
        if pos3==-1:
            break
        ttx1=html[pos3+12:pos4]
        ttx2=html[pos5+11:pos6]
        # print ttx1+":"+ttx2
        if ttx1!="" and ttx2!="":
            ips.append(ttx1+":"+ttx2)
        pos = html.find("<tr>",pos6+30)

    #print html
    
    print ips
    #print len(ips),"==================="
    return ips 
 
def check_data(ip,x):
    #print code,"11111111111111111"
    #code = code.strip()
    global gate
    global lock
    global lock2
    global sigs

    ip = ip.replace('<span style="font-size:14px;">',"")
    url2 = "http://data.eastmoney.com/zjlx/zs000001.html"
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
    br.set_proxies({"http": ip}) 
    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    html = ""
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    i=1
    while 1:
        try:
            r = br.open(url2, timeout=10)
            html = r.read()
            break
        except Exception,e:
            print "get web failed!2",e
            i=i+1
            if i>2:
                break

    if len(html)>5000 and -1!=html.find("StockCode"):
        lock2.acquire() 
        print "get one: " ,ip
        open("proxy.txt",'a').write(ip+"\n")
        lock2.release()        
       
    lock.acquire() 
    sigs =sigs -1
    lock.release()
    thread.exit_thread()
    
    
lock = thread.allocate_lock()
lock2 = thread.allocate_lock()   
useful_ip = []
all_ips = []
# all_ips=all_ips+get_all_data5() 
for line in open('proxy.txt','r'):
    line = line.strip()
    if line!="":
        all_ips.append(line) 

# total_urlsx=["ip","ippt","ipgw","ipgwtm"]        
# for ip in total_urlsx:
    # all_ips=all_ips+get_all_data6(ip)  
    # time.sleep(random.uniform(0.5, 1))   

# total_urlsx=["ip","ippt","ipgw","ipgwtm"]        
# for ip in total_urlsx:
    # i=2
    # while i<=20:
        # all_ips=all_ips+get_all_data7(ip,i) 
        # i = i+1        
        # time.sleep(random.uniform(0.5, 1))  
    
# time.sleep(random.uniform(16, 30))        
#-----------stage 1


# it = 2
# while it<=50:
    # all_ips=all_ips+get_all_data4(str(it))
    # time.sleep(random.uniform(0.5, 1))
    # it = it +1
    
# time.sleep(random.uniform(15, 115))
#-----------stage 2
it = 1
while it<=25:
    all_ips=all_ips+get_all_data3(str(it))
    time.sleep(random.uniform(0.5, 1))
    it = it +1
    
# open("log.txt","a").write(get_total_raw_data() +"\n")   
#get_all_data("http://www.youdaili.net/Daili/http/3892.html")
total_urls = get_urls("http://www.youdaili.net") 
#-----------stage 3
# if len(total_urls)<=0:
    # return ""
for ip in total_urls:
    all_ips=all_ips+get_all_data(ip)
    
    
#-----------stage 4  
# it = 51
# while it<=80:
    # all_ips=all_ips+get_all_data4(str(it))
    # time.sleep(random.uniform(0.5, 1))
    # it = it +1
print "-----------stage 4  "
all_ips=all_ips+get_all_data5()    
#-----------stage 5   
it = 1
while it<=10:
    all_ips=all_ips+get_all_data2(str(it))
    time.sleep(random.uniform(0.5, 1))
    it = it +1
 
s = []
for ip in all_ips:
    if ip not in s:
        s.append(ip)
# s = set(all_ips)
all_ips = s
print len(all_ips)
#print all_ips
if (os.path.isfile("proxy.txt")):
    os.remove("proxy.txt")
if (os.path.isfile("ips.txt")):
    os.remove("ips.txt")
for gg in all_ips:
    open("ips.txt",'a').write(ip+"\n")
sigs = 1
i =1    
for gg in all_ips:
    if sigs>=80:
        time.sleep(random.uniform(10, 12)) 
    if gg.find("<")>0:
        gg = gg.replace('<span style="font-size:14px;">',"")
    thread.start_new_thread (check_data,(gg,0))
    lock.acquire() 
    sigs =sigs +1
    lock.release()
    i=i+1
    if i%200 == 0:
        print len(all_ips),"=============="
    print "we are at: ",i,gg
while sigs>0:
        print "wait all finish"
        time.sleep(random.uniform(1, 12)) 
    # r = check_data(gg)
    # if r==1:
        # print "get one: " ,gg
        # open("proxy.txt",'a').write(gg+"\n")
    

    
    
    
    
    
    
    
    
    
    
    
