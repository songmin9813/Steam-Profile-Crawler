import re
import requests
import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def print_steam_crawl(steamID, ID_Range, fileNum):
    for n in range(ID_Range):
        time.sleep(20)
        steamID = steamID + 1
        print('current data:', steamID, '\n')
        string_ID = str(steamID)
        url = 'https://steamcommunity.com/profiles/' + string_ID + '/games/?tab=all&sort=playtime'
        try:  # private user check
            html = requests.get(url).text
            if 'profile_fatalerror' in html:
                steamID = steamID - 1
                print("427 Error")
                time.sleep(1800)
                continue
            htmlSearch = re.search('var rgGames =(.+?);', html, re.S)
            gameList = htmlSearch.group(1)
            SteamGame = json.loads(gameList)
        except:
            continue
        if (str(SteamGame) != "[]" and 'hours_forever' in gameList):
            f = open('Crawling_Data/'+string_ID + '.csv', 'w')
            f.write('GameName,Id:' + string_ID + '\n')
            for course in SteamGame:
                try:  # empty playtime check
                    gameName = '{name}'.format(**course)
                    gameName = gameName.replace(',', ' ')  # if comma inside gamename, replace space
                    gameTime = '{hours_forever}'.format(**course)
                    gameTime = gameTime.replace(',', '')
                    # gameData='{logo}'.format(**course)
                    # gameData=gameData[50:-19]
                    # html=requests.get('https://store.steampowered.com/app/'+gameData).text
                    # soup = BeautifulSoup(html, "html.parser")
                    # realsedate = soup.select("div.date")
                    # print(realsedate)
                    # if(float(gameTime)>=3.0):
                    f.write(gameName + ',' + gameTime + '\n')
                except:
                    continue
        else:
            continue
        html = requests.get('https://steamcommunity.com/profiles/' + string_ID + '/games/?tab=recent').text
        htmlSearch = re.search('var rgGames =(.+?);', html, re.S)
        gameList = htmlSearch.group(1)
        SteamGame = json.loads(gameList)
        if (str(SteamGame) != "[]" and 'hours' in gameList):
            f.write('\n' + 'Recently Played' + '\n')
            for course in SteamGame:
                try:  # empty playtime check
                    gameName = '{name}'.format(**course)
                    gameName = gameName.replace(',', ' ')  # if comma inside gamename, replace space
                    gameTime = '{hours}'.format(**course)
                    gameTime = gameTime.replace(',', ' ')
                    # if(float(gameTime)>=3.0):
                    f.write(gameName + ',' + gameTime + '\n')
                except:
                    continue
        f.write('\n')
        html = requests.get('https://steamcommunity.com/profiles/' + string_ID).text
        soup = BeautifulSoup(html, "html.parser")
        total = soup.select("span.profile_count_link_total")
        namevalue = soup.select("span.count_link_label")
        for key in namevalue:
            try:
                sentencevalue = key.text.join(key.text.split())
                f.write(sentencevalue + ',')
            except:
                continue
        f.write('Wishlist\n')
        for key in total:
            try:
                sentence = key.text.join(key.text.split())
                if (sentence == ''):
                    sentence = '0'
                f.write(sentence + ',')
            except:
                continue
        options=webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('disable-gpu')
        driver=webdriver.Chrome('chromedriver',options=options)
        driver.get('https://www.steamwishlistcalculator.com/?id=' + string_ID+'&currency=US')
        element=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,'titleCount')))
        f.write(element.text)
        #soup = BeautifulSoup(html, "html.parser")
        #wishlist = soup.find({'id':'titleCount'})
        #print(wishlist)
        f.close()

profileNum=int(input('input start id: '))
pages = int(input('how many pages?: '))
print_steam_crawl(profileNum, pages, 0)
# https://steamcommunity.com/profiles/76561198120029537/games/?tab=all&sort=playtime->test 427 error
# 76561197960265728 first steam user profiles, 76561198261943701 showmkk LOL, 76561198048511278 ME
