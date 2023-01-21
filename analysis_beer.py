"""
Exploring and organizing data using only native tools of Python language.

The objective here is combine datas that are in different datasets. These datasets are relative a beers and breweries but the information need to be joined taking that in the first dataset are all beers and your respective technical informations and at second dataset contains the name and specific informations about the breweries.

Let me learn you how to combine that informations using only native tools of Python language. Yes, no library or framework has been installed.

The datasets has used in this code were get at https://www.kaggle.com/datasets/nickhould/craft-cans?resource=download
Obs: The datasets are outdated, they are from 2017 or so.

Finally, the output is here will looks like this example below:

{
    "name": "Angry Minnow Brewing Company",
    "city": "Hayward",
    "state": " WI",
    "brewery_id": 542,
    "beers": [
        {
            "": "120",
            "abv": "0.054000000000000006",
            "ibu": "",
            "id": "410",
            "name": "River Pig Pale Ale",
            "style": "American Pale Ale (APA)",
            "brewery_id": 542,
            "ounces": "16.0"
        },
        {
            "": "121",
            "abv": "0.047",
            "ibu": "",
            "id": "409",
            "name": "Oaky's Oatmeal Stout",
            "style": "Oatmeal Stout",
            "brewery_id": 542,
            "ounces": "16.0"
        }
    ]
}
"""

import csv
import os
import pathlib
import itertools
from operator import itemgetter
import json


def read_csv_folder(content_root_folder):
    """
    Read any csv file on root folder.

    - param(s):
        content_root_folder: root folder content.

    - return:
        list_csv_beers: list of csv's content list.
    """

    # list that holds any csv that are on the root folder
    list_csv_beers = list()

    # Access root folder content
    for file in content_root_folder:
        # Verify if the file extension is equal .csv
        if pathlib.Path(file).suffix == ".csv":
            # Access the csv file, and extract the respective content
            with open(file, newline="") as csv_file:
                list_new_csv = list()
                # Insert into list_csv each line from csv file
                for row in csv.DictReader(csv_file):
                    list_new_csv.append(row)
                list_csv_beers.append(list_new_csv)
    
    return list_csv_beers

# Read the csv file
lines_csv_files = read_csv_folder(os.listdir(os.getcwd()))

# the next step is to analyze the data
# Here we have to do some updates into dicts
# Excluding the values that are into "" key because we won't need work with these values
# It is made only at the first list of dicts - list of beers
for row in lines_csv_files[0]:
    del row[""]

# Now at second list of dicts - list of breweries
# Creating a new field into a each dict that are on second list into lines_csv_files
# Inserting "breweries_id" as a key in this new field and copying the value that contains into a "" keys
# After is time to exclude the "" keys of each dict
# Now here we have a set of organized dicts
for row in lines_csv_files[1]:
    row["brewery_id"] = int(row[""])
    del row[""]

# Now we'll join that two dict lists (lines_csv_files) inserting all dicts into a new list called list_csv_dict
list_csv_dict = []
list_csv_dict.extend(lines_csv_files[1])
[item.update({"brewery_id": int(item["brewery_id"])}) for item in lines_csv_files[0]]
list_csv_dict.extend(lines_csv_files[0])

# Now is needed to order all dict
list_csv_dict = sorted(list_csv_dict, key=itemgetter("brewery_id"))

# After we'll a group all dicts that has the same "brewery_id"
iterator_csv_dict = itertools.groupby(list_csv_dict, key=lambda x:(x["brewery_id"]))

# In the last time we'll organize our output
for key_csv_dict, total_csv_dict in iterator_csv_dict:
    # List that holds all dicts of the group
    list_total_csv_dict = list(total_csv_dict)
    # It will hold our dict finalized
    # The ** is used to join the first dict of the group that contains the breweries data with the list of dicts of group that contains all beers and your respective technical informations
    line_dict = dict(list_total_csv_dict[0], **{"beers": list(list_total_csv_dict[1:])})
    # Converts the dict to json type
    line_json = json.dumps(line_dict, indent=4)
    print(line_json)
