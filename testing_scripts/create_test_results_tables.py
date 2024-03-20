import pandas as pd

test_results_file = 'testing_results_v2/test_results.txt'
# ERR3326140	neisseria_gonorrhoeae	Neisseria	485	CEPHALOSPORIN	penA_A510V;penA_A516G;penA_F504L	penA_A510V;penA_A516G;penA_F504L	True

# Define the column names
column_names = ['sample', 'species', 'databases', 'taxid', 'drug', 'expected', 'actual', 'passed']

# Use the column names when reading the file
df = pd.read_csv(test_results_file, sep="\t", names=column_names)
# Get rows where 'passed' column is False
failed_tests = df[df['passed'] == False]
# Sort by 'species'
failed_tests = failed_tests.sort_values('species')
failed_tests.to_csv(f'test_results_tables/all-failed.tsv', sep='\t', index=False)

# Group by the 'species' column
grouped = df.groupby('species')



# Create a DataFrame to store all failed tests
# failed_tests_df = pd.concat(failed_tests)

# Write a CSV file for each species
for name, group in grouped:
    taxid = group['taxid'].unique()[0]
    group.to_csv(f'test_results_tables/{taxid}-{name}.tsv', sep='\t', index=False)

