import pandas as pd
import nltk
from nltk.tokenize import RegexpTokenizer
import string
from nltk.stem import PorterStemmer 
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
import sys

stop_words_f = open('./stopwords.txt')
stop_words = stop_words_f.read().split('\n')
table = str.maketrans('', '', string.punctuation)
ss = SnowballStemmer("english", ignore_stopwords=True)
tokenizer = RegexpTokenizer(r'\w+|\$[\d\.]+|\S+') 

def query_expansion(current_query, relavent_indices, list_docs):
	
	current_terms = current_query.split()

	# clean documents
	cleaned_corpus = [] 
	for doc in list_docs:
		# word_tokens = nltk.word_tokenize(doc)
		word_tokens = tokenizer.tokenize(doc)
		cleaned_doc = []
		for word in word_tokens:
			word = word.lower()
			# stemming is not good, modify too much on words.
			#word = ss.stem(word) 
			if len(word) > 1 and word.isalpha() and word not in stop_words:
				cleaned_doc.append(word)
		cleaned_corpus.append(' '.join(cleaned_doc))


	# put cleaned corpus into tf-idf model, use onely one-gram
	vectorizer = TfidfVectorizer(ngram_range = (1, 1))
	X = vectorizer.fit_transform(cleaned_corpus)
	# only consider relavent docs 
	X = X[relavent_indices, :] 
	all_scores = pd.DataFrame.sparse.from_spmatrix(X, columns=vectorizer.get_feature_names())

	term_scores = all_scores.mean()  

	# add two new terms based on average tf-idf score 
	added = 0 
	sorted_terms = term_scores.sort_values(ascending=False)

	augmented_terms = [] 
	for term, sc in sorted_terms.items():
		if term not in current_terms and added < 2:
			print("Indexing results...")
			augmented_terms.append(term)
			current_terms.append(term)
			added += 1 
		if added >= 2:
			break
	print("Agumenting by  " + ' '.join(augmented_terms))

	term_maps = sorted_terms.to_dict()

	# reorder terms in the query based on average tf-idf score 
	q_scores = {}
	for term in current_terms:
		if term in term_maps.keys(): 
			q_scores[term] = term_maps[term]
		else:
			q_scores[term] = 0

	# sort term list by tf-idf scores 
	current_terms = sorted(q_scores.keys(), key=lambda item: item[1])

	new_query = " ".join(current_terms) 
	return new_query


