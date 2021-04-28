from pprint import pprint
from googleapiclient.discovery import build
import sys
from query_expansion import query_expansion

NUM_Q = 10
API_KEY = sys.argv[1]
SEARCH_ENGINE = sys.argv[2]
QUERY = sys.argv[4]
PRECISION = sys.argv[3]
#lists and variables to calcualte precision and pass for query expansion
relevant_indices = []
all_snippets = []
num_iter = 0
non_html_cnt = 0

def run_search(query):
	global num_iter, non_html_cnt
	#summary of user inputs
	print('Parameters:')
	print('Client key =', API_KEY)
	print('Engine key =', SEARCH_ENGINE)
	print('Query      =', query)
	print('Precision  =', PRECISION)
	print('Google Search Results:\n======================')
	#call google search api with user inputs
	service = build("customsearch", "v1", developerKey = API_KEY)
	res = service.cse().list(q=query, cx=SEARCH_ENGINE).execute()
	#variable to calcualte precision and pass for query expansion
	relevance_cnt = 0
	#loop through the 10 api search outputs, one at a time
	for i in range(NUM_Q):
		#handle corner case if api does not return the items we need
		if('fileformat' in res['items'][i]):
			non_html_cnt +=1
			print('NON HTML FILE FOUND', non_html_cnt)
		if('snippet' not in res['items'][i]):
			snippet = 'null'
		else:
			snippet = res['items'][i]['snippet']

		if('title' not in res['items'][i]):
			title = 'null'
		else:
			title = res['items'][i]['title']
		if('link' not in res['items'][i]):
			url = 'null'
		else:
			url = res['items'][i]['link']
		#show results
		print('\nResult',i + 1,'\n[')
		print(' URL:',url)
		print(' Title:',title)
		print(' Summary:',snippet)
		print(']\n')
		#take user input after each result
		relevance = input('Relevant (Y/N)?')

		if(snippet == 'null'):
			snippet = ''
		if(title == 'null'):
			title = ''
		#append all snippets and title to a list to send for query expansion
		all_snippets.append(snippet + " " + title)
		#only accept yY/nN as inputs
		if(relevance == 'y' or relevance == 'Y'):
			relevance_cnt += 1
			relevant_indices.append((num_iter*10) + i)
		elif(relevance == 'n' or relevance == 'N'):
			continue
		else: #raise expection if input is neither
			raise Exception("Invalid input")
	#calculate precision
	if(non_html_cnt == 10): #terminate if all files are non-html
		print('All files returned were non-html!')
		sys.exit()
	else: #ignore non-html files when calculating precision
		precision_calc = relevance_cnt/(10-non_html_cnt)
	#show summary
	print('==================')
	print('FEEDBACK SUMMARY')
	print('Query:', query)
	print('Precision:', precision_calc)
	#compare calculated precision with user desired input
	if(precision_calc == 0): #if calculated precision is 0, stop augmenting and end program
		print('Still below the desired precision of', PRECISION)
		print('Below desired precision, but can no longer augment the query')
	elif(precision_calc < float(PRECISION)): #if calculated precision is less than desiered, call query expansion
		print('Still below the desired precision of', PRECISION)
		new_q = query_expansion(query,relevant_indices,all_snippets)
		num_iter += 1
		run_search(new_q)
	else: #if calcualted precision is over the desired value or 1, end program
		print('Desired precision reached, done')

	return

def main():
	run_search(QUERY)
if __name__ == '__main__':
	main()
