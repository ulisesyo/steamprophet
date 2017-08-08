import requests
import time
import json
from bs4 import BeautifulSoup

idx = 0
gamesId = []
with open('games.txt', 'r') as f:
    for l in f:
        gamesId.append(l.strip())
f.closed

with open('sales.tsv', 'w', encoding='utf-8') as f:
    f.write("appid\tprice\tplayers\tvariance players\tmin players\n")
f.closed

with open('sales.tsv', 'a', encoding='utf-8') as f:
    for g in gamesId:
        page = requests.get('http://steamspy.com/api.php?request=appdetails&appid=' + str(g))
        data = json.loads(page.text)
        print("Parsing game: (" + str(data['appid']) + ") " + data['name'])
        # print(page.text)
        
        if (data['appid'] == 999999):
            f.write(str(g)+"\tHidden by developer")
        else:
            # get lower price from steamdb
            steamdb = requests.get('https://steamdb.info/app/' + str(g))
            soup = BeautifulSoup(steamdb.content, 'html.parser')
            dollarPrice = soup.select(".owned")
            print("Lower price: " + str(dollarPrice))
            
            minPlayers = data['players_forever'] - data['players_forever_variance']
            price = 0 if data['price'] == 0 else float(data['price'])/100.0
            f.write(str(g) + "\t" + str(price) + "\t" + str(data['players_forever']) + "\t" + str(data['players_forever_variance']) + "\t" + str(minPlayers) + "\n")
            
        idx = idx + 1
        time.sleep(0.25)
        break
            
f.closed



