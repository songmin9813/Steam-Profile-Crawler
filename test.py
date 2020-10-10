import re
import requests
import json
from bs4 import BeautifulSoup
import time


def print_steam_crawl(steamID,ID_Range,fileNum):
    for n in range(ID_Range):
        #time.sleep(20)
        steamID=steamID+1
        print('current data:', steamID ,'\n')
        string_ID=str(steamID)
        url='https://steamcommunity.com/profiles/'+string_ID+'/games/?tab=all&sort=playtime'
        try: #private user check
            html=requests.get(url).text
            if 'profile_fatalerror' in html:
                steamID=steamID-1
                print("427 Error")
                #time.sleep(1800)
                continue
            htmlSearch=re.search('var rgGames =(.+?);',html,re.S)
            gameList=htmlSearch.group(1)
            SteamGame=json.loads(gameList)
        except:
            continue
        if(str(SteamGame)!="[]" and 'hours_forever' in gameList):
            f=open('C:/Users/mitha/OneDrive/바탕 화면/dev/Crawling_Data/'+string_ID+'.csv','w')
            f.write('GameName,Id:'+string_ID+'\n')
            for course in SteamGame:
                try: #empty playtime check
                    gameName='{name}'.format(**course)
                    gameName=gameName.replace(',',' ')#if comma inside gamename, replace space
                    gameTime='{hours_forever}'.format(**course)
                    gameTime=gameTime.replace(',',' ')
                    #if(float(gameTime)>=3.0):
                    f.write(gameName+','+gameTime+'\n')
                except:
                    continue
        else:
            continue
        html = requests.get('https://steamcommunity.com/profiles/'+string_ID+'/games/?tab=recent').text
        htmlSearch = re.search('var rgGames =(.+?);', html, re.S)
        gameList = htmlSearch.group(1)
        SteamGame = json.loads(gameList)
        if (str(SteamGame) != "[]" and 'hours' in gameList):
            f.write('\n'+'Recently Played'+'\n')
            for course in SteamGame:
                try: #empty playtime check
                    gameName='{name}'.format(**course)
                    gameName=gameName.replace(',',' ')#if comma inside gamename, replace space
                    gameTime='{hours}'.format(**course)
                    gameTime=gameTime.replace(',',' ')
                    #if(float(gameTime)>=3.0):
                    f.write(gameName+','+gameTime+'\n')
                except:
                    continue
        f.write('\n')
        html = requests.get('https://steamcommunity.com/profiles/' + string_ID).text
        soup=BeautifulSoup(html,"html.parser")
        total=soup.select("span.profile_count_link_total")
        namevalue=soup.select("span.count_link_label")
        for key in namevalue:
            try:
                sentencevalue = key.text.join(key.text.split())
                f.write(sentencevalue+',')
            except:
                continue
        f.write('\n')
        for key in total:
            try:
                sentence = key.text.join(key.text.split())
                if(sentence==''):
                    sentence='0'
                f.write(sentence+',')
            except:
                continue
        f.close()


pages=1
print_steam_crawl(76561198048511277,pages,0)
#https://steamcommunity.com/profiles/76561198120029537/games/?tab=all&sort=playtime->test 427 error
#76561197960265728 first steam user profiles


