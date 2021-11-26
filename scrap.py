import pandas as pd
from googlesearch import search
import requests
import re
from bs4 import BeautifulSoup
import os

def listToString(s):    
    # initialize an empty string 
    str1 = ""     
    # traverse in the string  
    index = 0 
    for ele in s:
        if index != 0:
            str1 += ","
        str1 += ele
        index +=1  
    # return string   
    return str1 
class GoogleURLScraper():
    def __init__(self):
        self.search_string = "* @ * {string} *.com"
    def scrape(self, string):
        # write csv headers
        if os.path.exists('result.csv'):
            os.remove('result.csv')
        columns=['url', 'email']
        df = pd.DataFrame(columns = columns)
        df.to_csv('result.csv', mode='x', index=False, encoding='utf-8')

        search_string = self.search_string.format(string = string)
        # search all pages and write
        for url in search(search_string, tld='com.pk', lang='es'):
            item = {'url':'', 'email':''}
            print(url)
            if url.find(string) != -1: # check to contain search string
                new = []
                item['url'] = url
                email = self.findEmail(url)
                print(email)
                item['email'] = email
                new.append(item)
                ## save datas in csv
                df = pd.DataFrame(new, columns = columns)
                df.to_csv('result.csv', mode='a', header=False, index=False, encoding='utf-8')      
        print('end')
    def findEmail(self, url):
        res = ''
        EMAIL_REGEX = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        if soup != None:
            list = []
            for re_match in re.finditer(EMAIL_REGEX, soup.text):
                list.append(re_match.group())
            res = listToString(list)
        return res

if __name__ == '__main__':
    scraper = GoogleURLScraper()
    scraper.scrape('ceramica')