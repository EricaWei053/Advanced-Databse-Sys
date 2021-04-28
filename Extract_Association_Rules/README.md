
## How ro run 
```
python3 main.py EXAMPLE-DATASET.csv <min_sup> <min_conf>
```

- Once the program is complete, the terminal will print a "Finished" line and the output.txt file will be generated or written over (if already exists) in the same directory as the .py file.
- You can change dataset by yourself but make sure it's a csv file. 

## Description of project design 

- Our project can be broken down in three key part: process the dataset, compute and produce the frequent itemsets, and build association rules on those frequent itemsets.
- First, we take the input csv dataset and add all the rows (markets baskets) to a list and all the items in a set as frozen set to only keep track of the unique items. These set (to generate itemsets) and list (to compute frequency of items) are used later on to compute frequent set, support scores, and obtain the association rules. 
- Next, we iterate though the market baskets and count the frequency of each item in the full dataset. This allows us to then generate an itemset containing items with frequency >= to the minimum support input. This gives the first candidate set.
- Following the Agrawal and Srikant paper, we do the join step and prune steps in a loop to compute frequent itemsets and support scores.
- After generating all of the itemsets with support scores, we feed the largest itemsets C(k-1) to the function get_association_rule with the global map that contains all itemsets and supports scores. For each item set, we make each item as right-hand-side [item] and use the remaining items to get all combinations from genreate_subset as left-hand-side [item1, .. item_n], then we check if LHS -> RHS has a confident score larger than min_conf. Then output all sorted association rules with min_confident score. For the output function, it will simply write all item sets with support score and associate rules with the confidence score to file output.txt. 

The command line specification of a compelling sample run (i.e., a min_sup, min_conf combination that produces association rules that are revealing, surprising, useful, or helpful; see above). Briefly explain why the results are indeed compelling.
 
