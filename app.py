from flask import Flask, render_template, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_bootstrap import Bootstrap
import queryprocessor

app = Flask(__name__)


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
    form = SearchForm()
    Results = []
    Results.append("selida 1")
    Results.append("selida 2")
    Results.append("selida 3")

    #query = queryprocessor.queryProcessor()
    #query.calculate_cosine_sim("Greek university", self.pages, df_count, num_of_words_in_docs, indexer_copy)

    if form.is_submitted():
        flash(f'Results for {form.query.data}')
        return redirect(url_for('results', query = form.query.data))
    return render_template('results.html', form=form, len = len(Results), Results=Results, query=query)

