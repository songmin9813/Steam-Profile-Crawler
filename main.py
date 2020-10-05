import re
import requests
import json
import time


def print_steam_crawl(steamID,ID_Range,fileNum):
    userCount=int(fileNum)
    for n in range(ID_Range):
        time.sleep(20)
        steamID=steamID+1
        string_ID=str(steamID)
        url='https://steamcommunity.com/profiles/'+string_ID+'/games/?tab=all&sort=playtime'
        try: #private user check
            html=requests.get(url).text
            if 'profile_fatalerror' in html:
                steamID=steamID-1
                print("427 Error")
                time.sleep(1800)
                continue
            htmlSearch=re.search(r'var rgGames =(.+?);',html,re.S)
            gameList=htmlSearch.group(1)
            SteamGame=json.loads(gameList)
        except:
            continue
        if(str(SteamGame)!="[]" and 'hours_forever' in gameList):
            userCount=userCount+1
            f=open('C:/Users/mitha/OneDrive/바탕 화면/dev/'+str(userCount)+'.csv','w')
            f.write('GameName,Id:'+string_ID+'\n')
            for course in SteamGame:
                try: #empty playtime check
                    gameName='{name}'.format(**course)
                    gameName=gameName.replace(',',' ')#if comma inside gamename, replace space
                    gameTime='{hours_forever}'.format(**course)
                    gameTime=gameTime.replace(',',' ')
                    f.write(gameName+','+gameTime+'\n')
                except:
                    continue
            f.close()
        else:
            continue


            pages=100000
            now=datetime.now()
            print_steam_crawl(76561197960265728,pages,0)
            #https://steamcommunity.com/profiles/76561198120029537/games/?tab=all&sort=playtime->test 427 error
            #76561197960265728 first steam user profiles


