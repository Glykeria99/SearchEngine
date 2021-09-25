import os
import csv
import numpy
import math


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

        #print("len of idf_values:", len(idf_values))
        return idf_values

    def calculate_query_idf(self,query_count,count,N):
        idf_values = [] #key is each word and the value is the idf value
        for query in query_count:
            for token in count:
                if token[0] == query[0]:
                    idf_values.append([token[0], math.log(N/token[1]+query[1])])


        print("query idf_values:",idf_values)
        return idf_values

    def calculate_count_of_word_in_doc(self,word,doc,indexer_copy):  #finds the count of times a word appears in a certain doc

        for row in indexer_copy:
        # row variable is a list that represents a row in csv
            if row[0] == word: #if it finds the word then must check for the specific doc
                for d in row[2]:
                    if d[0] == doc:
                        return d[1]
        return 0


    def process_query(self,query,N,count,num_of_words_in_docs,indexer_copy):

        #calculate TF-IDF
        idf = self.calculate_idf(count, N)
        tfidf_documents = []
        for doc in num_of_words_in_docs:
            doc_tfidf = []
            for word in idf:
                tf = self.calculate_count_of_word_in_doc(word[0],doc[0],indexer_copy)/doc[1]
                doc_tfidf.append([word[0],doc[0], tf * word[1]])
            tfidf_documents.append(doc_tfidf)
        #print("tfidf_documents: ",tfidf_documents)

        #calculate cosine similarity

        #turn the query into list of words and number of appearance
        query = query.lower()
        query_list = list(query.split(" "))
        query_list.sort(key=get_word)
        query_count = []
        frequency = 0
        previous_word = query_list[0]
        for word in query_list:
            current_word = word
            if current_word == previous_word:
                frequency = frequency + 1
                previous_word = current_word
            else:
                query_count.append([previous_word, frequency])
                frequency = 1
                previous_word = current_word
        query_count.append([previous_word, frequency])

        print("test: ",query_count)

        #vectorize the query by calculating tf-idf
        query_idf = self.calculate_query_idf(query_count,count,N)
        query_tfidf = []
        i = 0
        for word in query_idf:
            query_tf = query_count[i][1]/len(query_list)
            query_tfidf.append([word[0],"query", query_tf * word[1]])
            i = i+1
        print("tf-idf of query:", query_tfidf)

    """  
    def cosine_similarity(self,vector1, vector2):
    dot_product = sum(p*q for p,q in zip(vector1, vector2))
    magnitude = math.sqrt(sum([val**2 for val in vector1])) * 
    math.sqrt(sum([val**2 for val in vector2]))
    if not magnitude:
        return 0
    return dot_product/magnitude
"""




def get_word(array):
    return array[0]



