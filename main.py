import indexer
import crawler

# os.mkdir(".\\files")
url = "auth.gr"  # url
pages = 5  # number of pages to iterate
save = 0  # keep last data or delete it (1 = keep, 0 = delete)
threads = 8  # number of threads (not using it)
if not url.startswith("http"):
    url = "http://" + url
MyCrawler = crawler.Crawler
MyCrawler.myCrawler(url, pages, save, threads)
indexer = indexer.myInvertedIndexer()
