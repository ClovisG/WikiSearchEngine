from itertools import chain
from collections import defaultdict
import numpy
import pickle
import sys
import copy

with open("doctok.dict",'rb') as f:
	doctok = pickle.load(f)

with open("pageRank.dict",'rb') as f:
	pageRankDict = pickle.load(f)


docList = doctok.keys()
Ndocs = len(docList)


tokInfo = defaultdict(float)
tf = dict()
for doc in doctok:
	tf[doc] = defaultdict(float)
	for tok in doctok[doc]:
		tf[doc][tok] += 1
	for tok in set(doctok[doc]):
		tokInfo[tok] += 1 # for now only store the counts

for doc in tf:
	Ntok = sum(tf[doc].values())
	for tok in tf[doc]:
		tf[doc][tok] /= Ntok

for tok in tokInfo.keys():
	tokInfo[tok] = -numpy.log(tokInfo[tok]/Ndocs)

print("done.")

print("transposing...",end="")
tfidf = defaultdict(dict)
for doc in tf:
	for tok in tf[doc]:
		tfidf[tok][doc] = tf[doc][tok]*tokInfo[tok]
print("done.")



print("normalizing...",end="")
tfidfNorm = copy.deepcopy(tfidf)
norm = defaultdict(float)
for tok in tfidf:
	for doc in tfidf[tok]:
		norm[doc] += tfidf[tok].get(doc,0)**2.0
		
for tok in tfidf:
	for doc in tfidf[tok]:
		tfidfNorm[tok][doc] = tfidf[tok][doc]/numpy.sqrt(norm[doc])
print("done.")



def scal(query,doc,tfidf):
	s = float()
	for tok in query:
		s += tfidf[tok].get(doc,0)*tokInfo[tok]
	return s

def scalNorm(query,doc,tfidf):
	s = float()
	for tok in query:
		s += tfidfNorm[tok].get(doc,0)*tokInfo[tok]
	return s

# Ranked by token relevance (vector model)
def getBestResultsNormed(queryStr, topN):
	query = queryStr.split(" ")
	res = defaultdict(float)
	for tok in query:
		for doc in tfidfNorm[tok]:
			res[doc] += tfidfNorm[tok].get(doc,0)*tokInfo[tok]
	return sorted(res, key=res.get,reverse=True)[0:topN]



# Ranked by token relevance (vector model)
def getBestResults(queryStr, topN):
	query = queryStr.split(" ")
	res = defaultdict(float)
	for tok in query:
		for doc in tfidf[tok]:
			res[doc] += tfidf[tok].get(doc,0)*tokInfo[tok]
	return sorted(res, key=res.get,reverse=True)[0:topN]

def rankResults(results):
	ranks = [ pageRankDict.get(page,0) for page in results ]
	rankedResults = list(reversed([ results[i] for i in numpy.argsort(ranks) ]))
	return rankedResults


def printResults(rankedResults):
	for idx,page in enumerate(rankedResults):
		print(str(idx) + ". " + page)


#queryStr = sys.argv[1]
query = "evolution of bacteria"
top = 15
results = getBestResults(query,top)
printResults(results)


results = getBestResultsNormed(query,top)
printResults(results)

rankedResults = rankResults(results)
printResults(rankedResults)

#bestPageSimilarity = list(reversed([ searchRes[i] for i in numpy.argsort(searchRes)[-10:] ]))
#bestPageSimilarity


