from django.shortcuts import render
import base64
import docx
import pdfplumber
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from numpy import unicode, asarray, sqrt, log
from numpy.dual import svd
import nltk.data

import time
from numpy.ma import zeros
from nltk.stem import SnowballStemmer


stemmer = SnowballStemmer("russian")

import nltk.data
nltk.download('punkt')
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

class LSI(object):

    def __init__(self, stopwords, ignorechars, docs, find):
        self.wdict = {}
        self.dictionary = []
        self.stopwords = stopwords
        if type(ignorechars) == unicode: ignorechars = ignorechars.encode('utf-8')
        self.ignorechars = ignorechars
        self.docs = []
        self.indexes = []
        self.find_word = self.dic(find.lower().strip(), True)
        for index, doc in enumerate(docs):
            self.add_doc(index, doc)

    def prepare(self):
        self.build()

    def dic(self, word, add=False):
        if type(word) == unicode: word = word.encode('utf-8')
        word = word.lower().translate(None, self.ignorechars)
        word = word.decode('utf-8')
        word = stemmer.stem(word)
        if word in self.dictionary:
            return self.dictionary.index(word)
        else:
            if add:
                self.dictionary.append(word)
                return len(self.dictionary) - 1
            else:
                return None

    def add_doc(self,i, doc):
        words = [self.dic(word, True) for word in doc.lower().split()]
        if self.find_word in words:
            self.docs.append(words)
            self.indexes.append(i)
            for word in words:
                if word in self.stopwords:
                    continue
                elif word in self.wdict:
                    self.wdict[word].append(len(self.docs) - 1)
                else:
                    self.wdict[word] = [len(self.docs) - 1]

    def build(self):
        self.keys = [k for k in self.wdict.keys() if len(self.wdict[k]) > 0]
        self.keys.sort()
        self.A = zeros([len(self.keys), len(self.docs)])
        for i, k in enumerate(self.keys):
            for d in self.wdict[k]:
                self.A[i, d] += 1

    def TFIDF(self):
        wordsPerDoc = sum(self.A, axis=0)
        docsPerWord = sum(asarray(self.A > 0, 'i'), axis=1)
        rows, cols = self.A.shape
        for i in range(rows):
            for j in range(cols):
                self.A[i, j] = (self.A[i, j] / wordsPerDoc[j]) * log(float(cols) / docsPerWord[i])

    def find(self):
        self.prepare()
        idx = self.find_word
        if idx < 0:
            # print('слово невстерчается')
            return []
        if not idx in self.keys:
            # print('слово отброшено как не имеющее значения которое через stopwords')
            return []
        return zip(self.indexes, self.docs)


class sdfk(CreateAPIView):
    def post(self, request, *args, **kwargs):
        t0 = time.time()

        pdf_list = [{
                "name": "Name",
                "count": 17,
                "sentences": [
                    {"page": 1, "text": "Texxt1"},
                    {"page": 2, "text": "Texxt2"},
                    {"page": 3, "text": "Texxt3"}
                ]
            }]
        files = request.POST.getlist('title')
        keys = request.POST.get('key').split(" ")
        files_list = [i.split(',') for i in files]
        ignorechars = ''',:'!'''

        for index, file in enumerate(files_list, start=1):
            if "pdf" in file[2]:

                file_text = str(file[0])
                decoded_file_text = base64.b64decode(file_text)
                filename = 'file_pdf_' + str(index)
                with open(filename, 'wb') as pdf:
                    pdf.write(decoded_file_text)
                with pdfplumber.open(r'{}'.format(filename)) as pdf:
                    sdfp = []
                    for k, j in enumerate(pdf.pages):
                        pages_text = tokenizer.tokenize(j.extract_text())
                        sentenses = []
                        for key in keys:
                            lsa = LSI([], ignorechars, pages_text, key)
                            for res, red in lsa.find():

                                # print(res, pages_text[res].strip().rstrip("\n"))
                                sentenses.append({
                                    "page": k,
                                    "text": pages_text[res]
                                })
                        if sentenses:
                            pdf_list.append({
                                "name": file[1],
                                "count": 1,
                                "sentences": sentenses
                            })
            else:
                file_text = str(file[0])
                decoded_file_text = base64.b64decode(file_text)
                filename = 'file_doc' + str(index)  # + ".docx"
                with open(filename, 'wb') as pdf:
                    pdf.write(decoded_file_text)
                doc = docx.Document(filename)
                for k, j in enumerate(doc.paragraphs):
                    pages_text = tokenizer.tokenize(j.text)
                    sentenses = []
                    for key in keys:
                        lsa = LSI([], ignorechars, pages_text, key)
                        for res, red in lsa.find():
                            # print(res, pages_text[res].strip().rstrip("\n"))
                            sentenses.append({
                                "page": k,
                                "text": pages_text[res]
                            })
                    if sentenses:
                        pdf_list.append({
                            "name": file[1],
                            "count": 1,
                            "sentences": sentenses
                        })
        # print(pdf_list)
        # print(len(pdf_list))
        t1 = time.time()
        print(t1-t0)
        return Response({"status": True, "message": "some text", "list": pdf_list})
