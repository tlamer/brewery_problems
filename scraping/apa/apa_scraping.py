# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import re, csv
import requests
from bs4 import BeautifulSoup

# <codecell>

BASE = 'http://www.apa.sk/index.php?navID=206'

# <codecell>

def scrape_years(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    
    years = soup.find('select', attrs = {'name':'rok'}).find_all('option', attrs = {'value':re.compile('[0-9]{4}')})
    
    return list(year.text for year in years)
    

# <codecell>

def scrape_pages(year):
    r = requests.get(BASE + '&rok=' + str(year))
    soup = BeautifulSoup(r.text)
    
    pages = soup.find('div', attrs= {'id':'strankovanie'}).find(text = re.compile('stránky'))
    
    reg = re.search('(?<=stránky \([0-9]/)[0-9]+', pages)
    return int(reg.group(0))

# <codecell>

def scrape_data(year, writer):
    pages = scrape_pages(year)
    for page in range(pages):
        print(str(year) + ': ' + str(page + 1))
        r = requests.get(BASE + '&rok=' + str(year) + '&offset=' + str(page))
        soup= BeautifulSoup(r.text)
    
        table = soup.find('table').find_all('tr')[1:]
        
        for row in table:
            entry = row.find_all('td')
            entry = list(x.text for x in entry)
            entry.insert(0, year)
            writer.writerow(entry)
        

# <codecell>

fd = open('apa.csv', 'w', newline='')
wrt = csv.writer(fd)

# <codecell>

for year in scrape_years(BASE):
    scrape_data(year, wrt)

# <codecell>

fd.close()

