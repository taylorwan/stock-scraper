# imports
from bs4 import BeautifulSoup
import urllib
import requests

# constant
base = 'https://finance.yahoo.com/q/hp?s='


# load beautiful soup
def make_soup(url):
    html = requests.get(url)
    return BeautifulSoup(html.text)


# given a ticker, find the url to its historical data
def get_data_link(ticker):
    url = base + ticker
    soup = make_soup(url)
    for a in soup.find_all('a'):
        if a.text == 'Download to Spreadsheet':
            return a.get('href')
    raise Exception("Invalid Ticker")


# download the file at a particular link
def download_file(url, filename='downloaded.csv'):
    urllib.urlretrieve(url, filename)
    return filename


# given a ticker, load the data into a 2D array
def get_data(ticker):

    # try and get a link for ticker
    try:
        url = get_data_link(ticker)
    except Exception as e:
        print e.args[0]
        return -1

    # download file
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


# helper for aligning columns
def pretty_print(s, lenControl):
    if len(str(s)) < lenControl:
        return str(s) + '\t\t'
    return str(s) + '\t'


# print the array, with variable tab width
def print_array(d, lenControl=8):
    output = ''
    for r in d:
        if r == '':
            continue
        for c in r:
            output += pretty_print(c, lenControl)
        output += '\n'
    print output


if __name__ == '__main__':
    data = get_data('AAPL')
    print_array(data)
