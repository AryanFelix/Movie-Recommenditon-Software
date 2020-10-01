import json
import requests
import os
from dotenv import load_dotenv

tdkey = os.getenv("TASTEDIVE_KEY")
omdbkey = os.getenv("OMDB_KEY")

def get_movies_from_tastedive(s):
    baseurl = "https://tastedive.com/api/similar"
    paramlist = {}
    paramlist["q"] = s
    paramlist["type"] = "movies"
    paramlist["limit"] = 5
    paramlist["k"] = tdkey
    result = requests.get(baseurl, params = paramlist)
    result = result.json()
    return result
    
def extract_movie_titles(res):
    temp = []
    for x in res["Similar"]["Results"]:
        temp.append(x["Name"])
    return temp

def get_related_titles(l):
    related = []
    for x in l:
        temp = get_movies_from_tastedive(x)
        temp = extract_movie_titles(temp)
        related.append(temp)
    final = []
    for x in related:
        for y in x:
            if y not in final:
                final.append(y)
    return final

def get_movie_data(s):
    baseurl = "http://www.omdbapi.com/"
    paramlist = {}
    paramlist["t"] = s
    paramlist["r"] = "json"
    paramlist["apikey"] = omdbkey
    result = requests.get(baseurl, params = paramlist)
    result = result.json()
    return result

def get_movie_rating(res):
    rat = 0
    for x in res["Ratings"]:
        if x["Source"] == "Rotten Tomatoes":
            rat = x['Value']
            rat = rat[:-1]
            rat = int(rat)
    return rat

def get_sorted_recommendations(l):
    tits = []
    rats = []
    rel = get_related_titles(l)
    for x in rel:
        tits.append(x)
        rats.append(get_movie_rating(get_movie_data(x)))
    final = list(zip(tits,rats))
    final.sort(reverse = True, key = lambda a: (a[1],a[0]))
    finalnew = []
    for x in final:
        finalnew.append(x[0])
    return finalnew

print("WELCOME TO MOVIE RECOMMENDATION SYSTEM")
print("Feeling bored? Well we are here to help!")
recomlist = []
ch = ""
print("Keep entering movies. Enter -1 to stop.")
print("Enter movie titles the same as the actual movies.")
while ch != "-1":
    ch = input("Enter movie title : ")
    recomlist.append(ch)
recoms = get_sorted_recommendations(recomlist)
print("Your recommended movies are :")
for i in range(len(recoms)):
    print("{}. {}".format(i+1, recoms[i]))