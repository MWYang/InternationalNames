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


# Clean entries a bit
CUSTOM = ['', 'nan', 'male']
REMOVE_LIST = list(string.ascii_lowercase) + [str(i) for i in range(10)] + CUSTOM
for c in REMOVE_LIST:
    try:
        first_name_dict.remove(c)
        last_name_dict.remove(c)
        name_dict.remove(c)
    except KeyError as e:
        continue

# Combine the entries by unioning over the sets
# name_dict = first_name_dict | last_name_dict

# Write to file
def make_df_from_dict(dict):
    return pd.DataFrame.from_dict(dict).sort_values(by=[0])

first_df = make_df_from_dict(first_name_dict)
first_df.to_csv('output/JRC_First.txt', header=None, index=None, sep=' ')
last_df = make_df_from_dict(last_name_dict)
last_df.to_csv('output/JRC_Last.txt', header=None, index=None, sep=' ')
name_df = make_df_from_dict(name_dict)
name_df.to_csv('output/JRC_Combined.txt', header=None, index=None, sep=' ')
