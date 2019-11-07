import pandas as pd
import re, string

jrc = pd.read_csv('input/JRCRawData.txt',
                  delim_whitespace=True, header=0, names=['id', 'type', 'lang', 'alias'])
# Remove non-person entities
jrc = jrc[jrc.type != 'O']
jrc

# Remove non-word characters
pattern = re.compile('[\W_]+', re.UNICODE)

# Create dictionary
first_name_dict = set()
last_name_dict = set()
name_dict = set()
for row in jrc.alias.str.lower().str.split('+').str[0:]:
    N = len(row)
    for (i, name) in enumerate(row):    
        new_name = pattern.sub('', name)
        # Skip empty strings
        # Skip names that begin or end with numbers
        if len(new_name) > 0 and not new_name[0].isdigit() and not new_name[-1].isdigit():
            if i == 0:
                first_name_dict.add(new_name)
            if i == N - 1 and N > 1:
                last_name_dict.add(new_name)
            name_dict.add(new_name)

# Load a list of top 10000 English words, to be removed from the JRC dataset
NUM_TOP = None
english_words = set(pd.read_csv('input/google-10000-english.txt', header=None, nrows=NUM_TOP)[0].values)
america_words = set(pd.read_csv('input/google-10000-english-usa.txt', header=None, nrows=NUM_TOP)[0].values)
top_words = english_words | america_words
# ... But we also need to remove words from this data that themselves are names. To do that,
# we'll use a cleaner source of names (but with less coverage): US/UK government birth registries
us = pd.read_csv('input/usprocessed.csv')
uk = pd.read_csv('input/ukprocessed.csv', error_bad_lines=False)
combined = pd.concat([us, uk]).groupby('Name').agg({
    'years.appearing': 'sum',
    'count.male': 'sum',
    'count.female': 'sum',
    'prob.gender': 'first',
    'obs.male': 'mean',
    'est.male': 'mean',
    'upper': 'mean',
    'lower': 'mean'
}).reset_index()
# Recompute proper 'prob.gender' values
combined['prob.gender'] = combined.apply(lambda row: "Male" if (row['count.male'] / (row['count.male'] + row['count.female'])) >= 0.5 else "Female", axis=1)
combined.to_csv('output/GenderDictionary_USandUK.csv', index=None)

for name in combined.Name:
    name = name.lower()
    if name in top_words:
        top_words.remove(name)


# Clean entries
CUSTOM = ['', 'nan', 'male']
REMOVE_LIST = list(string.ascii_lowercase) + [str(i) for i in range(10)] + list(top_words) + CUSTOM
removed = []
for c in REMOVE_LIST:
    try:
        name_dict.remove(c)
        removed.append(c)
    except KeyError as e:
        pass
    try:
        first_name_dict.remove(c)
    except KeyError as e:
        pass
    try:
        last_name_dict.remove(c)
    except KeyError as e:
        continue

print(f"Number of words removed: {len(removed)}")
pd.DataFrame.from_dict({'removed': removed}).to_csv('output/RemovedWords.txt', header=None, index=None, sep=' ')

# Combine the entries by unioning over the sets
# name_dict = first_name_dict | last_name_dict

# Write to file
def make_df_from_dict(dict):
    return pd.DataFrame.from_dict(dict).sort_values(by=[0])

first_df = make_df_from_dict(first_name_dict)
first_df.to_csv('output/Names_JRC_First.txt', header=None, index=None, sep=' ')
last_df = make_df_from_dict(last_name_dict)
last_df.to_csv('output/Nanes_JRC_Last.txt', header=None, index=None, sep=' ')
name_df = make_df_from_dict(name_dict)
name_df.to_csv('output/Names_JRC_Combined.txt', header=None, index=None, sep=' ')