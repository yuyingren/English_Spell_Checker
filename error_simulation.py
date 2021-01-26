

@author: yuyingren
"""

import re
import nltk
from nltk.tokenize.treebank import TreebankWordDetokenizer
import random
import os

### read the text data and process line by line, each line contains at least 1 paragraph 
#   and save them into a list.


texts = []
texts_no_punc = []
texts_tok = []
with open("data1.txt", "r") as d1:
    text = []
    for line in d1:
        text.append(line.rstrip().lstrip())
    for t in text:
        tt = nltk.word_tokenize(t)
        if len(tt) >= 20:
            ttt = TreebankWordDetokenizer().detokenize(tt)
            texts.append(ttt)

print(len(texts))

### read the English word dictionary data

word_list = []
with open("words_alpha.txt", "r") as r:
    for w in r:
        word_list.append(w.strip())
print(len(word_list))

### Functions of simulating errors

def err_insert(tok, char):
    return tok.replace(char[0], char[0] + char[1], 1)

def err_sub(tok, char):
    return tok.replace(char[0], char[1], 1)

def err_del(tok, char):
    return tok.replace(char[0], "", 1)

err_functions = [err_insert, err_sub, err_del]

### randomly apply one of the error simulation functions to the word selected from original texts.

def apply_err(tok, char):
    f = random.choice(err_functions)
    return f(tok, char)

### create error words

def create_error(tok):
    cor_err = []

    cor_err.append(tok)

    char = random.choices(tok, k = 2)

    error = apply_err(tok, char)
   

    if error == tok:
        error = apply_err(tok, char)
    
        
    cor_err.append(error)

    return cor_err


### select words from the original texts, and replace them with error words. And create an 
#   answer sheet: the original word, the error and the index of them in the text. 
    
answers = []

for x in texts:

    txt = nltk.word_tokenize(x)

    candi = []
    aswr = []
    

    for i, t in enumerate(txt):

        if any(char.isupper() for char in t):
            continue

        if any(char.isdigit() for char in t):
            continue

        if len(t) >= 3:
            can = tuple([t, i])
            candi.append(can)
    candid = candi[::10]

    for ca in candid:
        pair = creat_error(ca[0])
        pair.append(ca[1])
        aswr.append(tuple(pair))
    for an in reversed(aswr):

        if an[1] in word_list:

            aswr.remove(an)
    answers.append(aswr)
print(len(answers))


### create text files for each line of the text file.

files = []
for i in range(1, len(texts) + 1):
    it = "text_" + str(i) + ".txt"
    files.append(it)    

empty_an = []
for i, an in enumerate(answers):
    if an == []:
        empty_an.append(i)
    

files2 = []

for j, f in enumerate(files):
    if j in empty_an:
        files2.append(f)


files1 = []
for f in files:
    if f not in files2:
        files1.append(f)


file_names = []

aff = "texts"
for f in files1:

    x = os.path.join(aff, f)
    file_names.append(x)


print(len(file_names))

### For each file, save the original text, the error text, and the answer sheet.

for i in range(0, len(file_names)):
    read_file = open(file_names[i], "r")

    for rr in read_file:
        toks = nltk.word_tokenize(rr)
    read_file.close()

    for a in answers[i]:
        for n, t in enumerate(toks):
            if a[2] == n:
                toks[n] = a[1]
                break
    tx = TreebankWordDetokenizer().detokenize(toks)
    write_file = open(file_names[i], "a")
    print(tx, file = write_file)
    print(answers[i], file = write_file)
    write_file.close()
print("ok")