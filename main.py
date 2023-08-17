import urllib.request
import json
import urllib.parse as ps
from constants import API_FILE, BASE_URL, SEARCH_DEPTH

def make_query():
    request = urllib.request.Request(base_url+endpoint,
                                     None,
                                     {"Authorization": "Bearer %s" % my_key})
    
    response = urllib.request.urlopen(request).read().decode("utf-8")
    result = json.loads(response)
    return result

print("Trophies (-1 if unknown): ")
trophies = int(input())
print("Player name: ")
player_name = input()
print("Clan name: ")
clan_name = input()

key_file = open(API_FILE)
my_key = key_file.read().rstrip("\n")
base_url = BASE_URL

# note hashes are replaced with %23
endpoint = "/clans/?name="+ps.quote_plus(clan_name)

clan_results = make_query()
depth_counter = 0

for clan in clan_results["items"]:
    endpoint = "/clans/"+ps.quote_plus(clan["tag"])+"/members"
    member_results = make_query()

    for member in member_results["items"]:
        if member["trophies"] == trophies or member["name"] == player_name:
            print("--------------------------")
            print("Name: "+member["name"])
            endpoint = "/players/"+ps.quote_plus(member["tag"])
            player_results = make_query()
            for card in player_results["currentDeck"]:
                print(card["name"]+"|", end="")
            print("\n\n")

    depth_counter += 1
    if depth_counter >= SEARCH_DEPTH:
        break
