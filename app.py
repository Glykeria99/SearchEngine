from flask import Flask, render_template, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_bootstrap import Bootstrap
import indexer
import crawler
import queue
import threading
import os
import queryprocessor

app = Flask(__name__)

if __name__ == '__main__':
    app.run(use_reloader=False,debug=True)
# os.mkdir(".\\files")
url = "https://www.auth.gr/" # url
links_to_crawl = queue.Queue()
url_lock = threading.Lock()
links_to_crawl.put(url)
crawler_threads = []


pages = int(input("Give the number of pages to crawl:"))  # number of pages to iterate
save = 0  # keep last data or delete it (1 = keep, 0 = delete)
num_of_threads = int(input("Give the number of threads:"))# number of threads
visited = set()
if save == 0:  # if the user requested to restart the crawler and delete all the previous data
    for f in os.listdir(".\\files\\"):  # delete all the txt files
        if not f.endswith(".txt"):
            continue
        os.remove(os.path.join(".\\files\\", f))
if not url.startswith("http"):
    url = "http://" + url

for i in range(int(num_of_threads)):
    MyCrawler = crawler.Crawler(url, links_to_crawl, visited, pages, save, url_lock)
    MyCrawler.start()
    crawler_threads.append(MyCrawler)
for crawler in crawler_threads:
    crawler.join()
print(f"Total Number of pages visited are {len(visited)} using {num_of_threads} threads")

df_count, num_of_words_in_docs, indexer_copy = indexer.myInvertedIndexer()


import os
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

Bootstrap(app)


class SearchForm(FlaskForm):
    query = StringField('query')
    search = SubmitField('search')

@app.route("/", methods=["GET", "POST"])
def search():
    form = SearchForm()
    if form.is_submitted():
        flash(f'Results for {form.query.data}')
        return redirect(url_for('results', query = form.query.data))
    return render_template('searchBar.html', title='search', form=form)


@app.route("/results/<query>", methods= ["GET", "POST"])
def results(query):
    Q = queryprocessor.queryProcessor()
    query_results = Q.process_query(str(query), pages, df_count, num_of_words_in_docs, indexer_copy)
    # query results contains a list of each document name and its score sorted
    form = SearchForm()
    links = []
    new_links = []
    print(query_results)
    for i in range(len(query_results)):
        links.append(str(query_results[i][0]))
    for i in range(len(links)):
        if links[i].startswith('https'):
            links[i] = links[i].replace(".txt", "")
            new_links.append(str(links[i][:5]) + '//:' + str(links[i][5:]))


    if form.is_submitted():
        flash(f'Results for {form.query.data}')
        return redirect(url_for('results', query = form.query.data))
    return render_template('results.html', form=form, len = len(new_links), Results=new_links, query=query)

