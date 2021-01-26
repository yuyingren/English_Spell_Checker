

@author: yuyingren
"""

import os
import ast
import re
import nltk

def error_detect(errtxt):

    ''''Tokenize the error words in the text. Ignore words that are not in 
    the dictionary such as punctuations, uppercased words(like names), and 
    digits. Return all the words aren't found in the dictionary, including 
    the simulated real word errors and out of vocabulary words(such as foreign
    words).'''
    
    res = re.sub(r'[^\w\s]', '', errtxt)
    res_tok = nltk.word_tokenize(res)
    detected_errs = []
    oov = []
    for rr in res_tok:
        
        if any(char.isupper() for char in rr):
            continue
        if any(char.isdigit() for char in rr):
            continue
        if rr not in word_list:
            detected_errs.append(rr)
            
    for w in detected_errs:
        if w not in errors:
            oov.append(w)
    return detected_errs, oov



def mini_edistance(er, cr):

    '''Calculate the minimum edit distance of the input two words: the er->error
    and the cr->candidate words selected to compare with the error.'''
    rows = len(er)+1
    cols = len(cr)+1
    mtrx = [[0 for x in range(cols)] for x in range(rows)]

    for i in range(1, rows):
        mtrx[i][0] = i


    for i in range(1, cols):
        mtrx[0][i] = i
        
    for col in range(1, cols):
        for row in range(1, rows):
            if er[row-1] == cr[col-1]:
                cost = 0
            else:
                cost = 1
            mtrx[row][col] = min(mtrx[row-1][col] + 1,     
                                 mtrx[row][col-1] + 1,  
                                 mtrx[row-1][col-1] + cost)
    
    return mtrx[row][col]

 
def candidates_selection(detec_err):

    '''To reduce the calculation, two steps to choose the candidates: first,
    select the words from the dictionary that have similar length with the error, 
    since the errors are simualted by only one of the operations: insertion, 
    deletion, substitution. Second, select words(from step1) that only have 1 
    minimum edit distance from the error.
    detec_err -> "errors" list contains all the simulated errors that generated
    by the main function below.'''
    candidates1 = [] #list of candidates from step1 
    candidates2 = [] #list of candidates from step2
    
    for e in detec_err:
        s = len(e) - 1
        m = len(e) + 1
        cans = []
        for w in word_list:
            if len(w) >= s and len(w) <= m:
                cans.append(w)
        candidates1.append(cans)

        candi = []
        for w1 in candidates1:
            for ww in w1:
            
                dis = mini_edistance(e, ww)
                if dis <= 1 and ww not in candi:
                    candi.append(ww)
        candidates2.append(candi)
    return candidates2



def get_context(lst, txt):

    '''Find the errors' context words. bigrams(left context word and right context
     word) and trigrams(both left and right context words) are extracted.
    lst -> the answers list of original correct words, errors simulated
    from the words and their index in the text. 
    txt-> the text containing errors.'''
    err_tx_lst = nltk.word_tokenize(txt.lower())
    cntxt_tri = []
    cntxt_l = []
    cntxt_r = []
    
    for an in lst:

        for i, w in enumerate(err_tx_lst):
            if an[2] == i:
                l_gram = tuple([err_tx_lst[i-1], w])

                r_gram = tuple([w, err_tx_lst[i+1]])

                tri_gram = tuple([err_tx_lst[i-1], w, err_tx_lst[i+1]])

        cntxt_l.append(l_gram)
        cntxt_r.append(r_gram)
        cntxt_tri.append(tri_gram)
    
    return cntxt_l, cntxt_r, cntxt_tri

def get_candid_cntxt(lst1, lst2):

    '''Replacing the error words in the bigram/trigram context with their 
    candidates that seleted in candidates_selection function.
    lst1 -> candidates list generated in candidates_selection; 
    lst2->error contexts list generated in get_context function(could be left 
    contexts, right contexts, or tri contexts)'''
    
    candi_ctx = []

    
    for can in reversed(lst1):
        
        
        ### For left contexts
#         for lg in reversed(lst2):
#             lst3 = []
#             if can != []:
#                 for w in can:
#                     nw_lg = tuple([lg[0], w])
#                     lst3.append(nw_lg)
#             if can == []:
#                 nw_lg = tuple(["_", lg[1], "_"])
#                 lst3.append(nw_lg)
#             lst2.pop()
#             break

        ### For right contexts
#         for rg in reversed(lst2):
#             lst3 = []
#             if can != []:
#                 for w in can:
#                     nw_rg = tuple([w, rg[1]])
#                     lst3.append(nw_rg)
#             if can == []:
#                 nw_rg = tuple(["_", rg[0], "_"])
#                 lst3.append(nw_rg)
#             lst2.pop()
#             break

        ### for trigram contexts  
        for tri in reversed(lst2):
            lst3 = []
            if can != []:
                for w in can:

                    nw_tri = tuple([tri[0], w, tri[2]])
                    lst3.append(nw_tri)
            if can == []:
                nw_tri = tuple(["_", tri[1], "_"])
                lst3.append(nw_tri)

            lst2.pop()

            break

        lst1.pop()

        candi_ctx.append(lst3)

    
    return candi_ctx

def get_results(lst,cnt_dict):

    '''For each error, search their candidates contexts grams in the bi/tri gram
    corpus. if there are multiple candidates with contexts are found, the system
    will select the one with the highest frequency in the bi/tri gram corpus.
    lst -> list of candidtes with contexts of the errors.
    cnt_dict -> the bi/tri gram corpus: grams are extracted from the data, and 
    frequencies are calculated.'''
    slct_w = []
    pred_w = []
    
    
    for ctxt in lst:
        frq = []
        cn_w = []
        for i in ctxt:
            if i in cnt_dict:
                frq.append(cnt_dict.get(i))
                cn_w.append(i[1])
            if i not in cnt_dict:
                frq.append(0)
                cn_w.append(i[1])
            
        w_frq = dict(zip(cn_w, frq))

        
        slct_w.append(w_frq)
    
    for d in slct_w:
        if len(d) <= 1:
            for k, v in d.items():
                
                pred_w.append(k)

        if len(d) > 1:
            pred_w.append(max(d, key = d.get))
        


    result_s = [i for i in reversed(slct_w)]
    result_w = [i for i in reversed(pred_w)]
    result_p = list(zip(corrections, result_w))

    return result_s, result_w, result_p


### Get the files of texts

files = os.listdir('texts')
print(len(files))
file_names = []
for f in files:
    if f.startswith("text_"):
        f1 = os.path.join("texts", f)
        file_names.append(f1)


print(len(file_names))

### organize the files into descending order

def get_digits(text):
    return int(text) if text.isdigit() else text
def _keys(text):
    return [  get_digits(c) for c in re.split(r'(\d+)', text) ]

file_names.sort(key = _keys)

test = file_names[:20]

### read the dictionary file

word_list = []
with open("words_alpha.txt", "r") as r:
    for w in r:
        word_list.append(w.strip())
print(len(word_list))


### read the trigram_frequency file:

tri_g = []
tri_g_frequency = []
with open("tri_freq.txt", 'r') as tg:
    

    for line in tg:
        
        grams, pro = line.rstrip().split("\t")
        tri_g.append(tuple(grams.split(" ")))
        tri_g_frequency.append(float(pro))

tri_dict = dict(zip(tri_g, tri_g_frequency))
print(len(tri_dict))

### Test the system with the first 20 files

for file in test:
    with open(file, "r") as r:
        content = r.readlines()
        orgn_tx = content[0]
        err_tx = content[1]
        answers = ast.literal_eval(content[2])
    errors = [ew[1] for ew in answers]
    corrections = [cw[0] for cw in answers]
    errors_found = error_detect(answers, err_tx)[0]
    candidates = candidates_selection(errors)
    err_contxt_left = get_context(answers, err_tx)[0]
    err_contxt_right = get_context(answers, err_tx)[1]
    err_contxt_tri = get_context(answers, err_tx)[2]
    candid_contxt = get_candid_cntxt(candidates, err_contxt_tri)
    results = get_results(candid_contxt,tri_dict)[2]
        
    with open(file, "a") as f:
        print(str(errors_found) + "\n" + str(results), file = f)

print("ok")