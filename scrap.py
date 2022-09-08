#web site - https://news.ycombinator.com/

# pip install bs4

from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

url = 'https://news.ycombinator.com/'
page = requests.get(url)
limit = 30

#Titles
soup = BeautifulSoup(page.content, 'html.parser')

raw_titles = soup.find_all('a', class_='titlelink')

titles = list()

for index in range(0,limit):
    titles.append(raw_titles[index].text)
print('TITLES')
print(titles)
print(len(titles))

#Rank/Number of the order
soup = BeautifulSoup(page.content, 'html.parser')

raw_rank = soup.find_all('span', class_='rank')

rank = list()

for index in range(0,limit):
    rank.append(float(raw_rank[index].text))
print('NUMBER OF THE ORDER')
print(rank)
print(len(rank))

#Comments

soup = BeautifulSoup(page.content, 'html.parser')

# raw_comments = soup.find_all('a', {'href': re.compile(r'item\?id=')}, {'href': re.compile(r'item\?id=')}, text = re.compile('discuss|comment|comments'))

# raw_comments = soup.find_all('td', class_='subtext')

# for raw in raw_comments:
#     print(raw)

print(len(soup.find_all('td', class_='subtext')))

# print('COMMENTS')
# print(raw_comments)
# print(len(raw_comments))

# comments = list()

# for index in range(0,len(raw_comments)):
#     value = raw_comments[index].text
#     # removing \xa0 from the comments
#     value = value.replace(u'\xa0', u' ')
#     comments.append(value)
    # print(str(raw_comments[index].text))
# print(comments)
# print(len(comments))
# #Point
# soup = BeautifulSoup(page.content, 'html.parser')

# raw_points = soup.find_all('span', class_='score')
# print('POINTS')
# print(raw_points)
# print(len(raw_points))


#TODO
#TRY TO MAKE JUST 1 ONLY FOR LOOP FOR EVERY ONE. EVERYTHING INSIDE THE FOR LOOP