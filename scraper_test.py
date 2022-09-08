import unittest
import scraper

class TestScraper(unittest.TestCase):

    def test_getWebSite(self): #check if the url is given
        URL = 'https://news.ycombinator.com/'
        scra = scraper.Scraper(URL)

        r = scra.getWebSite()
        self.assertIsNotNone(r)
    
    def test_get_entry_head_parsed(self): #check if the entries are inside a list
        testDict = list() 
        URL = 'https://news.ycombinator.com/'
        scra = scraper.Scraper(URL)

        all_entries = scra.get_all_entries(scra.entries_titles, scra.entries_body)
        self.assertEqual(type(testDict), type(all_entries))

    def test_number_of_properties(self): #check if the entries just have the 4 properties (title, rank, comments, points)
        URL = 'https://news.ycombinator.com/'
        scra = scraper.Scraper(URL)

        all_entries = scra.get_all_entries(scra.entries_titles, scra.entries_body)
        self.assertEqual(list(all_entries[0].keys()), ['title', 'rank', 'comments', 'points'])