from autocorrect import Speller
import time
#
spell = Speller(lang='ru')
# t0 = time.time()
# print(spell('орфаграфит'))
# print(spell('одтн'))
# print(spell('провурк'))
# print(spell('отрфтом'))
# t1 = time.time()
# total = t1-t0
# print(total)

import nltk.data
nltk.download('punkt')

text = "Следующим проверяется значение 4. Так как оно меньше семи, мы должны перенести его на правильную позицию в отсортированную часть массива. Остается вопрос: как ее определить? Это осуществляется методом FindInsertionIndex. Он сравнивает переданное ему значение (4) с каждым значением в отсортированной части, пока не найдет место для вставки."
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
data = text
print('\n-----\n'.join(tokenizer.tokenize(data)))