
## Package need to install 
```
pip3 install beautifulsoup4 
sudo apt-get update
pip3 install -U pip setuptools wheel
pip3 install -U spacy
python3 -m spacy download en_core_web_lg 
git clone https://github.com/gkaramanolakis/SpanBERT
cd SpanBERT
pip3 install -r requirements.txt
bash download_finetuned.sh
```
Once the SpanBERT folder is cloned from github, requirements.txt is installed, and the script is run per the instructions, copy/move the all files inside the SpanBERT folder. The main.py file references the spacy_help_functions.py within the SpanBERT folder. 

## How to run 
Once the above steps are followed, the program can be run as the following:
```
python3 main.py <google api key> <google engine id> <r> <t> <q> <k>
```

## Description about project design 
For this project, we have four main steps.

- First, it processes input arguments and calls the google API to run the search on the given query, getting 10 results.
- Then, function text_from_url processes each URL from the results and extracts the main text from each website.  We used urllib to request the website and BeautifulSoup to extract text. 
- We process the main text by spaCy to split the text into sentences and extract named entities.  We filter the candidate pairs by corresponding named entities and then use the sentences and named entity pairs as input to SpanBERT to predict the corresponding relations. We add tuples that have correctly predicted relations and score larger than the confidence threshold. 
- Then we sort the tuples in X using Python's sorted() function and arrange in decreasing ordered based on confidence, which is the value in the X dictionary. The sorted() function returns a list of the organized key-value pairs, where the key contain subject and object and the value is the confidence. If we need more than one iteration to reach the desired top-k tuples, we maintain a pointer variable which points to the 0th index of the sorted list, which is the highest confidence tuple. Before starting the following iteration, we check if that 0th key was used as a query previously by comparing with a list which contains used queries from the sorted list. It then updates the query accordingly and call the google API to run the search. 
 
