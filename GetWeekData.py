import requests
import datetime
from bs4 import BeautifulSoup

allGamesGot = False
daysToFilter = datetime.timedelta(days=6)
currentDate = datetime.date.today()
lastDate = currentDate + daysToFilter;
currentPage = 1
idx = 0

with open('data.tsv', 'w', encoding='utf-8') as f:
    f.write("#\tAppid\tName\tSteam URL\tDate\tSteamspy URL\tFirst week score\tSecond week score\tThird week score\tFourth week score\n")
f.closed

appids = []
while (not allGamesGot):
    page = requests.get('http://store.steampowered.com/search/?tags=492&filter=comingsoon&page=' + str(currentPage))
    soup = BeautifulSoup(page.content, 'html.parser')
    data = soup.select(".search_result_row")

    with open('data.tsv', 'a', encoding='utf-8') as f:
        for row in data:
            url = row.get('href')
            appid = row.get('data-ds-appid')
            name = row.select(".search_name .title")[0].string
            releasedDate = row.select(".search_released")[0].string

            try:
                realReleaseDate = datetime.datetime.strptime(releasedDate, '%d %b, %Y')

                if (realReleaseDate.date() > lastDate):
                    allGamesGot = True;
                    continue
            except ValueError:
                continue
            except TypeError:
                continue
                
            appids.append(appid)
            print(idx, "\t", name, "\t", url, "\t", realReleaseDate, "\t", appid, "")
            f.write(str(idx) + "\t" + appid + "\t" + name + "\t" + url + "\t" + str(realReleaseDate.date()) + "\thttp://www.steamspy.com/app/" + str(appid) + "\n")
            idx = idx + 1
    f.closed
    currentPage = currentPage+1


