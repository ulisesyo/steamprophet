import requests
import time
import json
import re
from bs4 import BeautifulSoup

idx = 0
gamesId = []
with open('games.txt', 'r') as f:
    for l in f:
        gamesId.append(l.strip())
f.closed

with open('sales.tsv', 'w', encoding='utf-8') as f:
    f.write("appid\tprice\tplayers\tplayers_variance\tmin players\tmin price\tearning estimation\n")
f.closed

with open('sales.tsv', 'a', encoding='utf-8') as f:
    for g in gamesId:
        page = requests.get('http://steamspy.com/api.php?request=appdetails&appid=' + str(g))
        data = json.loads(page.text)
        print("Parsing game: (" + str(data['appid']) + ") " + str(data['name']))
        # print(page.text)
        
        if (data['appid'] == 999999):
            f.write(str(g)+"\tHidden by developer")
        else:
            minPlayers = data['players_forever'] - data['players_forever_variance']
            minPlayers = 0 if minPlayers < 0 else minPlayers
            price = 0 if data['price'] == None or data['price'] == 0 else float(data['price'])/100.0

            # get lower price from steamdb
            try:
                steamdb = requests.get('https://steamdb.info/app/' + str(g))
                soup = BeautifulSoup(steamdb.content, 'html.parser')
                dollarPrice = soup.select(".owned")[1].select("td")[3].text
                priceAndDiscount = re.findall(r'[+-]?[0-9.]+', str(dollarPrice))
            except:
                f.write(str(g) + "\t" + "{0:.2f}".format(price) + "\t" + str(data['players_forever']) + "\t" + str(data['players_forever_variance']) + "\t" + str(minPlayers) + "\t0\t0\tError at steamdb\n")
                continue

            if price > 0:
                estimation = float(priceAndDiscount[0])*int(minPlayers)
                print("Lower price: " + str(priceAndDiscount[0]) + "-> Estimation: " + "{0:.2f}".format(estimation))
                f.write(str(g) + "\t" + "{0:.2f}".format(price) + "\t" + str(data['players_forever']) + "\t" + str(data['players_forever_variance']) + "\t" + str(minPlayers) + "\t" + str(priceAndDiscount[0]) + "\t" + "{0:.2f}".format(estimation) + "\n")
            else:
                f.write(str(g) + "\tF2P\n")
        idx = idx + 1
        time.sleep(0.25)
            
f.closed



