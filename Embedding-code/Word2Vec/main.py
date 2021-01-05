import codecs
import gensim
import pandas as pd
import re
from operator import add


vocabulary=[]
vocab_word=""
vocabfile = open("vocab.txt", "r", encoding="utf-8")
for vline in vocabfile:
    vocab_word= vline.strip()
    vocab_word= vocab_word.replace("\n","")
    vocabulary.append(vocab_word)
    vocab_word=""


# Data import and post-process
matrix=[]
words=[]
data=[]
res=""

f = open('products_V02allc.uml', 'r', encoding="utf-8")
for line in f:
    words = list(dict.fromkeys(line.split()))
    
    for mot in words:
        res = mot
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
        res = re.sub('\\b[0-9]+\\b','',res)
        res = re.sub('\\b[a-z]\\b','',res)
   
        data.append(res)
        res=""
       
    matrix.append(data)
    data=[] 

model = gensim.models.KeyedVectors.load_word2vec_format("Model/vectors.w2vformat.txt", binary=False )

out = open("outofvocab.txt","a", encoding="utf-8")
embedding = open("embeddings.csv","a", encoding="utf-8")

words_vec=[]
products=[]
emb_vec=[0]*300
emb=[]
check=0
id=""
i=0
j=0
fline=""
print(" generate embeddings")
for row in matrix:
    for w in row:
        if w in vocabulary:
            wf = "b'" + w +"'"
            try:
                if w !="\\xc3\\xb6":
                    emb = model[wf]
                    emb_vec = list(map(add, emb_vec, emb))
                    check=1
            except:
                pass
        else:
            fline= format(w) +", "
            out.write(fline)
        emb=[]
        wf=""

    if check==1:
        id = format(i)+","
        embedding.write(id)
        embedding.write(",".join(str(item) for item in emb_vec))
        embedding.write("\n")
        i+=1
    else:
        products.append(i)
        id = format(i)+","
        embedding.write(id)
        embedding.write(",".join(str(item) for item in emb_vec))
        embedding.write("\n")
        i+=1
    emb_vec=[0]*300
    check=0
    id=""
    out.write("\n")

print(products)