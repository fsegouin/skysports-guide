#!/usr/bin/python
# Filename: get-tv-guide.py

import requests, time, re
from datetime import datetime
from bs4 import BeautifulSoup

def get_channel_name(x):
    return {
        0: '',
        1: 'Sky Sports 1',
        2: 'Sky Sports 2',
        3: 'Sky Sports 3',
        4: 'Sky Sports 4',
        5: 'Sky Sports 5',
        6: 'Sky Sports News HQ',
        7: 'Sky Sports F1',
    }.get(x, '?')

def main():
    page = requests.get('http://www.skysports.com/watch/tv-guide')
    c = page.content
    soup = BeautifulSoup(c, 'lxml')

    channels = soup.find_all('div', 'row-table')

    hours = datetime.now().strftime('%-I')
    minutes = datetime.now().strftime('%M')
    am_pm = datetime.now().strftime('%p').lower()

    print 'Now:', hours + ':' + minutes + am_pm

    regex = re.compile(ur'\b' + hours + ':..' + am_pm)

    for index, c in enumerate(channels):
        if index > 0:
            print '============'
            print get_channel_name(index)
            print '============'
            programs = c.find_all('a', '-a-block tvg-det callfn')
            for p in programs:
                title = p.find('h4')
                time = p.find('p')
                if regex.findall(time.string.strip()):
                    print title.string.strip(), '-', time.string.strip()

if __name__ == "__main__":
    main()
