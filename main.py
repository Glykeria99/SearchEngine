import indexer
import crawler
import queryprocessor

# os.mkdir(".\\files")
url = "auth.gr"  # url
pages = 5  # number of pages to iterate
save = 0  # keep last data or delete it (1 = keep, 0 = delete)
threads = 8  # number of threads (not using it)
if not url.startswith("http"):
    url = "http://" + url
MyCrawler = crawler.Crawler
MyCrawler.myCrawler(url, pages, save, threads)

df_count, num_of_words_in_docs, indexer_copy = indexer.myInvertedIndexer()
query = queryprocessor.queryProcessor()
query.calculate_cosine_sim("Greek university", pages, df_count, num_of_words_in_docs, indexer_copy)


