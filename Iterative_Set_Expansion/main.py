import sys
import spacy
import argparse
from pprint import pprint
from googleapiclient.discovery import build
import socket
import urllib.request
from bs4 import BeautifulSoup
from spanbert import SpanBERT
from spacy_help_functions import get_entities, create_entity_pairs
# Load pre-trained SpanBERT model
spanbert = SpanBERT("./pretrained_spanbert")
print("\n\n")
target_relations = ["Schools_Attended", "Work_For", "Live_In", "Top_Member_Employees"]
# A list of dictionaries indicating target types we need to fit into SpanBERT
target_types = [ {'Subject': 'PERSON', 'Object': ['ORGANIZATION']},
                                 {'Subject': 'PERSON', 'Object': ['ORGANIZATION']},
                                 {'Subject': 'PERSON', 'Object': ['LOCATION', 'CITY', 'STATE_OR_PROVINCE', 'COUNTRY']},
                                 {'Subject': 'ORGANIZATION', 'Object': ['PERSON']}
                                ]
# internel relation 
relations_list = ["per:schools_attended", "per:employee_of", "per:cities_of_residence", "org:top_members/employees"]
URL_seen = set()
def tuples_expansion(API_KEY, SEARCH_ENGINE, r, q, t, k, it, X):
        print(f"=========== Iteration: {it} - Query: {q} ===========")
        service = build("customsearch", "v1", developerKey = API_KEY)
        res = service.cse().list(q=q, cx=SEARCH_ENGINE).execute()
        num = min(10, len(res['items']) )
        entities_of_interest = target_types[r]['Object']
        entities_of_interest.append(target_types[r]['Subject'])
        #print(entities_of_interest)
        for i in range(num):
                url = res['items'][i]['link']
                print(f"URL ( {i+1} / {num}): {url}")
                if url not in URL_seen:
                        URL_seen.add(url)
                        print("\tFetching text from url ...")
                        text, length = text_from_url(url)
                        if text is None:
                                print("Unable to fetch URL. Continuing.")
                                continue
                        #print(text[:1000])
                        print(f"\tWebpage length (num characters): {length}")
                        print("\tAnnotating the webpage using spacy...")
                        # Load spacy model
                        nlp = spacy.load("en_core_web_lg")
                        # Apply spacy model to raw text (to split to sentences, tokenize, extract entities etc.)
                        doc = nlp(text)
                        num_sents = len(list(doc.sents))
                            extracted_num = 0
                        print(f"\tExtracted {num_sents} sentences. \
                            Processing each sentence one by one to check for presence of right pair of named entity type so, will run the second pipeline ...")
                        j = 0
                        overall_relations = 0
                        sentence_unannoted = 0
                        for sentence in doc.sents:
                                if not (j % 5) and j > 0 :
                                        print(f"\tProcessed {j}/{num_sents} sentences")
                                # tokenize sentence 
                                ents = get_entities(sentence, entities_of_interest)
                                # create entity pairs
                                candidate_pairs = []
                                sentence_entity_pairs = create_entity_pairs(sentence, entities_of_interest)
                                for ep in sentence_entity_pairs:
                                        #print(ep)
                                        # keep subject-object pairs of the right type for the target relation 
                                        # (e.g., Person:Organization for the "Work_For" relation)
                                        if ep[1][1] == target_types[r]['Subject'] and ep[2][1] in target_types[r]['Object']:
                                                candidate_pairs.append({"tokens": ep[0], "subj": ep[1], "obj": ep[2]})
                                        elif  ep[2][1] == target_types[r]['Subject'] and ep[1][1] in target_types[r]['Object']:
                                                candidate_pairs.append({"tokens": ep[0], "subj": ep[2], "obj": ep[1]})
                                if len(candidate_pairs) == 0:
                                        sentence_unannoted += 1
                                        j += 1
                                        continue
                                #print(candidate_pairs)
                                relation_preds = spanbert.predict(candidate_pairs)
                                # Process predicted realtions 
                                for ex, pred in list(zip(candidate_pairs, relation_preds)):
                                        pred_relation = pred[0]
                                        confidence = pred[1]
                                        if pred_relation == relations_list[r]:
                                                overall_relations += 1
                                                print("\t\t=== Extracted Relation ===")
                                                print("\t\tSentence: {}".format(sentence))
                                                print("\t\t Confidence: {:.4f} ; Subject: {} ; Object: {} ;".format(confidence, ex["subj"][0], ex["obj"][0]))
                                                if confidence < t:
                                                        print("\t\tConfidence is lower than threshold confidence. Ignoring this. ")
                                                else:
                                                        current_tuple = (ex["subj"][0], ex["obj"][0])
                                                        if current_tuple not in X.keys():
                                                                print("\t\tAdding to set of extracted relations.")
                                                                X[current_tuple] = confidence
                                                                extracted_num += 1
                                                        elif (X[current_tuple] < confidence):
                                                                print("\t\tAdding to set of extracted relations.")
                                                                X[current_tuple] = confidence
                                                        else:
                                                                print("\t\tDuplicate with lower confidence than existing record. Ignoring this.")
                                                print("\t\t==========")
                                j += 1
                        print(f" Extracted annotations for  {num_sents - sentence_unannoted}  out of total  {num_sents} sentences ")
                        print(f" Relations extracted from this website: {extracted_num} (Overall: {overall_relations}) ")
                else:
                        print("URL seen before, skipped.")
        return X

