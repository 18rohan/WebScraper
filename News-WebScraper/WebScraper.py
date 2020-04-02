import bs4 as bs
import urllib.request
import pandas as pd

#getting the source of data
source = urllib.request.urlopen("https://news.ycombinator.com").read()

#creating an object of beautifulsoup with: source of data & type of pasrser
soup = bs.BeautifulSoup(source,'html.parser')

#printing out the title
print(soup.title)
print(soup.title.contents[0])

#reading the data
data = soup.find_all('tr',attrs={'class':'athing'})

#looping through the data, getting the: news, links, score for the articles in the website
articles = []
for news in data:
    items_a = news.find('a', class_ = 'storylink')
    news_s = (items_a.text)
    item_link = items_a.get('href') if items_a else None
    next_row = news.find_next_sibling('tr')
    score = next_row.find('span', class_='score')
    score_final = score.get_text(strip=True) if items_a else '0 Points'

    articles.append({
        'link':item_link,
        'news':news_s,
        'score':score_final
    })

#printing the data gathered from the website.
print(articles)