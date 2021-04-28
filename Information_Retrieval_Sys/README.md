
### How to run
``` 
python3 proj1.py <api key> <search engine> <precsion> <query>
``` 

### External libraries installed
```
pip3 install pandas  
pip3 install sklearn 
pip3 install nltk
python3 -m nltk.downloader stopwords
python3 -m nltk.downloader punkt
pip3 install --upgrade google-api-python-client
```

### Details about project design 

For this project, we have two main components: the search on the query and query expansion to output more accurate results per user feedback. The proj1.py file is used to take the user inputs and call the google API to run the search on the given query. It then taken user feedback on each results to calculate precision of the outputs. If precision is greater than 0 but less than desired, it will call the query expansion portion of the design and pass on the current query, tiltles, snippets, and the indices of the relevant queries. Based on that, the expansion (explained in the next section below) will return an updated query to search for and repeat the process mentioned above until precision is reached. We store all the result and incides for all iterations in two global variables.

For non-html files, we are first checking the 'fileformat' field of the Google search API. For non-html files, the search returns this fileformat key, otherwise it is not present. We manitain and increment a counter if this key is in the search results and subtract this counter from the total (10) when calculating the precision.For html files that are returned wihtout a title or snippet, we print a null and pass along an empty string to the query expansion.  

### A detailed description of query-modification method
The input information including current query, a list of snippets and titles from allresults and also relevant documents indices for all iterations. 
For the query-modification method, our main idea is to use tf-idf scores for each valid word in the documents through all the iterations so far to decide which word to add. We take the mean value of scores for each word through all the relevant documents and pick the two words with highest scores(except existing term in query).  We first decided to use RegexpTokenizer from nltk(https://www.nltk.org/_modules/nltk/tokenize/regexp.html) to tokenize each document because it matches patterns in snippets and titles. Then we clean all the tokens, removing them if they are not alphabet, or only one character or in the stopwords. And then fit our cleaned corpus into the TfidfVectorizer. We used tf-idf Vectorizer from sklearn(https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html) to handle tf-idf measurement through all the documents. And we get the scores matrix and corresponding words from this class. Then choose only rows with relevant document indices(relevant documents from usersâ€™ input) and calculate the mean value of scores for each word through those relevant documents. We picked two words that are not in the current query with the highest mean scores. Finally reorder all the terms(the term in current query and also two new terms) based on their mean scores(in descending order).  
