# APIs

https://api.sofascore.com/api/v1/player/{player-id}/unique-tournament/11653/season/48017/statistics/overall
https://api.sofascore.com/api/v1/team/{team-id}/players

## all
https://api.sofascore.com/api/v1/event/10961781/odds/1/all

Home Team = ['markets'][16]['choices'][0]['name']
Away Team = ['markets'][16]['choices'][2]['name']

## statiscs
https://api.sofascore.com/api/v1/event/10961781/statistics

Expected Goals Home = ['statistics'][0]['groups'][0]['statisticsItems'][0]['homeValue']
Expected Goals Away = ['statistics'][0]['groups'][0]['statisticsItems'][0]['awayValue']

Posession Home = ['statistics'][0]['groups'][1]['statisticsItems'][0]['homeValue']
Posession Away = ['statistics'][0]['groups'][1]['statisticsItems'][0]['awayValue']

Total Shots Home = ['statistics'][0]['groups'][2]['statisticsItems'][0]['homeValue']
Total Shots Away = ['statistics'][0]['groups'][2]['statisticsItems'][0]['awayValue']

Shots on Target Home = ['statistics'][0]['groups'][2]['statisticsItems'][1]['homeValue']
Shots on Target Away = ['statistics'][0]['groups'][2]['statisticsItems'][1]['awayValue']

Shots off Target Home = ['statistics'][0]['groups'][2]['statisticsItems'][2]['homeValue']
Shots off Target Away = ['statistics'][0]['groups'][2]['statisticsItems'][2]['awayValue']

Blocked shots Home = ['statistics'][0]['groups'][2]['statisticsItems'][3]['homeValue']
Blocked shots Away = ['statistics'][0]['groups'][2]['statisticsItems'][3]['awayValue']

Corner kicks Home = ['statistics'][0]['groups'][3]['statisticsItems'][0]['homeValue']
Corner kicks Away = ['statistics'][0]['groups'][3]['statisticsItems'][0]['awayValue']

Offsides Home = ['statistics'][0]['groups'][3]['statisticsItems'][1]['homeValue']
Offsides Away = ['statistics'][0]['groups'][3]['statisticsItems'][1]['awayValue']

Fouls Home = ['statistics'][0]['groups'][3]['statisticsItems'][2]['homeValue']
Fouls Away = ['statistics'][0]['groups'][3]['statisticsItems'][2]['awayValue']

Yellow Cards Home = ['statistics'][0]['groups'][3]['statisticsItems'][3]['homeValue']
Yellow Cards Away = ['statistics'][0]['groups'][3]['statisticsItems'][3]['awayValue']

Red Cards Home = ['statistics'][0]['groups'][3]['statisticsItems'][4]['homeValue']
Red Cards Away = ['statistics'][0]['groups'][3]['statisticsItems'][4]['awayValue']

Free Kicks Home = ['statistics'][0]['groups'][3]['statisticsItems'][5]['homeValue']
Free Kicks Away = ['statistics'][0]['groups'][3]['statisticsItems'][5]['awayValue']

Throw-ins Home = ['statistics'][0]['groups'][3]['statisticsItems'][6]['homeValue']
Throw-ins Away = ['statistics'][0]['groups'][3]['statisticsItems'][6]['awayValue']

Goal Kicks Home = ['statistics'][0]['groups'][3]['statisticsItems'][7]['homeValue']
Goal Kicks Away = ['statistics'][0]['groups'][3]['statisticsItems'][7]['awayValue']

Shots Inside Box Home = ['statistics'][0]['groups'][4]['statisticsItems'][0]['homeValue']
Shots Inside Box Away = ['statistics'][0]['groups'][4]['statisticsItems'][0]['awayValue']

Shots Outside Box Home = ['statistics'][0]['groups'][4]['statisticsItems'][1]['homeValue']
Shots Outside Box Away = ['statistics'][0]['groups'][4]['statisticsItems'][1]['awayValue']

Goalkeeper Saves Home = ['statistics'][0]['groups'][4]['statisticsItems'][2]['homeValue']
Goalkeeper Saves Away = ['statistics'][0]['groups'][4]['statisticsItems'][2]['awayValue']

Passes Home = ['statistics'][0]['groups'][5]['statisticsItems'][0]['homeValue']
Passes Away = ['statistics'][0]['groups'][5]['statisticsItems'][0]['awayValue']

Accurate Passes Home = ['statistics'][0]['groups'][5]['statisticsItems'][1]['homeValue']
Accurate Passes Away = ['statistics'][0]['groups'][5]['statisticsItems'][1]['awayValue']

Long Balls Home = ['statistics'][0]['groups'][5]['statisticsItems'][2]['homeTotal']
Long Balls Away = ['statistics'][0]['groups'][5]['statisticsItems'][2]['awayTotal']

Crosses Home = ['statistics'][0]['groups'][5]['statisticsItems'][3]['homeTotal']
Crosses Away = ['statistics'][0]['groups'][5]['statisticsItems'][3]['awayTotal']

Dribbles Home = ['statistics'][0]['groups'][6]['statisticsItems'][0]['homeTotal']
Dribbles Away = ['statistics'][0]['groups'][6]['statisticsItems'][0]['awayTotal']

Possesion Lost Home = ['statistics'][0]['groups'][6]['statisticsItems'][1]['homeValue']
Possesion Lost Away = ['statistics'][0]['groups'][6]['statisticsItems'][1]['awayValue']

Duels Won Home = ['statistics'][0]['groups'][6]['statisticsItems'][2]['homeValue']
Duels Won Away = ['statistics'][0]['groups'][6]['statisticsItems'][2]['awayValue']

Aerials Won Home = ['statistics'][0]['groups'][6]['statisticsItems'][3]['homeValue']
Aerials Won Away = ['statistics'][0]['groups'][6]['statisticsItems'][3]['awayValue']

Tackles Home = ['statistics'][0]['groups'][7]['statisticsItems'][0]['homeValue']
Tackles Away = ['statistics'][0]['groups'][7]['statisticsItems'][0]['awayValue']

Interceptions Home = ['statistics'][0]['groups'][7]['statisticsItems'][1]['homeValue']
Interceptions Away = ['statistics'][0]['groups'][7]['statisticsItems'][1]['awayValue']

Clearences Home = ['statistics'][0]['groups'][7]['statisticsItems'][2]['homeValue']
Clearences Away = ['statistics'][0]['groups'][7]['statisticsItems'][2]['awayValue']

## incidents
https://api.sofascore.com/api/v1/event/10961803/incidents

Home Score = ['incidents'][0]['homeScore']
Away Score = ['incidents'][0]['awayScore']
