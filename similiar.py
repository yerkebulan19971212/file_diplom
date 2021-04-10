from numpy import unicode, asarray, sqrt, log
from numpy.dual import svd
from numpy.ma import zeros
from nltk.stem import SnowballStemmer

stemmer = SnowballStemmer("russian")


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
            print('слово невстерчается')
            return []
        if not idx in self.keys:
            print('слово отброшено как не имеющее значения которое через stopwords')
            return []
        return zip(self.indexes, self.docs)


docs = [
    "Британская полиция знает о местонахождении основателя WikiLeaks",
    "Церемонию вручения Нобелевской премии мира бойкотируют 19 стран",
    "В Великобритании арестован основатель сайта Wikileaks Джулиан Ассандж",
    "Украина игнорирует церемонию вручения Нобелевской премии",
    "Шведский суд отказался рассматривать апелляцию основателя Wikileaks",
    "НАТО и США разработали планы обороны стран Балтии против России",
    "НАТО и США разработали планы обороны стран Балтии против России",
    "Полиция Великобритании нашла основателя WikiLeaks, но, не арестовала",
    "Полиция Великобритании нашла основателя WikiLeaks, но, не арестовала",
    "Полиция Великобритании нашла основателя WikiLeaks, но, не арестовала",
    "В Стокгольме и Осло сегодня состоится вручение Нобелевских премий"
]
ignorechars = ''',:'!'''
word = "Полиция"
lsa = LSI([], ignorechars, docs, word)
# lsa.build()
# lsa.calc()

for res, red in lsa.find():
    print(res, red, docs[res])