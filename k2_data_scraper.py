'''
API/Web Scraper to pull data from corrected light curves.
python3 -m cProfile -s tottime k2_data_scraper.py
'''
__author__ = "Ollie Jackson"
#import requests
from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
import re

def linker(url):
    host = 'https://lweb.cfa.harvard.edu/~avanderb/'
    link = urllib.request.urlopen(host + url).read()
    #link = requests.get(host + url).text -> This took about 5x as long
    soup = BeautifulSoup(link, 'lxml')
    return soup

# Looping through <a tags in html to find the ones we want
def scrape_init(url):
    tags = linker(url)('a')

    for tag in tags:
        if 'Explore Campaign' in tag.string:
            scrape_init(re.findall('all.*\.html', str(tag))[0])
            #break
        elif 'EPIC' in tag.string:
            scrape_final(re.findall('k2.*\.html', str(tag))[0])
            break

#Pulling data and saving based on the EPIC num
def scrape_final(url):
    tags = linker(url)('a')

    for tag in tags:
        if 'Corrected light curve' in tag.string:
            data_link = re.findall('http://.*.txt', str(tag))
            file_name = url.split('/')[1].split('.')[0]
            file = open(file_name, 'w')
            x = urllib.request.urlopen(data_link[0]).read().decode()
            file.write(x)
            return #once it's found the corrected light curve it's done


if __name__ == '__main__':
    scrape_init('k2.html')
