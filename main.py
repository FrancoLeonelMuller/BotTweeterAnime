import tweepy
import json
import requests
from datetime import datetime
import time


def writeLog(timestamp, logName, text, ):
    f = open(f"./Logs/{logName}", "a")
    f.write("\n")
    f.write(str(timestamp))
    f.write(" | ")
    f.write(str(text))
    f.close()
    return f"{timestamp} | {logName} | {text}"


def getLastEP_AnimeFLV(url):
    try:
        response = requests.get(url).text
        episodes = response[response.find("var episodes = ")+15:response.find("]];")+2]
        episodes = episodes.replace('[','')
        episodes = episodes.replace(']','')
        episodes = episodes.split(',')
        writeLog(datetime.now(), "AnimeFLV", "Success get episode")
        return int(episodes[0])
    except:
        writeLog(datetime.now(), "AnimeFLV", "Error get episode")
        return 0

def getLastEP_PorygonSubs(url):
    try:
        response = requests.get(url).text
        indPosCap = response.find("<strong>Capítulos: </strong>")
        episodes = response[indPosCap+28:indPosCap+31]
        writeLog(datetime.now(), "PorygonSubs", "Success get episode")
        return int(episodes)
    except:
        writeLog(datetime.now(), "PorygonSubs", "Error get episode")
        return 0

def enviarTweetBot(msgText):
    f = open('apiKey.txt')
    apiKey = json.load(f)
    f.close()
    api_key = apiKey['api_key']
    api_secret = apiKey['api_secret']
    bearer_token = apiKey['bearer_token']
    access_token = apiKey['access_token']
    access_token_secret = apiKey['access_token_secret']


    try:
        client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)
        auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
        api = tweepy.API(auth)
        writeLog(datetime.now(), "TwitterBot", "Success Bot Connect")
        client.create_tweet(text = msgText)
        writeLog(datetime.now(), "TwitterBot", "Success Bot tweet")
    except:
        writeLog(datetime.now(), "TwitterBot", "Error Bot Connect")

        
        
        
     
        

dayWeek = datetime.now().strftime('%A')
f = open('AnimeID.txt')
data = json.load(f)
f.close()

########    Reset de Week_Release Monday a 6AM   ########
timeNow = datetime.now()
time6am = timeNow.replace(hour=6, minute=0, second=0, microsecond=0)
time7am = timeNow.replace(hour=7, minute=0, second=0, microsecond=0)
if(dayWeek == "Monday" and timeNow > time6am and timeNow < time7am):
    for i in range(len(data)):
        data[i]['Week_Released'] = "false"
##########################################################


for i in range(len(data)):
    if(data[i]['Week_Released'] == "false"):
        data[i]['Week_Released'] = False
        
    if dayWeek == data[i]['Day'] and data[i]['Week_Released'] == False:
        print("En dia")
        lastEP = getLastEP_AnimeFLV(data[i]['AnimeFLV_URL'])
        if lastEP != data[i]['Current_EP']:
            data[i]['Current_EP'] = lastEP
            data[i]['Week_Released'] = "true"
            print("Salio")


            msgTwitter = f"El episodio {data[i]['Current_EP']}/{data[i]['Total_Ep']} de {data[i]['Anime']} salio. \n"
            msgTwitter += f"{data[i]['Crunchy_URL']}"

            enviarTweetBot(msgTwitter)

            jsonData = str(data).replace("'",'"')
            jsonData = jsonData.replace('True','true')
            jsonData = jsonData.replace('False','false')
            f = open("AnimeID.txt", "w")
            f.write(jsonData)
            f.close()
    
