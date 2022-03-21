import datetime as dt
import requests
import sys
import time

TeamNames = {"ATL": "Atlanta Hawks", "BOS": "Boston Celtics", "CHA": "Charlotte Hornets", "CHI": "Chicago Bulls", "CLE": "Cleveland Cavaliers", 
             "DAL": "Dallas Mavericks", "DEN": "Denver Nuggets", "DET": "Detroit Pistons", "GSW": "Golden State Warriors", 
             "HOU": "Houston Rockets", "IND": "Indiana Pacers", "LAC": "Los Angeles Clippers", "LAL": "Los Angeles Lakers", "MEM": "Memphis Grizzlies", 
             "MIA": "Miami Heat", "MIL": "Milwaukee Bucks", "MIN": "Minnesota Timberwolves", "NOP": "New Orleans Pelicans", 
             "NYK": "New York Knicks", "BKN": "Brooklyn Nets", "OKC": "Oklahoma City Thunder", "ORL": "Orlando Magic", 
             "PHI": "Philadelphia 76ers", "PHO": "Phoenix Suns", "POR": "Portland Trail Blazers", "SAC": "Sacramento Kings", "TOR": "Toronto Raptors", 
             "UTA": "Utah Jazz", "WAS": "Washington Wizards", "SAS": "San Antonio Spurs"}

sdb_url_base = "https://www.thesportsdb.com/api/v1/json/2/searchevents.php?e="

def print_game(game):
    Time_Correction_Hours = 4
    Time_Correction_Minutes = 0
    home = game['hTeam']['triCode']
    away = game['vTeam']['triCode']
    
    
    event_url = sdb_url_base + str(TeamNames[home] + " vs " + TeamNames[away])
    resp_check = False
    while(not resp_check):
        try:
            response = requests.get(event_url).json()
            resp_check = True
        except ValueError:
            time.sleep(0.5)
    event_id = response['event'][0]['idEvent']
    event_date = response['event'][0]['dateEvent']
    event_time = response['event'][0]['strTime'] 
    game_time = dt.datetime.fromisoformat(event_date + " " + event_time) - dt.timedelta(hours=Time_Correction_Hours, minutes=Time_Correction_Minutes) 
    print(f'{home}  -  {away}    Time =  {game_time}')
    print("Event ID = " + str(event_id))
    print()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        input_days = 1
    else:
        input_days = int(sys.argv[1])

    today_dt = dt.date.today()
    date_check = today_dt - dt.timedelta(days=1)
    xdays_dt = str(today_dt + dt.timedelta(days=input_days-1))
    today_dt = str(today_dt)
    Total_Games_In_Day = 0
    num_days = 0

    date_string = str(dt.date.today().year) + str(dt.date.today().month).zfill(2) + str(dt.date.today().day).zfill(2)
    #'https://data.nba.net/prod/v2/20200224/scoreboard.json'
    jsonData = requests.get('https://data.nba.net/prod/v2/'+ date_string + '/scoreboard.json').json()
    print()

    while(num_days < input_days):
        current_day = dt.date.today() + dt.timedelta(days=num_days)
        date_string = str(current_day.year) + str(current_day.month).zfill(2) + str(current_day.day).zfill(2)
        jsonData = requests.get('https://data.nba.net/prod/v2/'+ date_string + '/scoreboard.json').json()
        for game in jsonData['games']:
            
            if(date_check != current_day):
                if(Total_Games_In_Day != 0):
                    print("TOTAL GAMES = " + str(Total_Games_In_Day))
                    Total_Games_In_Day = 0
                print()
                print("                           " + str(current_day) + "                           ")
                print()
                date_check = current_day
            print_game(game)
            
            Total_Games_In_Day += 1
        num_days += 1
    print("TOTAL GAMES = " + str(Total_Games_In_Day))

