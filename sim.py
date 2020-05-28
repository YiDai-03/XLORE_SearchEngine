# coding=utf-8
import os
import sys
import jieba.posseg as pseg
import codecs
import logging
from gensim import corpora, models, similarities


def tokenization(text,stopwords):
    result = []
    stop_flag = set(['c', 'd', 'f', 'm', 'p', 'r', 't', 'u', 'uj', 'x'])
   # stop_words_file = 'data/stop_words.txt'
   # stopwords = [x.strip() for x in codecs.open(stop_words_file, 'r', encoding='utf8').readlines()]

    words = pseg.cut(text)
    for word, flag in words:
        if (flag not in stop_flag and flag not in stopwords):
            result.append(word)
    # logging.debug("result length is " % len(result))
    return result

def proc(text,q,stopwords):


    corpus = []
    for sent in text:
        corpus.append(tokenization(sent,stopwords))

  

    dictionary = corpora.Dictionary(corpus)

# logging.info("the dictionary is %s" % ",".join(dictionary))

    doc_vectors = [dictionary.doc2bow(text) for text in corpus]

# logging.debug("doc_vectors is %s" % ",".join(doc_vectors))
    simlarity_tfidf,tfidf_vectors = sim_cal_tfidf(doc_vectors, q,dictionary,stopwords)
    return simlarity_tfidf



def sim_cal_tfidf(doc_vector=None, query='',dictionary=None,stopwords=None):
   # print(doc_vector)
    tfidf = models.TfidfModel(doc_vector)
    tfidf_vectors = tfidf[doc_vector]
    # logging.info("length of vector is :%d" % tfidf_vectors)
    # logging.info("vector[0] is %s" % ",".join(tfidf_vectors[0]))
    query = tokenization(query,stopwords)
    query_bow = dictionary.doc2bow(query)
  #  print(tfidf_vectors)
  #  print(tfidf)

    # logging.info("query_bow is %s" % ",".join(query_bow))
    try:
        index = similarities.MatrixSimilarity(tfidf_vectors)
        sims = index[query_bow]
        return list(enumerate(sims)), tfidf_vectors
    except:
        return list(enumerate([0]*len(doc_vector))),0



