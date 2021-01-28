import requests
from bs4 import BeautifulSoup
import urllib.parse
import os
import csv
import numpy


def myCrawler(url, max_pages, save, threads):

    if save == 0:  # if the user requested to restart the crawler and delete all the previous data
        for f in os.listdir(".\\files\\"):  # delete all the txt files
            if not f.endswith(".txt"):
                continue
            os.remove(os.path.join(".\\files\\", f))

    page_num = 0  # number of pages we have visited
    urls = [url]  # urls saves all the urls found
    visited = [url]   # visited contains all the already visited urls, so we dont have to visit them again
    while page_num <= max_pages:
        res = requests.get(urls[page_num])
        html_page = res.content
        soup = BeautifulSoup(html_page, 'html.parser')  # create a new bs4 object from the html data loaded
        soup.encode("utf-8")
        for script in soup(["script"]):  # extract only the text from the html file
            script.extract()
        text = soup.get_text()

        # finds other urls in the current page
        for link in soup.findAll('a', href=True): # finds the contents of the tags <a> that have an url
            link['href'] = urllib.parse.urljoin(urls[0], link['href'])
            if link['href'] not in visited:  # if the link is not in visited appends it to urls and visited
                if '.pdf' not in link['href'] and '.jpg' not in link['href']:  # makes sure no jpg or pdfs pass
                    urls.append(link['href'])
                    visited.append(link['href'])

        title = soup.title.string  # get the title of the current page.
        title = title.replace("\n", "")  # removing all the unnecessary things from the title
        title = title.replace("\r", "")
        title = title.replace("\t", "")
        title = title.replace("|", "")
        title = title.replace(":", "")
        title = title.strip(' ')

        # creates a txt file with the name of the page
        file = open(".\\files\\" + title + ".txt", "w", encoding='utf-8')
        file.write(text)                                 # and saves the text.
        page_num = page_num + 1  # increase the number of pages we have visited.


def myInvertedIndexer():
    list = []
    num = 0
    columns = ['word', 'document', 'frequency']
    # getting each word from each file
    # creating a csv file to save the data
    with open('.\\indexer\\indexer.csv', 'w', newline='', encoding='utf-8') as csv_file:

        for file in os.listdir(".\\files\\"):  # for each txt file created by crawler
            if not file.endswith(".txt"):
                continue
                # reading each line
            with open(".\\files\\" + file, 'r',  encoding='utf-8') as f:
                for line in f:
                    # reading each word
                    for word in line.split():
                        punc = '''!()|-[]{};:'", <>./?@#$%^&*_~©®™¨¨«»'''
                        if word in punc:
                            continue
                        flag = 0
                        for index, array in enumerate(list):
                            if word in array[0] and str(file) == str(array[1]):
                                list[index][2] = int(list[index][2]) + 1
                                flag = 1
                        if flag == 0:
                            list.append(numpy.array([str(word), str(file), 1]))
                        else:
                            continue
        # sorting the csv in alphabetic order by the 'word' value
        list.sort(key=get_word)
        # print(numpy.array(list).tolist())
        # calculating the number of documents that each word appears in.
        count = []
        frequency = 0
        previous_word = list[0][0]
        print(previous_word)
        for array in list:
            current_word = array[0]
            if current_word == previous_word:
                frequency = frequency + 1
                previous_word = current_word
            else:
                count.append([previous_word, frequency])
                frequency = 1
                previous_word = current_word
    # creating a csv file to save the data
    with open('.\\indexer\\indexer.csv', 'w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['word', 'documents', 'data']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        temp = []
        for data in count:
            temp.clear()
            for array in list:
                if array[0] == data[0]:
                    temp.append([str(array[1]), int(array[2])])
            writer.writerow({'word': data[0], 'documents': data[1], 'data': temp})


def get_word(array):
    return array[0]


# os.mkdir(".\\files")
url = "auth.gr"  # url
pages = 5  # number of pages to iterate
save = 0  # keep last data or delete it (1 = keep, 0 = delete)
threads = 8  # number of threads (not using it)
if not url.startswith("http"):
    url = "http://" + url
# myCrawler(url, pages, save, threads)
myInvertedIndexer()