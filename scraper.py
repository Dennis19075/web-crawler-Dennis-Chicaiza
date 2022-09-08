from requests_html import HTMLSession

import re

from operator import itemgetter
import csv

class Scraper:

    def __init__(self, URL):
        self.URL = URL
        self.entries_titles = []
        self.entries_body = []
        self.entries_res = []
    
    def getWebSite(self):
        session = HTMLSession()
        r = session.get(self.URL)
        return r

    def get_entry_head_parsed(self, entry):
        title = entry.find('a.titlelink', first=True).text.strip()
        rank = entry.find('span.rank', first=True).text.strip()
        rank = re.sub("\D", "", rank)

        entryHead = {
        'title': title,
        'rank': rank
        }
        return entryHead

    def get_entry_body_parsed(self, entry):

        try:
            points = entry.find('span.score', first=True).text.strip()
            points = re.sub("\D", "", points) #extract only digits
        except AttributeError as err:
            points = '0'

        comments = entry.find('td.subtext', first=True).text.strip()
        comment_splited = comments.split('| ') #it is a list
        comment = comment_splited[len(comment_splited)-1].replace(u'\xa0', u'') #extract just the comments and remove the extra bad chars cant find comments because of the variant comment and comments
        comment = re.sub("\D", "", comment) #extract only digits
        
        if comment == "": #check if comments are empty
            comment = "0"

        entryBody = {
        'points': points,
        'comments': comment
        }
        return entryBody

    # split because some data are in different tags
    def get_entries_titles(self):
        r = self.getWebSite()
        entries = r.html.find('tr.athing')
        for entry in entries:
            self.entries_titles.append(self.get_entry_head_parsed(entry))

    def get_entries_body(self):
        r = self.getWebSite()
        entries = r.html.find('td.subtext')
        # print(entries)
        for entry in entries:
            self.entries_body.append(self.get_entry_body_parsed(entry))

    def get_all_entries(self, dic1, dic2): #merging dictionaries (head + body)
        self.get_entries_titles()
        self.get_entries_body()

        for index in range(0,len(dic1)):
            entry = {
                'title': dic1[index]['title'],
                'rank': int(dic1[index]['rank']),
                'comments': int(dic2[index]['comments']),
                'points': int(dic2[index]['points'])
            }
            self.entries_res.append(entry)
        return self.entries_res

    # FILTERS
    # Filter all previous entries with more than five words in the title ordered by the number of comments first.
    def filter_ordered_by_comments(self, entryList):
        resList = []
        for entry in entryList:
            if len(entry['title'].strip().split(" ")) > 5:
                resList.append(entry)
        return sorted(resList, key=itemgetter('comments')) #Do not know if the sorted should be ascending or descending way. The requirements email says "by the number of comments first." just in case, if the order is descending, add the property reverse=True after the key ... key=itemgetter('comments'), reverse=True)

    # Filter all previous entries with less than or equal to five words in the title ordered by points.
    def filter_ordered_by_points(self, entryList):
        resList = []
        for entry in entryList:
            if len(entry['title'].strip().split(" ")) <= 5:
                resList.append(entry)
        return sorted(resList, key=itemgetter('points')) #the same than the first filter

    def save_csv(self, filteredList, csv_filename):

        keys = filteredList[0].keys() #get the headers for the csv

        with open(csv_filename, 'w') as f:
            dict_writer = csv.DictWriter(f, keys)
            dict_writer.writeheader()
            dict_writer.writerows(filteredList)

def main():
    URL = 'https://news.ycombinator.com/'
    FIRST_FILTER = 'first_filter.csv'
    SECOND_FILTER = 'second_filter.csv'
    # Class Instance
    scraper = Scraper(URL)

    all_entries = scraper.get_all_entries(scraper.entries_titles, scraper.entries_body)
    first_filter = scraper.filter_ordered_by_comments(all_entries)
    second_filter = scraper.filter_ordered_by_points(all_entries)
    
    scraper.save_csv(first_filter, FIRST_FILTER)
    scraper.save_csv(second_filter, SECOND_FILTER)
    print('Filters done!')

if __name__ == '__main__':
    main()