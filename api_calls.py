import requests
import json
import csv

url_all = 'https://api.sofascore.com/api/v1/event/{id_partido}/odds/1/all'
url_statistics = 'https://api.sofascore.com/api/v1/event/{id_partido}/statistics'
url_incidents = 'https://api.sofascore.com/api/v1/event/{id_partido}/incidents'
headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

# TODO: Obtener el id de los partidos
ids = []

with open('ids.txt', 'r') as file:
    for row in file:
        ids.append(row.strip())

headers_csv = ["team_home", "team_away", "score_home", "score_away", "expected_goals_home", 
               "expected_goals_away", "posession_home", "posession_away", "total_shots_home", 
               "total_shots_away", "shots_on_target_home", "shots_on_target_away", 
               "shots_off_target_home", "shots_off_target_away", "blocked_shots_home", 
               "blocked_shots_away", "corner_kicks_home", "corner_kicks_away", "offsides_home", 
               "offsides_away", "fouls_home", "fouls_away", "yellow_cards_home", "yellow_cards_away", 
               "red_cards_home", "red_cards_away", "free_kicks_home", "free_kicks_away", 
               "throw_ins_home", "throw_ins_away", "goal_kicks_home", "goal_kicks_away", 
               "shots_inside_box_home", "shots_inside_box_away", "shots_outside_box_home", 
               "shots_outside_box_away", "goalkeeper_saves_home", "goalkeeper_saves_away", 
               "passes_home", "passes_away", "accurate_passes_home", "accurate_passes_away", 
               "long_balls_home", "long_balls_away", "crosses_home", "crosses_away", 
               "dribbles_home", "dribbles_away", "possesion_lost_home", "possesion_lost_away", 
               "duels_won_home", "duels_won_away", "aerials_won_home", "aerials_won_away", 
               "tackles_home", "tackles_away", "interceptions_home", "interceptions_away", 
               "clearences_home", "clearences_away"]

estadisticas = []

