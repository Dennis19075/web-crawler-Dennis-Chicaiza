
# Web crawler by Dennis Chicaiza A

A web crawler using scraping techniques to extract entries from https://news.ycombinator.com/

## Requirements

Using the language that you feel most proficient in, you’ll have to create a web crawler using scraping techniques to extract the first 30 entries from https://news.ycombinator.com/ . You’ll only care about the title, the number of the order, the number of comments, and points for each entry.

From there, we want it to be able to perform a couple of filtering operations:
- Filter all previous entries with more than five words in the title ordered by the number of comments first.
- Filter all previous entries with less than or equal to five words in the title ordered by points.

## Required libraries
```bash
pip3 install requests-html
```

## Run the script to generate the entries list as CSV files
```bash
python3 scraper.py
```

When the script is done, 2 csv files will be generated with the names of "**first_filter.csv**" and "**second_filter.csv**" getting the data filtered as proposed requirements

## Run the test script to check some unit tests
```bash
python3 -m unittest scraper_test.py 
```

### Unit test list:
- Check if the url is given (***test_getWebSite***)
- Check if the entries are inside a list (***test_get_entry_head_parsed***)
- Check if the entries just have the 4 properties (title, rank, comments, points) (***test_number_of_properties***)
