import os
import csv
import numpy
import math
from csv import reader

"""
t — term (word)
d — document (set of words)
N — count of corpus
corpus — the total document set

DF = count of t in documents
TF= count of t in d / number of words in d
IDF(t) = log(N/DF)
TF-IDF = tf*idf

"""

class queryProcessor:

    def __init__(self):
        pass

    def calculate_idf(self,count, N):
        idf_values = [] #key is each word and the value is the idf value
        for token in count:
            idf_values.append([token[0], math.log(N/token[1])])

        print("len of idf_values:", len(idf_values))
        return idf_values

    def calculate_count_of_word_in_doc(self,word,doc,indexer_copy):  #finds the count of times a word appears in a certain doc

        for row in indexer_copy:
            print("row: ",row) #SOMETHING WRONG WITH THE INDEXER VALUES?????
        # row variable is a list that represents a row in csv
            if row[0] == word: #if it finds the word then must check for the specific doc
                for d in row[2]:
                    if d[0] == doc:
                        return d[1]






        """
        for row in indexer:
            print("row 0 is: ", row[0])
            temp = row[2]
            if word == row[0]:
                for d in temp:
                    if doc == d[0]:
                        print("doc is: ", doc, "and in index i found same: ", d[0])
                        return d[1]
                        """




    def calculate_tf_idf(self,N,count,num_of_words_in_docs,indexer_copy):
        idf = self.calculate_idf(count, N)
        tfidf_documents = []
        for doc in num_of_words_in_docs:
            doc_tfidf = []
            for word in idf:
                tf = self.calculate_count_of_word_in_doc(word[0],doc[0],indexer_copy)/doc[1]
                doc_tfidf.append(tf * idf[word])
            tfidf_documents.append(doc_tfidf)
        return tfidf_documents
