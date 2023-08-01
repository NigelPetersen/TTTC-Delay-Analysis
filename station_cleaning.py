import numpy as np
import pandas as pd
import sklearn
import matplotlib as plt
import seaborn as sns
from itertools import compress

Delays_2023 = pd.read_csv("https://raw.githubusercontent.com/NigelPetersen/TTTC-Delay-Analysis/main/ttc-subway-delay-data-2023.csv")

true_stations = [
    "Finch",
    "North York Centre",
    "Sheppard-Yonge",
    "York Mills",
    "Lawrence",
    "Eglinton",
    "Davisville",
    "St. Clair",
    "Summerhill",
    "Rosedale",
    "Bloor-Yonge",
    "Wellesley",
    "College",
    "Dundas",
    "Queen",
    "King",
    "Union",
    "St. Andrew",
    "Osgoode",
    "St. Patrick",
    "Queen's Park",
    "Museum",
    "St. George",
    "Spadina",
    "Dupont",
    "St. Clair West",
    "Eglinton West",
    "Glencairn",
    "Lawrence West",
    "Yorkdale",
    "Wilson",
    "Sheppard West",
    "Downsview Park",
    "Finch West",
    "York University",
    "Pioneer Village",
    "Highway 407",
    "Vaughan",
    "Kipling",
    "Islington",
    "Royal York",
    "Old Mill",
    "Jane",
    "Runnymede",
    "High Park",
    "Keele",
    "Dundas West",
    "Lansdowne",
    "Dufferin",
    "Ossington",
    "Christie",
    "Bathurst",
    "Bay",
    "Sherbourne",
    "Castle Frank",
    "Broadview",
    "Chester",
    "Pape",
    "Donlands",
    "Greenwood",
    "Coxwell",
    "Woodbine",
    "Main Street",
    "Victoria Park",
    "Warden",
    "Kennedy",
    "Lawrence East",
    "Ellesmere",
    "Midland",
    "Scarborough Centre",
    "McCowan",
    "Bayview",
    "Bessarion",
    "Leslie",
    "Don Mills"
]
true_station_names = [(station+" station").upper() for station in true_stations]

for i in range(len(Delays_2023)):
    station_name = Delays_2023["Station"][i]
    if " TO " in station_name:
        Delays_2023["Station"] = Delays_2023["Station"].replace(station_name, station_name[:station_name.index(" TO ")])
    if "(TO " in station_name:
        Delays_2023["Station"] = Delays_2023["Station"].replace(station_name, station_name[:station_name.index("(TO ")])

Delays_2023 = Delays_2023.drop(list(Delays_2023.loc[Delays_2023["Station"] == "TORONTO TRANSIT COMMIS"].index))

# Helper functions

obs_station_names = list(Delays_2023["Station"].unique())

def get_alt_station_names(name:str):
    """
    Given a true station name "name", return a list of all recorded station names from the data set that contain "name"
    """
    name = name.upper()
    return list(compress(obs_station_names, [name in obs_station_names[i] for i in range(len(obs_station_names))]))

def drop_duplicates(L:list):
    """
    given a list, return the list with unique entries
    """
    return list(dict.fromkeys(L))

def get_words(s:str):
    """
    given a string s containing a sentence, return a list of strings consisting of each word in the sentence s
    """
    cut = s
    words = []
    if "-" in cut:
        cut = cut[:cut.index("-")] + " " + cut[cut.index("-")+1:]
    while " " in cut:
        i = cut.index(" ")
        words.append(cut[:i])
        cut = cut[i+1:]
    words.append(cut)
    return words

def get_search_words(s:str):
    """
    Given a station name s that consists of multiple words, return the words in the name that are useful for searching.
    Ignore the "st" in names like "St. George station"
    """
    words = get_words(s)[:-1]
    if words[0] == "ST.":
        words = words[1:]
    return words

special_case_search_words = [get_search_words(station_name) for station_name in special_cases]
special_case_search_words[special_case_search_words.index(["QUEEN'S", 'PARK'])].append("QUEENS")
special_cases = list(compress(true_station_names,[" " in station_name[:len(station_name) - len("station")-1] for
    station_name in true_station_names]))
special_cases.extend(list(compress(true_station_names,["-" in station_name for station_name in true_station_names])))
non_special_cases = [station_name for station_name in true_station_names if station_name not in special_cases]

alt_station_names = {}
for station_name in non_special_cases:
    alt_station_names[station_name] = get_alt_station_names(station_name[:len(station_name) - len("station")-1])
alt_station_names
