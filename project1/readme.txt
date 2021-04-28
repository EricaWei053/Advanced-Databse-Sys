Erica Wei (cw3137)
Ishraq Khandaker (ibk2110)

List of files submitted
- proj1.py
--- driver file for the project, takes user inputs, calls google search api to run query, call query_expansion based on precision calculations
- query_expansion.py
--- takes query and snippets from proj1.py, runs algorithm and returns the augmented query to proj1.py
- stopwords.txt
--- list of stop words used to generate the augmented query in query_expansion.py
- transcript.txt
--- contains result of the test cases
- README.txt

A clear description of how to run your program. Note that your project must compile/run in a Google Cloud VM that you set up exactly following our instructions. 
Provide all commands necessary to install the required software and dependencies for your program.
- to run the program
--- from proj1 directory, run the following: python3 proj1.py <api key> <search engine> <precsion> <query>

- External libraries installed
--- pip3 install pandas 
------ used to manipulate data after tf-idf vectorizer
--- pip3 install sklearn 
------to use tf-idf vectorizer for handling tf-idf measurements 
--- pip3 install nltk
------to use RegexpTokenizer to tokenize each document
--- python3 -m nltk.downloader stopwords
------used to identify stopwords, which do not add much meaning to a sentence
--- python3 -m nltk.downloader punkt
------Used to divide text into a list of sentences by using an unsupervised algorithm to build a model for abbreviation words, collocations, and words that start sentences.
--- pip3 install --upgrade google-api-python-client
------used to obtain search results on user query

A clear description of the internal design of your project, explaining the general structure of your code (i.e., what its main high-level components are and what they do), 
as well as acknowledging and describing all external libraries that you use in your code
- For this project, we have two main components: the search on the query and query expansion to output more accurate results per user feedback. The proj1.py file is used to take the user inputs and call the google API to run the search on the given query. It then taken user feedback on each results to calculate precision of the outputs. If precision is greater than 0 but less than desired, it will call the query expansion portion of the design and pass on the current query, tiltles, snippets, and the indices of the relevant queries. Based on that, the expansion (explained in the next section below) will return an updated query to search for and repeat the process mentioned above until precision is reached. We store all the result and incides for all iterations in two global variables.

- For non-html files, we are first checking the 'fileformat' field of the Google search API. For non-html files, the search returns this fileformat key, otherwise it is not present. We manitain and increment a counter if this key is in the search results and subtract this counter from the total (10) when calculating the precision.

- For html files that are returned wihtout a title or snippet, we print a null and pass along an empty string to the query expansion.  

A detailed description of query-modification method
- The input information including current query, a list of snippets and titles from allresults and also relevant documents indices for all iterations. 

- For the query-modification method, our main idea is to use tf-idf scores for each valid word in the documents through all the iterations so far to decide which word to add. We take the mean value of scores for each word through all the relevant documents and pick the two words with highest scores(except existing term in query). 

- We first decided to use RegexpTokenizer from nltk(https://www.nltk.org/_modules/nltk/tokenize/regexp.html) to tokenize each document because it matches patterns in snippets and titles. Then we clean all the tokens, removing them if they are not alphabet, or only one character or in the stopwords. And then fit our cleaned corpus into the TfidfVectorizer. We used tf-idf Vectorizer from sklearn(https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html) to handle tf-idf measurement through all the documents. And we get the scores matrix and corresponding words from this class. Then choose only rows with relevant document indices(relevant documents from usersâ€™ input) and calculate the mean value of scores for each word through those relevant documents. We picked two words that are not in the current query with the highest mean scores. Finally reorder all the terms(the term in current query and also two new terms) based on their mean scores(in descending order).  


Google Custom Search Engine JSON API Key and Engine ID
- Erica
--- Search engine: 11fc3fe2ef66a0247
--- API key: AIzaSyBENIKHiM69Ahj3BX_851uuO83DdqUW-os

-Ishraq
--- Search engine: ef836ce004ee810dd
--- API key: AIzaSyDnbjTW2ZmRVzzRB0SPgGSyZt8HrpyEJyg