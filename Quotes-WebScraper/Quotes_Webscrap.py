import pandas as pd
import numpy as np
import bs4 as bs
import urllib.request
from urllib.parse import urlparse, urljoin

# Declaring the base urls - Source of Data
base_url = 'http://quotes.toscrape.com/'
source = urllib.request.urlopen(base_url).read()
soup = bs.BeautifulSoup(source, 'html.parser')


#function to get the quotes text from the webpages
def quotes(url):
    new_list = []
    source = urllib.request.urlopen(url).read()
    soup = bs.BeautifulSoup(source, 'html.parser')
    data = soup.find_all('div', attrs = {'class':'row','class':'col-md-8'})
    for i in data:
        text = i.find_all('span', class_='text')
        for j in text:
            new_list.append(j.text.strip())

    return new_list

# Getting the URLs
def get_urls(soup):
    all_tags = []
    for i in soup.find_all('div', class_ = 'col-md-4 tags-box'):
        tags = i.find_all('a', href = True)
        for j in tags:
            all_tags.append(j.get('href'))
    base_url = 'http://quotes.toscrape.com/'
    tag_urls = []
    for tag_url in all_tags:
        url_tag = urljoin(base_url, tag_url)
        tag_urls.append(url_tag)
    return tag_urls


#Main function
all_quotes = []
urls = get_urls(soup)
for url1 in urls:
   # print(url1)
    quote_l = quotes(url1)
   # print(quote_l)
    next_page = soup.select('li.next > a')
    if not next_page or not next_page[0].get('href'):
        break
    url1 = url1 + next_page[0].get('href').lstrip('/')
   # print(url1)
    all_quotes.append(quote_l)
    #print(len(all_quotes))
new_list = []
for i in all_quotes:
    for j in i:
        new_list.append(j)
quotes_to_scrap = pd.DataFrame()
quotes_to_scrap['Quotes'] = new_list

print(quotes_to_scrap)