with open('estadisticas_partidos.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers_csv)

    for id in ids:
    # TODO: Obtener Nombre de los equipos
        response_all = requests.get(url_all.format(id_partido=id),
                                    headers=headers)
        if response_all.status_code == 200:
            all = json.loads(response_all.text)
            length = len(all['markets'])
            home_team = all['markets'][length - 1]['choices'][0]['name']
            away_team = all['markets'][length - 1]['choices'][2]['name']

    # TODO: Obtener Goles de los equipos
        response_incidents = requests.get(url_incidents.format(id_partido=id),
                                        headers=headers)
        if response_incidents.status_code == 200:
            incidents = json.loads(response_incidents.text)
            home_score = incidents['incidents'][0]['homeScore']
            away_score = incidents['incidents'][0]['awayScore']


    # TODO: Obtener Estadísticas de los equipos
        response_statistics = requests.get(url_statistics.format(id_partido=id),
                                        headers=headers)
        if response_statistics.status_code == 200:
            statistics = json.loads(response_statistics.text)
            
            expected_goals_home = statistics['statistics'][0]['groups'][0]['statisticsItems'][0]['homeValue']
            expected_goals_away = statistics['statistics'][0]['groups'][0]['statisticsItems'][0]['awayValue']

            posession_home = statistics['statistics'][0]['groups'][1]['statisticsItems'][0]['homeValue']
            posession_away = statistics['statistics'][0]['groups'][1]['statisticsItems'][0]['awayValue']

            total_shots_home = statistics['statistics'][0]['groups'][2]['statisticsItems'][0]['homeValue']
            total_shots_away = statistics['statistics'][0]['groups'][2]['statisticsItems'][0]['awayValue']

            shots_on_target_home = statistics['statistics'][0]['groups'][2]['statisticsItems'][1]['homeValue']
            shots_on_target_away = statistics['statistics'][0]['groups'][2]['statisticsItems'][1]['awayValue']

            shots_off_target_home = statistics['statistics'][0]['groups'][2]['statisticsItems'][2]['homeValue']
            shots_off_target_away = statistics['statistics'][0]['groups'][2]['statisticsItems'][2]['awayValue']

            blocked_shots_home = statistics['statistics'][0]['groups'][2]['statisticsItems'][3]['homeValue']
            blocked_shots_away = statistics['statistics'][0]['groups'][2]['statisticsItems'][3]['awayValue']

            if len(statistics['statistics'][0]['groups'][3]['statisticsItems']) == 8:

                corner_kicks_home = statistics['statistics'][0]['groups'][3]['statisticsItems'][0]['homeValue']
                corner_kicks_away = statistics['statistics'][0]['groups'][3]['statisticsItems'][0]['awayValue']

                offsides_home = statistics['statistics'][0]['groups'][3]['statisticsItems'][1]['homeValue']
                offsides_away = statistics['statistics'][0]['groups'][3]['statisticsItems'][1]['awayValue']

                fouls_home = statistics['statistics'][0]['groups'][3]['statisticsItems'][2]['homeValue']
                fouls_away = statistics['statistics'][0]['groups'][3]['statisticsItems'][2]['awayValue']

                yellow_cards_home = statistics['statistics'][0]['groups'][3]['statisticsItems'][3]['homeValue']
                yellow_cards_away = statistics['statistics'][0]['groups'][3]['statisticsItems'][3]['awayValue']

                red_cards_home = statistics['statistics'][0]['groups'][3]['statisticsItems'][4]['homeValue']
                red_cards_away = statistics['statistics'][0]['groups'][3]['statisticsItems'][4]['awayValue']

                free_kicks_home = statistics['statistics'][0]['groups'][3]['statisticsItems'][5]['homeValue']
                free_kicks_away = statistics['statistics'][0]['groups'][3]['statisticsItems'][5]['awayValue']

                throw_ins_home = statistics['statistics'][0]['groups'][3]['statisticsItems'][6]['homeValue']
                throw_ins_away = statistics['statistics'][0]['groups'][3]['statisticsItems'][6]['awayValue']

                goal_kicks_home = statistics['statistics'][0]['groups'][3]['statisticsItems'][7]['homeValue']
                goal_kicks_away = statistics['statistics'][0]['groups'][3]['statisticsItems'][7]['awayValue']
            
            elif len(statistics['statistics'][0]['groups'][3]['statisticsItems']) == 7:

                corner_kicks_home = statistics['statistics'][0]['groups'][3]['statisticsItems'][0]['homeValue']
                corner_kicks_away = statistics['statistics'][0]['groups'][3]['statisticsItems'][0]['awayValue']

                offsides_home = statistics['statistics'][0]['groups'][3]['statisticsItems'][1]['homeValue']
                offsides_away = statistics['statistics'][0]['groups'][3]['statisticsItems'][1]['awayValue']

                fouls_home = statistics['statistics'][0]['groups'][3]['statisticsItems'][2]['homeValue']
                fouls_away = statistics['statistics'][0]['groups'][3]['statisticsItems'][2]['awayValue']

                yellow_cards_home = statistics['statistics'][0]['groups'][3]['statisticsItems'][3]['homeValue']
                yellow_cards_away = statistics['statistics'][0]['groups'][3]['statisticsItems'][3]['awayValue']

                red_cards_home = 0
                red_cards_away = 0

                free_kicks_home = statistics['statistics'][0]['groups'][3]['statisticsItems'][4]['homeValue']
                free_kicks_away = statistics['statistics'][0]['groups'][3]['statisticsItems'][4]['awayValue']

                throw_ins_home = statistics['statistics'][0]['groups'][3]['statisticsItems'][5]['homeValue']
                throw_ins_away = statistics['statistics'][0]['groups'][3]['statisticsItems'][5]['awayValue']

                goal_kicks_home = statistics['statistics'][0]['groups'][3]['statisticsItems'][6]['homeValue']
                goal_kicks_away = statistics['statistics'][0]['groups'][3]['statisticsItems'][6]['awayValue']

            shots_inside_box_home = statistics['statistics'][0]['groups'][4]['statisticsItems'][0]['homeValue']
            shots_inside_box_away = statistics['statistics'][0]['groups'][4]['statisticsItems'][0]['awayValue']

            shots_outside_box_home = statistics['statistics'][0]['groups'][4]['statisticsItems'][1]['homeValue']
            shots_outside_box_away = statistics['statistics'][0]['groups'][4]['statisticsItems'][1]['awayValue']

            goalkeeper_saves_home = statistics['statistics'][0]['groups'][4]['statisticsItems'][2]['homeValue']
            goalkeeper_saves_away = statistics['statistics'][0]['groups'][4]['statisticsItems'][2]['awayValue']

            passes_home = statistics['statistics'][0]['groups'][5]['statisticsItems'][0]['homeValue']
            passes_away = statistics['statistics'][0]['groups'][5]['statisticsItems'][0]['awayValue']

            accurate_passes_home = statistics['statistics'][0]['groups'][5]['statisticsItems'][1]['homeValue']
            accurate_passes_away = statistics['statistics'][0]['groups'][5]['statisticsItems'][1]['awayValue']

            long_balls_home = statistics['statistics'][0]['groups'][5]['statisticsItems'][2]['homeTotal']
            long_balls_away = statistics['statistics'][0]['groups'][5]['statisticsItems'][2]['awayTotal']

            crosses_home = statistics['statistics'][0]['groups'][5]['statisticsItems'][3]['homeTotal']
            crosses_away = statistics['statistics'][0]['groups'][5]['statisticsItems'][3]['awayTotal']

            dribbles_home = statistics['statistics'][0]['groups'][6]['statisticsItems'][0]['homeTotal']
            dribbles_away = statistics['statistics'][0]['groups'][6]['statisticsItems'][0]['awayTotal']

            possesion_lost_home = statistics['statistics'][0]['groups'][6]['statisticsItems'][1]['homeValue']
            possesion_lost_away = statistics['statistics'][0]['groups'][6]['statisticsItems'][1]['awayValue']

            duels_won_home = statistics['statistics'][0]['groups'][6]['statisticsItems'][2]['homeValue']
            duels_won_away = statistics['statistics'][0]['groups'][6]['statisticsItems'][2]['awayValue']

            aerials_won_home = statistics['statistics'][0]['groups'][6]['statisticsItems'][3]['homeValue']
            aerials_won_away = statistics['statistics'][0]['groups'][6]['statisticsItems'][3]['awayValue']

            tackles_home = statistics['statistics'][0]['groups'][7]['statisticsItems'][0]['homeValue']
            tackles_away = statistics['statistics'][0]['groups'][7]['statisticsItems'][0]['awayValue']

            interceptions_home = statistics['statistics'][0]['groups'][7]['statisticsItems'][1]['homeValue']
            interceptions_away = statistics['statistics'][0]['groups'][7]['statisticsItems'][1]['awayValue']

            clearences_home = statistics['statistics'][0]['groups'][7]['statisticsItems'][2]['homeValue']
            clearences_away = statistics['statistics'][0]['groups'][7]['statisticsItems'][2]['awayValue']

        this_match = [
            home_team,
            away_team,
            home_score,
            away_score,
            expected_goals_home,
            expected_goals_away,
            posession_home,
            posession_away,
            total_shots_home,
            total_shots_away,
            shots_on_target_home,
            shots_on_target_away,
            shots_off_target_home,
            shots_off_target_away,
            blocked_shots_home,
            blocked_shots_away,
            corner_kicks_home,
            corner_kicks_away,
            offsides_home,
            offsides_away,
            fouls_home,
            fouls_away,
            yellow_cards_home,
            yellow_cards_away,
            red_cards_home,
            red_cards_away,
            free_kicks_home,
            free_kicks_away,
            throw_ins_home,
            throw_ins_away,
            goal_kicks_home,
            goal_kicks_away,
            shots_inside_box_home,
            shots_inside_box_away,
            shots_outside_box_home,
            shots_outside_box_away,
            goalkeeper_saves_home,
            goalkeeper_saves_away,
            passes_home, passes_away,
            accurate_passes_home,
            accurate_passes_away,
            long_balls_home,
            long_balls_away,
            crosses_home,
            crosses_away,
            dribbles_home,
            dribbles_away,
            possesion_lost_home,
            possesion_lost_away,
            duels_won_home,
            duels_won_away,
            aerials_won_home,
            aerials_won_away,
            tackles_home,
            tackles_away,
            interceptions_home,
            interceptions_away,
            clearences_home,
            clearences_away
        ]
        estadisticas.append(this_match)
        writer.writerow(this_match)
