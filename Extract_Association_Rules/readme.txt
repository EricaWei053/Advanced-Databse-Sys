Erica Wei (cw3137)
Ishraq Khandaker (ibk2110)

A list of all the files that you are submitting.
- main.py
-- this file containts all the code for this project
- INTEGRATED-DATASET.csv
-- this is the dataset used for testing our algorithm, details in section below
- example-run.txt
-- this file containts the output of a compelling sample run
- README.txt


A clear description of how to run your program. Note that your project must compile/run in a Google Cloud VM set up exactly following our instructions; if you need more memory, please indicate so clearly in the README file and specify what configuration we should use for your Google Cloud VM. Provide all commands necessary to install the required software and dependencies for your program.
- For this project testing, the Google Cloud VM was configured for n1-standard-4 (4 vCPUs, 15GB memory), unchanged from project 2.
- To run the program, first unpack the proj3 tarball and please make sure the INTEGRATED-DATASET.csv (the any input dataset in general) is in the same directory as the main.py file unpacked from the tarball. 
- Then, the following from the command line:
-- python3 main.py INTEGRATED-DATASET.csv <min_sup> <min_conf>
- Once the program is complete, the terminal will print a "Finished" line and the output.txt file will be generated or written over (if already exists) in the same directory as the .py file.


A detailed description explaining: (a) which NYC Open Data data set(s) you used to generate the INTEGRATED-DATASET file; (b) what (high-level) procedure you used to map the original NYC Open Data data set(s) into your INTEGRATED-DATASET file; (c) what makes your choice of INTEGRATED-DATASET file compelling (in other words, justify your choice of NYC Open Data data set(s)). The explanation should be detailed enough to allow us to recreate your INTEGRATED-DATASET file exactly from scratch from the NYC Open Data site.
- For this project, we used the "NYPD Complain Data Historic" dataset which includes all valid felony, misdemeanor, and violation crimes reported to the NYPD from 2006 through 2019. Crime is a big part of NYC, unfortunately, and we thought this would be a good dataset to understand the types, frequency, and relations of a crime in a given year. We often see/hear news flashes about crimes throughout the boroughs but this dataset and project gives a good insight on high level victim and suspect descriptions as well as types and locations of these crimes. Hence, we selected this dataset.
- However, this dataset has about 7 million rows so to keep the dataset at a reasonable size, we used only the 2019 data (~450K rows). To obtain the 2019 data, we filtered by the CMPLNT_FR_FT (date of occurance of the reported event) is after 12/31/2018.
- Once this data was downloaded, we made further modifications to the dataset so it is more suitable and revealing for the purposes of this project:
-- We removed several columns that were primarily used to report times, dates, internal code number, incident status etc.
-- We only kept the following columns: ADDR_PCT_CD (precint at which incident occured)	OFNS_DESC (Description of offense corresponding with key code)	LAW_CAT_CD (Level of offense: felony, misdemeanor, violation )	BORO_NM (The name of the borough in which the incident occurred)	LOC_OF_OCCUR_DESC (Specific location of occurrence in or around the premises; inside, opposite of, front of, rear of)	PREM_TYP_DESC (Specific description of premises; grocery store, residence, street, etc.)	SUSP_AGE_GROUP (Suspectâ€™s Age Group)	SUSP_RACE (Suspectâ€™s Race Description)	SUSP_SEX (Suspectâ€™s Sex Description)	VIC_AGE_GROUP (Victimâ€™s Age Group)	VIC_RACE (Victimâ€™s Race Description)	VIC_SEX (Victimâ€™s Sex Description)
-- Furthermore, since some of the columns has similar information, such as victim age vs suspect age, there was not a clear way to distinguish these items. So we edited the csv file through excel and updated those fields, for example "Vic_Age = X" instead of the given "X", so that number is not confused with suspect age when running hte algorithm and discussing our results.


A clear description of the internal design of your project; in particular, if you decided to implement variations of the original a-priori algorithm (see above), you must explain precisely what variations you have implemented and why.
- Our project can be broken down in three key part: process the dataset, compute and produce the frequent itemsets, and build association rules on those frequent itemsets.
- First, we take the input csv dataset and add all the rows (markets baskets) to a list and all the items in a set as frozen set to only keep track of the unique items. These set (to generate itemsets) and list (to compute frequency of items) are used later on to compute frequent set, support scores, and obtain the association rules. 
- Next, we iterate though the market baskets and count the frequency of each item in the full dataset. This allows us to then generate an itemset containing items with frequency >= to the minimum support input. This gives the first candidate set.
- Following the Agrawal and Srikant paper, we do the join step and prune steps in a loop to compute frequent itemsets and support scores.
- After generating all of the itemsets with support scores, we feed the largest itemsets C(k-1) to the function get_association_rule with the global map that contains all itemsets and supports scores. For each item set, we make each item as right-hand-side [item] and use the remaining items to get all combinations from genreate_subset as left-hand-side [item1, .. item_n], then we check if LHS -> RHS has a confident score larger than min_conf. Then output all sorted association rules with min_confident score. For the output function, it will simply write all item sets with support score and associate rules with the confidence score to file output.txt. 


The command line specification of a compelling sample run (i.e., a min_sup, min_conf combination that produces association rules that are revealing, surprising, useful, or helpful; see above). Briefly explain why the results are indeed compelling.
- Command line specification for the sample run is below:

-- python3 main.py INTEGRATED-DATASET.csv 0.1 0.2
- Based on frequent itemsets, interesting to see most crimes committed in 2019 were "Inside" premises, such as residence, commercial building, hospital, bar etc. 
-- [INSIDE], 54.21%
- Similarly, misdemeanors are most frequent crimes in NYC
-- [MISDEMEANOR], 53.61%
-- [FELONY], 30.5%
- Most identified suspects are male and the 25-44 age group is common for suspects, note that some suspect info does not include M/F sex
-- [Sus_Sex = M], 46.37%
-- [Sus_Age = 25-44], 25.64%
- Crimes commited at or inside a apartment/resident are often with female victims
-- [RESIDENCE - APT. HOUSE,INSIDE] => [Vic Sex = F] (Conf: 61.4%, Supp: 11.65%)
-- [RESIDENCE - APT. HOUSE] => [Vic Sex = F] (Conf: 60.0%, Supp: 13.07%)
- Male suspects often go after female victims in particular
-- [Sus_Sex = M] => [Vic Sex = F] (Conf: 40.56%, Supp: 18.81%)