def text_from_url(url):
        try:
                req = urllib.request.Request(url)
                response = urllib.request.urlopen(req, timeout=10).read().decode("utf-8")
        except:
                return None, 0
        soup = BeautifulSoup(response, "html.parser")
        #remove tags
        for script in soup(["script", "style"]):
                script.extract()
        text = soup.get_text().replace("\n", " ")
        text = list(text)
        truncate_num = min(20000, len(text))
        text = "".join(text[:truncate_num])
        #print(text)
        return text, truncate_num
if __name__ == "__main__":
        #parse arguments 
        parser = argparse.ArgumentParser(description='Parse argument for running project 2.')
        parser.add_argument('API_KEY', metavar='API_KEY', type=str,
                help='Your Google Custom Search Engine JSON API Key. \n' )
        parser.add_argument('SEARCH_ENGINE', metavar='SEARCH_ENGINE', type=str,
                help='Your Google Engine ID \n')
        parser.add_argument('r', metavar='r', type=int, choices=range(1, 5),
                help='An integer r between 1 and 4, indicating the relation to extract\n')
        #1 is for Schools_Attended, 2 is for Work_For,
        #3 is for Live_In, and 4 is for Top_Member_Employees
        parser.add_argument('t', metavar='t', type=float,
                help='A real number t between 0 and 1, indicating the extraction confidence threshold \n')
        parser.add_argument('q', metavar='q', type=str,
                help='A seed query q, which is a list of words i \n')
        parser.add_argument('k', metavar='k', type=int,
                help='An integer greater than 0, indicating the number of tuples that we request in the output \n')
        args = parser.parse_args()
        if args.t > 1 or args.t < 0:
                print("t should be in range [0, 1] ")
                exit()
        if args.k <= 0:
                print("k should be larger than 0. ")
                exit()
        r = args.r-1 # convinient for indexing 
        print("____")
        print('Parameters:')
        print('Client key   =', args.API_KEY)
        print('Engine key   =', args.SEARCH_ENGINE)
        print('Relation     =', relations_list[r])
        print('Threshold    =', args.t)
        print('Query        =', args.q)
        print("# of Tuples  = ", args.k)
        print("Loading necessary libraries; This should take a minute or so ...)")
        X = {}  # dicitonary : (Subject, Object): confidence score
        used_X = [] #keep track of new queries after initial user input, in more than 1 iteration is needed
        iteration_num = 0
        pointer = 0
        while len(X) < args.k:
                if (iteration_num == 0):
                        q = args.q
                else:
                        print(pointer)
                        while(sorted_X[pointer][0] in used_X):
                                pointer += 1
                                if(pointer == len(sorted_X)):
                                        print("No tuple exists for further iterations, exiting program... ")
                                        exit()
                        q = " ".join(sorted_X[pointer][0]) #sorted_X[0] is always the best confidence
                        used_X.append(sorted_X[pointer][0])
                        pointer = 0
                X = tuples_expansion(args.API_KEY, args.SEARCH_ENGINE, r, q, args.t, args.k, iteration_num, X)
                iteration_num += 1
                if (len(X)>0):
                        sorted_X = sorted(X.items(), key=lambda item:item[1], reverse=True) #sort by confidence
                else:
                        print("Unable to fetch any URL, exiting program...")
                        exit()
                print(f"==================== ALL RELATIONS for {relations_list[r]} ({len(X)}) ====================")
                #sorted_X = sorted(X.items(), key=lambda item:item[1], reverse=true) #sort by confidence
                for k, v in sorted_X:
                        print(f"Confidence: {v}     | Subject: {k[0]}   | Object: {k[1]} ")
        print(f"Total # of iterations = {iteration_num}")

