import re
import requests
import json
import time


def print_steam_crawl(steamID,ID_Range,fileNum):
    for n in range(ID_Range):
        userCount = 0
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
            htmlSearch=re.search(r'var rgGames =(.+?);',html,re.S)
            print(htmlSearch)
            gameList=htmlSearch.group(1)
            #print(gameList)
            SteamGame=json.loads(gameList)
            #print(SteamGame)
        except:
            continue
        if(str(SteamGame)!="[]" and 'hours_forever' in gameList):
            userCount=userCount+1
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
                    userCount = userCount + 1
                except:
                    userCount = userCount + 1
                    continue
            f.write('\n'+'Counted Games'+','+str(userCount)+'\n')
        else:
            continue
        html = requests.get('https://steamcommunity.com/profiles/'+string_ID+'/games/?tab=recent').text
        htmlSearch = re.search(r'var rgGames =(.+?);', html, re.S)
        print(htmlSearch)
        gameList = htmlSearch.group(1)
        SteamGame = json.loads(gameList)
        print(SteamGame)
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
        f.close()
        #f.write(str(userCount)+'\n')


pages=1
#now=datetime.now()
print_steam_crawl(76561198048511277,pages,0)
#https://steamcommunity.com/profiles/76561198120029537/games/?tab=all&sort=playtime->test 427 error
#76561197960265728 first steam user profiles


