from ast import parse
from requests_html import HTMLSession

import re

# Creating a class to instance
# class Entry:
#     def __init__(self, title, rank, comments, score):
#         self.title = title
#         self.rank = rank
#         self.comments = comments
#         self.score = score

# entries lists
entries_titles = []
entries_body = []
entries_res = []

URL = 'https://news.ycombinator.com/'

session = HTMLSession()

r = session.get(URL)

def get_entry_head_parsed(entry):
    title = entry.find('a.titlelink', first=True).text.strip()
    rank = entry.find('span.rank', first=True).text.strip()

    entryHead = {
    'title': title,
    'rank': rank
    }

    return entryHead

def get_entry_body_parsed(entry):

    try:
        points = entry.find('span.score', first=True).text.strip()
    except AttributeError as err:
        points = 'None'

    comments = entry.find('td.subtext', first=True).text.strip()
    comment_splited = comments.split('| ') #it is a list
    comment = comment_splited[len(comment_splited)-1].replace(u'\xa0comments', u'') #extract just the comments and remove the extra bad chars
    if comment[0].isdigit():
        comment=int(comment)
         #clean the entries do not have comments
    else:
        # if there are no comments, zero
        comment = 0
  
    entryBody = {
    'points': points,
    'comments': comment
    }
    return entryBody

# split because some data are in different tags
def get_entries_titles():
    entries = r.html.find('tr.athing')
    for entry in entries:
        entries_titles.append(get_entry_head_parsed(entry))

def get_entries_body():
    entries = r.html.find('td.subtext')
    # print(entries)
    for entry in entries:
        entries_body.append(get_entry_body_parsed(entry))

def merge_dics(dic1, dic2):
    get_entries_titles()
    get_entries_body()

    for index in range(0,len(dic1)):
        entry = {
            'title': dic1[index]['title'],
            'rank': dic1[index]['rank'],
            'comments': dic2[index]['comments'],
            'points': dic2[index]['points']
        }
        entries_res.append(entry)
    return entries_res

# get all the entries with the data required
all_entries = merge_dics(entries_titles, entries_body)

# print(all_entries)
# print(len(all_entries))


# Filter all previous entries with more than five words in the title ordered by the number of comments first.
def filter_ordered_by_comments(entryList):
    resList = []
    for entry in entryList:
        if len(entry['title'].strip().split(" ")) > 5:
            resList.append(entry)
    resList = sorted(resList, key=lambda d: d['comments']) 
    return resList

first_filter = filter_ordered_by_comments(all_entries)

print(first_filter)
print(len(first_filter))


# Filter all previous entries with less than or equal to five words in the title ordered by points.
def filter_ordered_by_points(entryList):
    resList = []
    for entry in entryList:
        if len(entry['title'].strip().split(" ")) <= 5:
            resList.append(entry)
    resList = sorted(resList, key=lambda d: d['points']) 
    return resList

second_filter = filter_ordered_by_points(all_entries)

print(second_filter)
print(len(second_filter))