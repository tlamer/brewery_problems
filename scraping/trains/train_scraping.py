# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import re, csv
import requests
from bs4 import BeautifulSoup

# <codecell>

r = requests.get('http://www.poloha.vlaku.info/')
soup = BeautifulSoup(r.text)

# <codecell>

trains = []

# <codecell>

for tag in soup.find_all(text=re.compile('mešká')):
    train = [x for x in tag.parent.parent.strings]
    if train[2] == '\xa0':
        trains.append((train[1],int(train[7])))
    else:
        trains.append((train[1] + ' - ' + train[2],int(train[7])))

# <codecell>

trains.sort(key=lambda x: x[1])

# <codecell>

# uloha #1
with open('1.csv','w',newline='') as f:
    writer = csv.writer(f)
    for train in trains:
        if (train[1] == 10):
            writer.writerow(train)
            

# <codecell>

# uloha #2
with open('2.csv','w',newline='') as f:
    writer = csv.writer(f)
    writer.writerows(trains[-10:])

# <codecell>

print(trains)

# <codecell>


