import pandas as pd
import numpy as np
import bs4 as bs
import urllib.request
from urllib.parse import urlparse, urljoin
import quote_pkg

base_url = 'http://quotes.toscrape.com/'
source = urllib.request.urlopen(base_url).read()
soup = bs.BeautifulSoup(source, 'html.parser')


all_authors3 = []
urls = quote_pkg.get_urls(soup)
for url1 in urls:
    # print(url1)
    author_names,quote_l = quote_pkg.quotes(url1)
    all_quotes = []
    all_author_urls = quote_pkg.get_author_links(url1)
    for j in all_author_urls:
        final_url = base_url + j.lstrip('/')
        all_author_urls.append(final_url)
    author_birthdate, author_birthplace = quote_pkg.get_author_birthdate()
    for author in author_names:
        all_authors3.append(author)
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
quotes_to_scrap['Author'] = all_authors3
quotes_to_scrap['Author_birthdate'] = author_birthdate
quotes_to_scrap['Author_birthplace'] = author_birthplace
print(quotes_to_scrap)
