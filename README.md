# Advanced-Databse-Sys
This repo contains projects(information retrieval system, information extraction on the web and rules extraction by a-priori algorithm) in class COMS6111 at Columbia. 

Prof: Luis Gravano

Team: Erica Wei, Ishraq Khandaker


## Project 1 (Information Retrieval System)
In this project, we implemented an information retrieval system that exploits user-provided relevance feedback to improve the search results returned by Google. User queries are often ambiguous. For example, a user who issues a query [jaguar] might be after documents about the car or the animal, and in fact search engines like Bing and Google return pages on both topics among their top 10 results for the query. In this project, we designed and implemented a query-reformulation system to disambiguate queries and improve the relevance of the query results that are produced. 


Details in ```./Information_Retrieval_Sys``` 


## Project 2 (Iterative Set Expansion)

In this project, we implemented a version of the Iterative Set Expansion (ISE) algorithm that described in class: for a target information extraction task, an "extraction confidence threshold," a "seed query" for the task, and a desired number of tuples k, following ISE, starting with the seed query (which should correspond to a plausible tuple for the relation to extract), to return k tuples extracted for the specified relation from web pages with at least the given extraction confidence. We used the spaCy library and the pre-trained SpanBERT classifier to annotate the plain text from each webpage and extract tuples for the target relation r.

The objective of this project is (i) retrieve and parse webpages; (ii) prepare and annotate text on the webpages for subsequent analysis; and (iii) extract structured information from the webpages.
### Example 

As an example, consider the following sentence and the output from the full information extraction process:

Sentence: "Bill Gates stepped down as chairman of Microsoft in February 2014 and assumed a new post as technology adviser to support the newly appointed CEO Satya Nadella."
```
Script output:
spaCy extracted entities: [('Bill Gates', 'PERSON'), ('Microsoft', 'ORGANIZATION'), ('February 2014', 'DATE'), ('Satya Nadella', 'PERSON')]
Candidate entity pairs:
1. Subject: ('Bill Gates', 'PERSON')   Object: ('Microsoft', 'ORGANIZATION')
2. Subject: ('Microsoft', 'ORGANIZATION')   Object: ('Bill Gates', 'PERSON')
3. Subject: ('Bill Gates', 'PERSON')   Object: ('Satya Nadella', 'PERSON')
4. Subject: ('Satya Nadella', 'PERSON')   Object: ('Bill Gates', 'PERSON')
5. Subject: ('Microsoft', 'ORGANIZATION')   Object: ('Satya Nadella', 'PERSON')
6. Subject: ('Satya Nadella', 'PERSON')   Object: ('Microsoft', 'ORGANIZATION')
```
SpanBERT extracted relations:
```
1. Subject: Bill Gates   Object: Microsoft   Relation: per:employee_of   Confidence: 1.00
2. Subject: Microsoft   Object: Bill Gates   Relation: org:top_members/employees   Confidence: 0.99
3. Subject: Bill Gates   Object: Satya Nadella  Relation: no_relation   Confidence: 1.00
4. Subject: Satya Nadella   Object: Bill Gates   Relation: no_relation   Confidence: 0.52
5. Subject: Microsoft   Object: Satya Nadella   Relation: no_relation   Confidence: 0.99
6. Subject: Satya Nadella   Object: Microsoft   Relation: per:employee_of   Confidence: 0.98
```
Details in ```./Iterative_Set_Expansion``` 

## Project 3 (Extract Association Rules)

For this project we implemented A-priori algorithm to extract association rules from an the give database.


### Example:

As a "toy" example from class, consider the following INTEGRATED-DATASET file, which is a CSV with four "market baskets":
```
pen,ink,diary,soap
pen,ink,diary
pen,diary
pen,ink,soap
```
By running the program with min_sup=0.7 and min_conf=0.8, the program should produce a file output.txt with the following information:
```
==Frequent itemsets (min_sup=70%)
[pen], 100%
[diary], 75%
[diary,pen], 75%
[ink], 75%
[ink,pen], 75%
==High-confidence association rules (min_conf=80%)
[diary] => [pen] (Conf: 100.0%, Supp: 75%)
[ink] => [pen] (Conf: 100.0%, Supp: 75%)
```

Details in ```./Extract_Association_Rules``` 


## Note 

For project 1 and 2, we need two inputs to sucessfully run. 
```
<google api key>, your Google Custom Search JSON API Key  
<google engine id>, your Google Custom Search Engine ID  
```
