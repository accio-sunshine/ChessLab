#Library details
import csv
import requests
import json
import datetime; datetime.datetime.utcfromtimestamp
import gspread
from oauth2client.service_account import ServiceAccountCredentials

#Variable definitions
username = input("Enter your chess.com username : ")
google_sheet_link = input ("Copy and paste the series of numbers and letters between the /d/ and /edit in your Google Sheet's URL : ")
url= " https://api.chess.com/pub/player/"+ username + "/games/archives"
response_0 = requests.get(url)
arch = json.loads(response_0.content)
m = arch["archives"]
k=1
p=0
n=0

#To store data in the local computer
with open('chess_master.csv', mode='w', newline='') as csv_file:
    fieldnames = ['match_number', 'white_player', 'res_w','extra_w','black_player','res_b','extra_b','date','final_moves']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    while (p < len(m)):
        response = requests.get(m[p])
        data_1 = json.loads(response.content)
        l = data_1["games"]
        while (n < len(l)):
            ts_epoch = l[n]["end_time"]
            ts = datetime.datetime.fromtimestamp(ts_epoch).strftime('%Y-%m-%d %H:%M:%S')
            if (l[n]["white"]["result"]) == "win" :
                res_wh = 'win'
                res_bl = 'lost'
            elif ((l[n]["white"]["result"]) == "draw" or (l[n]["white"]["result"]) == "repetition" or (l[n]["white"]["result"]) == "agreed" or (l[n]["white"]["result"]) == "50move" or (l[n]["white"]["result"]) == "timevsinsufficient"):
                res_wh = 'draw'
                res_bl = 'draw'
            else:
                res_wh = 'lost'
                res_bl = 'win'
            writer.writerow({'match_number': k, 'white_player': l[n]["white"]["username"], 'res_w': res_wh, 'extra_w': l[n]["white"]["result"], 'black_player': l[n]["black"]["username"], 'res_b': res_bl, 'extra_b': l[n]["black"]["result"], 'date': ts, 'final_moves': l[n]["fen"]})
            k= k+1
            n = n+1
        p=p+1
n=0

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

content = open('chess_master.csv', 'r').read()
client.import_csv(google_sheet_link, content) #Google sheet link address

cont = input("Do you want to get stats with a particular opponent (Y/N)? : ")
if cont == "N" :
    print ("Completed, have fun!")
elif cont =="Y" :
    opponent = input("Enter your OPPONENT'S chess.com username : ")
    google_sheet_link_1 = input ("Copy and paste the series of numbers and letters between the /d/ and /edit in your Google Sheet's URL : ")
    with open('Battles.csv', mode='w', newline='') as csv_file:
        fieldnames = ['match_number', 'white_player', 'res_w','extra_w','black_player','res_b','extra_b','date','final_moves']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        p=0
        k=1
        while (p < len(m)):
            response = requests.get(m[p])
            data_1 = json.loads(response.content)
            l = data_1["games"]
            while (n < len(l)):
                ts_epoch = l[n]["end_time"]
                ts = datetime.datetime.fromtimestamp(ts_epoch).strftime('%Y-%m-%d %H:%M:%S')
                if (l[n]["white"]["result"]) == "win" :
                    res_wh = 'win'
                    res_bl = 'lost'
                elif ((l[n]["white"]["result"]) == "draw" or (l[n]["white"]["result"]) == "repetition" or (l[n]["white"]["result"]) == "agreed" or (l[n]["white"]["result"]) == "50move" or (l[n]["white"]["result"]) == "timevsinsufficient"):
                    res_wh = 'draw'
                    res_bl = 'draw'
                else:
                    res_wh = 'lost'
                    res_bl = 'win'
                if ((l[n]["white"]["username"]) == opponent )or((l[n]["black"]["username"]) == opponent):    
                    writer.writerow({'match_number': k, 'white_player': l[n]["white"]["username"], 'res_w': res_wh, 'extra_w': l[n]["white"]["result"], 'black_player': l[n]["black"]["username"], 'res_b': res_bl, 'extra_b': l[n]["black"]["result"], 'date': ts, 'final_moves': l[n]["fen"]})
                    k= k+1
                n = n+1
            p=p+1
    n=0
    scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    content = open('Battles.csv', 'r').read()
    client.import_csv(google_sheet_link_1, content) #Google sheet link address
    print ("Completed,have fun!")
        

            

     
