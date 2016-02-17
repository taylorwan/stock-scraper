# imports
from bs4 import BeautifulSoup
from urllib2 import urlopen
import urllib
import requests

# constant
base = 'https://finance.yahoo.com/q/hp?s='


# load beautiful soup
def make_soup(url):
    # html = urlopen(url).read()
    html = requests.get(url)
    return BeautifulSoup(html.text)


# given a ticker, find the url to its historical data
def get_data_link(ticker):
    url = base + ticker
    print url
    soup = make_soup(url)
    for a in soup.find_all('a'):
        if a.text == 'Download to Spreadsheet':
            return a.get('href')
    return -1


# download the file at a particular link
def download_file(url, filename='downloaded.csv'):
    urllib.urlretrieve(url, filename)
    return filename


# given a ticker, load the data into a 2D array
def get_data(ticker):
    # download file
    url = get_data_link(ticker)
    fileName = ticker + '.csv'
    download_file(url, fileName)

    # load data into array
    data = []
    with open(fileName) as f:
        content = f.read()
        for line in content.split('\n'):
            line_data = []
            for cell in line.split(','):
                line_data.append(cell)
            data.append(line_data)
    return data


def print_array(d):
    lenControl = 8
    for r in d:
        output = ''
        for c in r:
            cur = str(c)
            output += cur + '\t'
            # dif = lenControl -
            if len(str(c)) < lenControl:
                output += '\t'
        print output

if __name__ == '__main__':
    data = get_data('AAPL')
    print_array(data)
