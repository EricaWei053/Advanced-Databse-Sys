 

A clear description of the internal design of your project, explaining the general structure of your code (i.e., what its main high-level components are and what they do), as well as acknowledging and describing all external libraries that you use in your code

	For this project, we have four main steps. 

	1. First, it processes input arguments and calls the google API to run the search on the given query, getting 10 results. 
	2. Then, function text_from_url processes each URL from the results and extracts the main text from each website.  We used urllib to request the website and BeautifulSoup to extract text. 
	3. We process the main text by spaCy to split the text into sentences and extract named entities.  We filter the candidate pairs by corresponding named entities and then use the sentences and named entity pairs as input to SpanBERT to predict the corresponding relations. We add tuples that have correctly predicted relations and score larger than the confidence threshold. 
	4.# sort X and generate new query: 

A detailed description of how you carried out Step 3 in the "Description" section above

	We have a function text_from_url to extract text from URL. For each URL, if the request time is more than 10 seconds then we skip it. After getting the text from each website, if it’s larger than 20,000  characters we take only the previous 20,000 characters. Then we use spaCy to split the text into sentences and extract named entities. For each pair in the sentence, we check if the named entities are the same ones in expected relation (For example, if the relations is Schools_Attended, we check if the two named entities in a pair are PERSON and ORGANIZATION), if they are correct ones, we added them into condidate_pairs list. After checking all the pairs in this sentence, we feed candidate_pairs list  into spanBERT to get predicted relations and confidence scores. We add those pairs whose predicted relation is what we want and the confidence score is above threshold. If the pair is already in X, we either update it with a higher score or skip it if the current score is lower than the one in X. 
