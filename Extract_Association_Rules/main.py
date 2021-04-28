import sys
import argparse
import csv
from itertools import combinations, chain
from collections import defaultdict
from operator import itemgetter 

freq_itemset_with_sup = dict() 

def get_candidate_set(ds):

	candidate_set = set()
	candidate_set_list = list()
	
	with open(ds, mode='r', encoding='utf-8-sig') as f:
		csv_data = csv.reader(f, delimiter=',')
		for market_basket in csv_data:
			line = list(filter(None, line))
			candidate_set_list.append(set(market_basket)) #put market baskets in a list to compare for frequency
			for item in market_basket:
				#if (item != '' and item !='Age ' and item !='Rate ' and item != 'Age .' and item != 'Rate .'):
				candidate_set.add(frozenset([item]))
	return candidate_set, candidate_set_list

def meet_min_sup(c, mb_list, ms):
	
	global freq_itemset_with_sup 

	itemset = set() #may not need this, only this dict is fine given Erica's code
	candidate_set_sup = defaultdict(int) #key=item:value=sup

	for item in c:
		for marketbasket in mb_list:
			if item.issubset(marketbasket):
				candidate_set_sup[item] += 1

	for item, sup in candidate_set_sup.items():
		freq_ratio = float(sup/len(mb_list)) 
		if(freq_ratio >= ms):
			itemset.add(item)
			freq_itemset_with_sup[frozenset(item)] = freq_ratio

	return itemset # itemset with at least min support items

def genreate_subset(items): 
	"""
	Get a list of subsets combinations from a set of items. 
	"""
	subset = list(chain.from_iterable( list(combinations(items, r)) for r in range(1, len(items)+1)))
	return subset

def get_association_rule(freq_set, support_scores, min_conf):
	"""
	Genreate association rules based on largets frequent itemsets and support scores. 
	"""
	rules = []
	for itemset in freq_set:
		if len(itemset) < 2:
			continue

		for item in itemset:
			remaining = list(itemset.copy())
			remaining.remove(item) 

			subset = genreate_subset(remaining)
			for lhs in subset:
				lhs = list(lhs) 
				rhs_lhs = lhs.copy()
				rhs_lhs.append(item) 
				if frozenset(rhs_lhs) in support_scores and frozenset(lhs) in support_scores:
					confidence = support_scores[frozenset(rhs_lhs)] / support_scores[frozenset(lhs)]
					rule = [ lhs, [item],  confidence , support_scores[frozenset(rhs_lhs)] ] 
					if confidence > min_conf and (rule not in rules):
						rules.append(rule)
	return sorted(rules, key=itemgetter(2), reverse=True)

def output(rules, support_scores, min_conf, min_sup):
	"""
	Writing results to file output.txt 
	"""
	fout = open("./output.txt" , "w")
	fout.write(f"==Frequent itemsets (min_sup={min_sup*100}%)\n")
	for k, v in sorted(support_scores.items(), key=lambda kv: kv[1], reverse=True):
		item = "[" + ",".join(list(k)) + "]"
		fout.write(f"{item}, { round(v*100, 2)}%\n") 

	fout.write(f"==High-confidence association rules (min_conf={min_conf*100}%)\n")
	
	for rule in rules:
		lhs = "[" + ",".join(rule[0]) + "]"
		rhs = "[" + ",".join(rule[1]) + "]"
		fout.write(f"{lhs} => {rhs} (Conf: {round(rule[2] *100, 2)}%, Supp: {round(rule[3]*100, 2)}%)\n")

if __name__ == "__main__":

	#parse arguments
	parser = argparse.ArgumentParser(description='Parse argument for running project 3')

	parser.add_argument('dataset', metavar='dataset', type=str, help='the integrated dataset csv \n')

	parser.add_argument('min_sup', metavar='min_sup', type=float, help='value between 0 and 1, indicating the minimum support \n')

	parser.add_argument('min_conf', metavar='min_conf', type=float, help='value between 0 and 1, indicating the minimum confidence \n')

	args = parser.parse_args()
	ds = args.dataset
	ms = args.min_sup
	mc = args.min_conf

	if ms > 1 or ms < 0:
		print('minimum support value should be in range [0, 1].')
		exit()
	if mc > 1 or mc < 0:
		print('minimum support value should be in range [0, 1].')
		exit()

	print('_______________')
	print('User inputs:')
	print('dataset  =', ds)
	print('min_sup  =', ms)
	print('min_conf =', mc)
	print('---------------')

	freq_itemset = dict() #key=k:value=curr_L
	print("Getting data from dataset...")
	candidate_set, baskets =get_candidate_set(ds)
	itemset_L = meet_min_sup(candidate_set, baskets, ms) #only keep Ck values with sup >= min sup input
	curr_itemset_L = itemset_L
 
	k=2

	while(len(curr_itemset_L) > 0):
		print("Getting new freq itemset, k = ", k)
		freq_itemset[k-1] = curr_itemset_L
		#get C[k] by joinin L[k-1] 
		C_k = set()
		for item in curr_itemset_L:
			for it in curr_itemset_L:
				if(len(item.union(it)) == k):
					C_k.add(item.union(it)) 
		
		#prune step
		candidate_pruned = C_k.copy()
		for item in C_k:
			subsets = combinations(item, k-1)
			for s in subsets:
				if(frozenset(s) not in curr_itemset_L):
					candidate_pruned.remove(item)
					#print(ck_pruned)
					break
		k += 1 		
		#get new min sup values
		curr_itemset_L = meet_min_sup(candidate_pruned, baskets, ms)

	last_freq_itemset = freq_itemset[k-2]

	# we use last_freq_itemset cuz we will do combination of each of them 
	#and then use sup score to get assoc scores
	print("Getting association rules...")
	assoc_rule = get_association_rule(last_freq_itemset, freq_itemset_with_sup, mc)
	print("Total number of rules:" , len(assoc_rule))
	print("Writing to file...")
	output(assoc_rule, freq_itemset_with_sup, ms, mc)
	print('Finished')

