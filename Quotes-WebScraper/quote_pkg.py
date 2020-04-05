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
    author_names = []
    final_list = []
    source = urllib.request.urlopen(url).read()
    soup = bs.BeautifulSoup(source, 'html.parser')
    data = soup.find_all('div', attrs = {'class':'row','class':'col-md-8'})
    for i in data:
        text = i.find_all('span', class_='text')
        for j in text:
            new_list.append(j.text.strip())
    for author in data:
        author_name = author.find_all('small', class_='author')
        for a_n in author_name:
            author_names.append(a_n.text.strip())

       # final_list.append({
        #    'quotes':new_list,
         #   'authors':author_names
        #})
    return author_names, new_list

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

# Get author links to get author's personal info
def get_author_links(url):
    source = urllib.request.urlopen(url).read()
    soup = bs.BeautifulSoup(source, 'html.parser')
    data = soup.find_all('div', attrs = {'class':'row','class':'col-md-8'})
    author_links = []
    for i in data:
        author_link = i.select('a')
        for j in author_link:
            author_link2 = j.get('href')
            if 'author' in author_link2:
                author_links.append(author_link2)

    return author_links

def get_author_birthdate(all_author_urls):
    author_birthdates = []
    author_birthplaces = []
    author_info = {}
    for author_url_single in all_author_urls:
        source_author = urllib.request.urlopen(author_url_single).read()
        soup = bs.BeautifulSoup(source_author, 'html.parser')
        data_author = soup.select('p')
        for author in data_author:
            birthdate = author.find_all('span',class_='author-born-date')
            for i in birthdate:
                author_birthdates.append(i.text)
        for author in data_author:
            birthplace = author.find_all('span', class_='author-born-location')
            for j in birthplace:
                author_birthplaces.append(j.text)

                author_info = {
                'birthdate':author_birthdates,
                'birthplace':author_birthplaces
                }
    return author_birthdates, author_birthplaces





#Main function
all_authors3 = []
urls = get_urls(soup)
all_quotes = []
for url1 in urls:
    # print(url1)
    author_names,quote_l = quotes(url1)
  #  all_author_urls = get_author_links(url1)
    #author_birthdate, author_birthplace = get_author_birthdate()
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


all_author_urls = []
for url in urls:
        author_urls = get_author_links(url)
        for j in author_urls:
            final_url = base_url + j.lstrip('/')
            all_author_urls.append(final_url)

author_birthdates, author_birthplaces = get_author_birthdate(all_author_urls)
quotes_to_scrap['Author_birthdate'] = author_birthdates
quotes_to_scrap['Author_birthplace'] = author_birthplaces

print(quotes_to_scrap)










