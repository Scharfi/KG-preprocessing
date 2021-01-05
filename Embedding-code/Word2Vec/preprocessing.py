#!/usr/bin/env python
# -*- coding: utf-8 -*-

# script to preprocess corpora for training
#
# @author: Andreas Mueller
# @see: Bachelor Thesis 'Analyse von Wort-Vektoren deutscher Textkorpora'
#
# Contributors:
#  Michael Egger <michael.egger@tsn.at>
#
# @example: python preprocessing.py test.raw test.corpus -psub

import gensim
import nltk.data
from nltk.corpus import stopwords
import argparse
import os
import re
import logging
import sys
import multiprocessing as mp
import queue
from multiprocessing.managers import BaseManager


# configuration
parser = argparse.ArgumentParser(description='Script for preprocessing public corpora')
parser.add_argument('raw', type=str, help='source file with raw data for corpus creation')
parser.add_argument('target', type=str, help='target file name to store corpus in')
parser.add_argument('-p', '--punctuation', action='store_true', help='remove punctuation tokens')
parser.add_argument('-s', '--stopwords', action='store_true', help='remove stop word tokens')
parser.add_argument(
    '-u', '--umlauts', action='store_true', help='replace german umlauts with their respective digraphs'
)
parser.add_argument('-b', '--bigram', action='store_true', help='detect and process common bigram phrases')
parser.add_argument('-t', '--threads', type=int, default=mp.cpu_count(), help='thread count')
parser.add_argument('--batch_size', type=int, default=32, help='batch size for multiprocessing')
args = parser.parse_args()
logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
sentence_detector = nltk.data.load('tokenizers/punkt/german.pickle')
punctuation_tokens = ['.', '..', '...', ',', ':', '(', ')', '"', '\'', '[', ']',
                      '{', '}', '?', '!', '-', '–', '+', '*', '--', '\'\'', '``','»','«','®','„','“','|','²','ø','>','<']
punctuation = '?.!/;:()&+%°ø™ ⓘ'


def replace_umlauts(text):
    """
    Replaces german umlauts and sharp s in given text.

    :param text: text as str
    :return: manipulated text as str
    """
    res = text
    """
    ø™ ⓘ
    res = res.replace('ä', 'ae')
    res = res.replace('ö', 'oe')
    res = res.replace('ü', 'ue')
    res = res.replace('Ä', 'Ae')
    res = res.replace('Ö', 'Oe')
    res = res.replace('Ü', 'Ue')
    res = res.replace('ß', 'ss')
    """
    
    res = res.replace('®','')
    res = res.replace('-',' ')
    res = re.sub('\\b[A-Z]+[0-9]+\\b',' ',res)
    res = re.sub('\\b[0-9]+[A-Z]+\\b',' ',res)
    res = re.sub('\\b[A-Z]+\\b','',res)
    res = re.sub('\\b\d+\\b',' ',res)
    res = res.replace(' x ','')
    res = res.replace("ä","\\xc3\\xa4")
    res = res.replace("ö","\\xc3\\xb6")
    res = res.replace("ü","\\xc3\\xbc")
    res = res.replace("Ä","\\xc3\\xa4")
    res = res.replace("Ö","\\xc3\\xb6")
    res = res.replace("Ü","\\xc3\\xbc")
    res = res.replace("ß","\\xc3\\x9f")
    res = res.replace('Õ',"\\xc3\\x95")
    res = res.replace('à',"\\xc3\\x93")
    res = res.replace('â',"\\xc3\\xa1")
    res = res.replace('ç',"\\xc3\\xa7")
    res = res.replace('è',"\\xc3\\xa8")
    res = res.replace('é',"\\xc3\\xa9")
    res = res.replace('ê',"\\xc3\\xaa")
    res = res.replace('ñ',"\\xc3\\xb1")
    res = res.replace('õ',"\\xc3\\xb5")
    #res = res.replace(';','')
    res = res.lower()
    
    return res



def process_line(line):
    """
    Pre processes the given line.

    :param line: line as str
    :return: preprocessed sentence
    """
    stop_words = stopwords.words('german')
    # detect sentences
    sentences = sentence_detector.tokenize(line)
    # process each sentence

    for sentence in sentences:
        # replace umlauts
        if args.punctuation:
            sentence = replace_umlauts(sentence)
        # get word tokens
            words = nltk.word_tokenize(sentence)
        # filter punctuation and stopwords
        
            words = [x for x in words if x not in punctuation_tokens]
            words = [re.sub('[{}]'.format(punctuation), '', x) for x in words]
        
            #words = [x for x in words if x not in stop_words]
        # write one sentence per line in output file, if sentence has more than 1 word
        
        return '{}\n'.format(' '.join(words))

def main():
# get stopwords
    if not args.umlauts:
        stop_words = stopwords.words('german')
    else:
        stop_words = [replace_umlauts(token) for token in stopwords.words('german')]


    with open(args.raw, 'r', encoding="utf-8") as infile:
        # start pre processing with multiple threads
        pool = mp.Pool(args.threads)
        values = pool.imap(process_line, infile, chunksize=args.batch_size)
        print("start-----------------------------")
        with open(args.target, 'w',encoding="utf-8") as outfile:
            for i, s in enumerate(values):
                if i and i % 25000 == 0:
                    logging.info('processed {} sentences'.format(i))
                    outfile.flush()
                if s:
                    outfile.write(s)
            logging.info('preprocessing of {} sentences finished!'.format(i))

# get corpus sentences
class CorpusSentences:
    def __init__(self, filename):
        self.filename = filename

    def __iter__(self):
        for line in open(self.filename):
            yield line.split()

if args.bigram:
    logging.info('train bigram phrase detector')
    bigram = gensim.models.Phrases(CorpusSentences(args.target))
    logging.info('transform corpus to bigram phrases')
    with open('{}.bigram'.format(args.target), 'w') as outfile:
        for tokens in bigram[CorpusSentences(args.target)]:
            outfile.write('{}\n'.format(' '.join(tokens)))


if __name__ == '__main__':
    # freeze_support() here if program needs to be frozen
    main()  # execute this only when run directly, not when imported!