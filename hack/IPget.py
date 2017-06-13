#coding:utf-8
import requests
from bs4 import BeautifulSoup
#获取外网IP
def GetOuterIP():
  url = r'http://www.whereismyip.com/'
  r = requests.get(url)
  bTag = BeautifulSoup(r.text, 'html.parser', from_encoding='utf-8').find('b')
  ip = ''.join(bTag.stripped_strings)
  print('ip:' + ip)
if __name__ == '__main__':
  GetOuterIP()