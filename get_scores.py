import datetime as dt
import requests
import sys
import time

if __name__ == "__main__":
    if len(sys.argv) == 1:
        input_days = 1
    else:
        input_days = int(sys.argv[1])

    today_dt = dt.date.today()
    date_check = today_dt - dt.timedelta(days=1)
    Total_Games_In_Day = 0
    num_days = 0

    date_string = str(dt.date.today().year) + str(dt.date.today().month).zfill(2) + str(dt.date.today().day).zfill(2)
    #'https://data.nba.net/prod/v2/20200224/scoreboard.json'
    jsonData = requests.get('https://data.nba.net/prod/v2/'+ date_string + '/scoreboard.json').json()
    print()

    while(num_days < input_days):
        current_day = dt.date.today() - dt.timedelta(days=num_days)
        date_string = str(current_day.year) + str(current_day.month).zfill(2) + str(current_day.day).zfill(2)
        jsonData = requests.get('https://data.nba.net/prod/v2/'+ date_string + '/scoreboard.json').json()
        
        for game in jsonData['games']:
            home = game['hTeam']['triCode']
            away = game['vTeam']['triCode']

            home_score = game['hTeam']['score']
            away_score = game['vTeam']['score']
            
            if(date_check != current_day):
                if(Total_Games_In_Day != 0):
                    print("TOTAL GAMES = " + str(Total_Games_In_Day))
                    Total_Games_In_Day = 0
                print()
                print("                           " + str(current_day) + "                           ")
                print()
                date_check = current_day

            if(home_score != '' and away_score != ''):
                home_score = int(home_score)  
                away_score = int(away_score)  
                if(home_score > away_score):
                    print(f'W {home} {home_score}  -  L {away} {away_score}')
                elif(away_score > home_score):
                    print(f'W {away} {away_score} - L {home} {home_score}')
            else:
                print(f'{home} - {away} is not complete yet')
            
            Total_Games_In_Day += 1
        
        num_days += 1
    print("TOTAL GAMES = " + str(Total_Games_In_Day))
		
