from __future__ import division
import csv
import pandas as pd 
import numpy as np

# Import yearly dataset with relevant vars as a dataframe 
y = 2007 
fname = "M:/IPUMS/hhdata/" + str(y) + ".csv"
varnames =  ['metaread',  # MSA 
				'year', 	 # Year
				'hhwt', 	 # Household weight
				'relate',	 # Relationship to hh head
				'hhtype',	 # HH type
				'numprec',   # Num person records following
				'bedrooms',  # Num bedrooms
				'gq',		 # Group quarter status
				'ownershpd', # Ownership status (tenure)
				'mortgage',  # Mortgage status
				'rent',		 # Rent
				'hhincome',  # Total hh income
				'nfams',	 # Num families in hh 
				'unitsstr',  # Units in structure
				'age',       # Age
				'marst',     # Marital status
				'raced',     # Detailed race
				'educd',	 # Education
				'empstatd',  # Employment status
				'serial', 	 # Household ID
				'nsubfam',   # Number of subfamilies
				'nfams',     # Number of families
				'ncouples',  # Number of couples
				'multgend',  # Number of generations living together
				'famsize',   # Size of family
				'subfam', 	 # Subfam
				'famunit' ]	 # Family unit]  

print varnames

# Get col indices of relevant vars 
f = csv.DictReader(open(fname,'rb'))
header = f.fieldnames
col_indices = [header.index(v) for v in varnames]
year = 2007

# Extract relevant vars from file by col index, read into dataframe
full = pd.read_csv("M:/IPUMS/hhdata/"+str(year)+".csv", usecols = col_indices)

# For each household, calculate the number of related and non-related members 
hhid = full['serial'].drop_duplicates()
heads = pd.DataFrame(np.random.randn(len(hhid), len(varnames)), index = hhid)
full_hh = full.groupby('serial')
for (serialid, hhinfo) in full_hh: 
	nrel_criterion = hhinfo['relate'].map(lambda x: x in ['Partner, friend, visitor', 'Other non-relatives', 'Institutional inmates'])
	rel_criterion = hhinfo['relate'].map(lambda x: x not in ['Partner, friend, visitor', 'Other non-relatives', 'Institutional inmates'])
	
	nrel_df = hhinfo[nrel_criterion]
	rel_df = hhinfo[rel_criterion]

	num_nonrel = nrel_df['relate'].count()
	num_rel = rel_df['relate'].count()

	share_nonrel = num_nonrel/ hhinfo['relate'].count()
	share_rel = num_rel/ hhinfo['relate'].count()

	hhinfo['rel_share'] = share_rel
	hhinfo['nonrel_share'] = share_nonrel

	hhinfo = hhinfo[hhinfo['relate'] == "Head/Householder"]
	
	heads.update(hhinfo)


	print [str(serialid), 'numrel: ' + str(num_rel), 'num_nonrel: ' + str(num_nonrel)]
	#nonrelatives = hhinfo[hhinfo['relate'] in ['Partner, friend, visitor', 'Other non-relatives', 'Institutional inmates']] 
