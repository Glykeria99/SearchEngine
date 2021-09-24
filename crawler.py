import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import threading


class Crawler(threading.Thread):

    def __init__(self, url, links_to_crawl, visited, max_pages, save, url_lock):
        threading.Thread.__init__(self)
        print(f"Web Crawler worker {threading.current_thread()} has Started")
        self.max_pages = max_pages
        self.save = save
        self.url = url
        self.links_to_crawl = links_to_crawl
        self.visited = visited
        self.url_lock = url_lock

    def run(self):

        while True:
            # In this part of the code we create a global lock on our queue of
            # links so that no two threads can access the queue at same time
            self.url_lock.acquire()
            link = self.links_to_crawl.get()
            self.url_lock.release()

            # if the link is None the queue is exhausted or the threads are yet
            # process the links.

            if link is None:
                break

            # if The link is already visited we break the execution.
            if link in self.visited:
                break

            try:
                # This method constructs a full "absolute" URL by combining the
                # base url with other url. this uses components of the base URL,
                # in particular the addressing scheme, the network
                # location and  the path, to provide missing components
                # in the relative URL.
                # in short we repair our relative url if it is broken.
                link = urljoin(self.url, link)

                res = requests.get(link)
                html_page = res.content
                if len(self.visited) >= self.max_pages:
                    break
                # this returns the html representation of the webpage
                soup = BeautifulSoup(html_page, "html.parser")

                # in this case we are finding all the links in the page.
                for a_tag in soup.find_all('a'):
                    # we are checking of the link is already visited and (network location part) is our
                    # base url itself.
                    if (a_tag.get("href") not in self.visited):
                        self.links_to_crawl.put(a_tag.get("href"))


                print(f"Adding {link} to the crawled list")
                self.visited.add(link)
                text = soup.get_text()

                title = link  # get the title of the current page.
                title = title.replace("\n", "")  # removing all the unnecessary things from the title
                title = title.replace("\r", "")
                title = title.replace("\t", "")
                title = title.replace("|", "")
                title = title.replace(":", "")
                title = title.replace("/", "")
                title = title.strip(' ')
                print(title)
                # creates a txt file with the name of the page
                file = open(".\\files\\" + title + ".txt", "w", encoding='utf-8')
                file.write(text)  # and saves the text.
                if len(self.visited) > self.max_pages:
                    break
            finally:
                self.links_to_crawl.task_done()

