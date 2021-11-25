#!/usr/bin/env python
from lxml.html import fromstring
import requests
from itertools import cycle
import traceback
from termcolor import colored

def get_proxies():      #AUTOPROXY - SCRAPE PROXYS FROM WEB
    url = 'https://free-proxy-list.net/'
    #url = 'http://spys.one/free-proxy-list/ES/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies

#----------------------------------------------------------------------------------------------------------
proxies = ['212.205.112.162:49595', '183.89.78.227:8080', '109.121.207.134:38383', '110.93.230.218:35895', '122.102.41.82:47684']  #HARDCODED PROXYS HERE - WORKING!
# --> GET FREE PROXYS FROM -->  http://spys.one/en/http-proxy-list/
#proxies = get_proxies()    #COMMENTING THIS LINE OR NEXT ONE, SWITCH BETWEEN AUTOPROXY AND MANUAL PROXYS 
#----------------------------------------------------------------------------------------------------------

proxy_pool = cycle(proxies)
url = 'https://httpbin.org/ip'
for i in range(1,6):
    proxy = next(proxy_pool)    #Get a proxy from the pool
    print(colored(' **************************************************** ', 'yellow'))
    print('  Request #{}'.format(i))  #------ DEBUGING PROXY USE ------
    try:
        response = requests.get(url,proxies={"http": proxy, "https": proxy})
        print('  Using proxy:         {}'.format(proxy))    #------ DEBUGING PROXY USE ------
        print('  Response received:   {}'.format(response.json()))

    except:
        print(" Skipping. Connnection error ")