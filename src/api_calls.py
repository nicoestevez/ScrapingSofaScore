import requests
import json
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import time
import os
from helpers import file_exists, get_season_ids

lock = threading.Lock()

FOLDER = 'statistics'
url_all = 'https://api.sofascore.com/api/v1/event/{id_partido}/odds/1/all'
url_statistics = 'https://api.sofascore.com/api/v1/event/{id_partido}/statistics'
url_incidents = 'https://api.sofascore.com/api/v1/event/{id_partido}/incidents'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}


def get_statistic_by_name(statistics_items, statistic_name, home_key='homeValue', away_key='awayValue', default_value=None):
    for item in statistics_items:
        if item.get('name') == statistic_name:
            return item.get(home_key, default_value), item.get(away_key, default_value)
    return default_value, default_value


def get_index_of_statistic(statistics_items, statistic_name):
    for index, item in enumerate(statistics_items):
        if item.get('groupName') == statistic_name:
            return index
    return None


headers_csv = ["number_of_match", "team_home", "team_away", "home_score", "away_score",
               "posession_home", "posession_away", "total_shots_home", "total_shots_away", "shots_on_target_home",
               "shots_on_target_away", "shots_off_target_home", "shots_off_target_away", "blocked_shots_home",
               "blocked_shots_away", "corner_kicks_home", "corner_kicks_away", "offsides_home", "offsides_away",
               "fouls_home", "fouls_away", "yellow_cards_home", "yellow_cards_away", "red_cards_home",
               "red_cards_away", "free_kicks_home", "free_kicks_away", "throw_ins_home", "throw_ins_away",
               "goal_kicks_home", "goal_kicks_away", "big_chances_home", "big_chances_away", "big_chances_missed_home",
               "big_chances_missed_away", "hit_woodwork_home", "hit_woodwork_away", "counter_attacks_home",
               "counter_attacks_away", "counter_attacks_shots_home", "counter_attacks_shots_away",
               "shots_inside_box_home", "shots_inside_box_away", "shots_outside_box_home", "shots_outside_box_away",
               "goalkeeper_saves_home", "goalkeeper_saves_away", "passes_home", "passes_away", "accurate_passes_home",
               "accurate_passes_away", "long_balls_home", "long_balls_away", "crosses_home", "crosses_away",
               "dribbles_home", "dribbles_away", "possesion_lost_home", "possesion_lost_away", "duels_won_home",
               "duels_won_away", "aerials_won_home", "aerials_won_away", "tackles_home", "tackles_away",
               "interceptions_home", "interceptions_away", "clearences_home", "clearences_away"]

estadisticas = []


def get_round_for_match(match_index, starting_round=30, matches_per_round=8):
    """
    Returns the round number for a given match index.

    :param match_index: Index of the match (0-based index)
    :param starting_round: The starting round number (default is 30)
    :param matches_per_round: Number of matches per round (default is 8)
    :return: The round number
    """
    # Calculate the round number
    round_number = starting_round - (match_index // matches_per_round)
    return round_number


def write_to_csv(data, writer):
    with lock:  # Ensure only one thread writes to the file at a time
        writer.writerow(data)


def find_data(id, numero_partido):
    try:
        response_all = requests.get(url_all.format(id_partido=id),
                                    headers=headers)
        if response_all.status_code == 200:
            all = json.loads(response_all.text)
            length = len(all['markets'])
            home_team = all['markets'][length - 1]['choices'][0]['name']
            away_team = all['markets'][length - 1]['choices'][2]['name']
        else:
            home_team = 1
            away_team = 2
    except IndexError:
        home_team = 1
        away_team = 2

    # Obtener Goles de los equipos
    response_incidents = requests.get(url_incidents.format(id_partido=id),
                                      headers=headers)
    if response_incidents.status_code == 200:
        incidents = json.loads(response_incidents.text)
        home_score = incidents['incidents'][0]['homeScore']
        away_score = incidents['incidents'][0]['awayScore']
    else:
        home_score = 999
        away_score = 999

    # Obtener Estadísticas de los equipos
    response_statistics = requests.get(url_statistics.format(id_partido=id),
                                       headers=headers)
    if response_statistics.status_code == 200:
        statistics = json.loads(response_statistics.text)

        # Posession
        index_possession = get_index_of_statistic(
            statistics['statistics'][0]['groups'], 'Possession')
        if index_possession != None:
            if statistics['statistics'][0]['groups'][index_possession]['groupName'] == "Possession":
                possesion = statistics['statistics'][0]['groups'][index_possession]['statisticsItems']

                posession_home, posession_away = get_statistic_by_name(
                    possesion, 'Ball possession')
        else:
            posession_home = None
            posession_away = None

        # Shots
        index_shots = get_index_of_statistic(
            statistics['statistics'][0]['groups'], 'Shots')
        if index_shots != None:
            if statistics['statistics'][0]['groups'][index_shots]['groupName'] == "Shots":
                shots = statistics['statistics'][0]['groups'][index_shots]['statisticsItems']

                total_shots_home, total_shots_away = get_statistic_by_name(
                    shots, 'Total shots')
                shots_on_target_home, shots_on_target_away = get_statistic_by_name(
                    shots, 'Shots on target')
                shots_off_target_home, shots_off_target_away = get_statistic_by_name(
                    shots, 'Shots off target')
                blocked_shots_home, blocked_shots_away = get_statistic_by_name(
                    shots, 'Blocked shots')
        else:
            total_shots_home = None
            total_shots_away = None
            shots_on_target_home = None
            shots_on_target_away = None
            shots_off_target_home = None
            shots_off_target_away = None
            blocked_shots_home = None
            blocked_shots_away = None

        # TVData
        index_tvdata = get_index_of_statistic(
            statistics['statistics'][0]['groups'], 'TVData')
        if index_tvdata != None:
            if statistics['statistics'][0]['groups'][index_tvdata]['groupName'] == "TVData":
                tvdata = statistics['statistics'][0]['groups'][index_tvdata]['statisticsItems']

                corner_kicks_home, corner_kicks_away = get_statistic_by_name(
                    tvdata, 'Corner kicks')
                offsides_home, offsides_away = get_statistic_by_name(
                    tvdata, 'Offsides')
                fouls_home, fouls_away = get_statistic_by_name(
                    tvdata, 'Fouls')
                yellow_cards_home, yellow_cards_away = get_statistic_by_name(
                    tvdata, 'Yellow cards')
                red_cards_home, red_cards_away = get_statistic_by_name(
                    tvdata, 'Red cards', default_value=0)
                free_kicks_home, free_kicks_away = get_statistic_by_name(
                    tvdata, 'Free kicks')
                throw_ins_home, throw_ins_away = get_statistic_by_name(
                    tvdata, 'Throw ins')
                goal_kicks_home, goal_kicks_away = get_statistic_by_name(
                    tvdata, 'Goal kicks')
        else:
            corner_kicks_home = None
            corner_kicks_away = None
            offsides_home = None
            offsides_away = None
            fouls_home = None
            fouls_away = None
            yellow_cards_home = None
            yellow_cards_away = None
            red_cards_home = None
            red_cards_away = None
            free_kicks_home = None
            free_kicks_away = None
            throw_ins_home = None
            throw_ins_away = None
            goal_kicks_home = None
            goal_kicks_away = None

        # Shots extra
        index_shots_extra = get_index_of_statistic(
            statistics['statistics'][0]['groups'], 'Shots extra')
        if index_shots_extra != None:
            if statistics['statistics'][0]['groups'][index_shots_extra]['groupName'] == "Shots extra":
                shots_extra = statistics['statistics'][0]['groups'][index_shots_extra]['statisticsItems']

                big_chances_home, big_chances_away = get_statistic_by_name(
                    shots_extra, 'Big chances')
                big_chances_missed_home, big_chances_missed_away = get_statistic_by_name(
                    shots_extra, 'Big chances missed')
                hit_woodwork_home, hit_woodwork_away = get_statistic_by_name(
                    shots_extra, 'Hit woodwork')
                counter_attacks_home, counter_attacks_away = get_statistic_by_name(
                    shots_extra, 'Counter attacks')
                counter_attacks_shots_home, counter_attacks_shots_away = get_statistic_by_name(
                    shots_extra, 'Counter attacks shots')
                shots_inside_box_home, shots_inside_box_away = get_statistic_by_name(
                    shots_extra, 'Shots inside box')
                shots_outside_box_home, shots_outside_box_away = get_statistic_by_name(
                    shots_extra, 'Shots outside box')
                goalkeeper_saves_home, goalkeeper_saves_away = get_statistic_by_name(
                    shots_extra, 'Goalkeeper saves')
        else:
            big_chances_home = None
            big_chances_away = None
            big_chances_missed_home = None
            big_chances_missed_away = None
            hit_woodwork_home = None
            hit_woodwork_away = None
            counter_attacks_home = None
            counter_attacks_away = None
            counter_attacks_shots_home = None
            counter_attacks_shots_away = None
            shots_inside_box_home = None
            shots_inside_box_away = None
            shots_outside_box_home = None
            shots_outside_box_away = None
            goalkeeper_saves_home = None
            goalkeeper_saves_away = None

        index_passes = get_index_of_statistic(
            statistics['statistics'][0]['groups'], 'Passes')
        if index_passes != None:
            if statistics['statistics'][0]['groups'][index_passes]['groupName'] == "Passes":
                passes = statistics['statistics'][0]['groups'][index_passes]['statisticsItems']

                passes_home, passes_away = get_statistic_by_name(
                    passes, 'Passes')
                accurate_passes_home, accurate_passes_away = get_statistic_by_name(
                    passes, 'Accurate passes')
                long_balls_home, long_balls_away = get_statistic_by_name(
                    passes, 'Long balls')
                crosses_home, crosses_away = get_statistic_by_name(
                    passes, 'Crosses')
        else:
            passes_home = None
            passes_away = None
            accurate_passes_home = None
            accurate_passes_away = None
            long_balls_home = None
            long_balls_away = None
            crosses_home = None
            crosses_away = None

        # Duels
        index_duels = get_index_of_statistic(
            statistics['statistics'][0]['groups'], 'Duels')
        if index_duels != None:
            if statistics['statistics'][0]['groups'][index_duels]['groupName'] == "Duels":
                duels = statistics['statistics'][0]['groups'][index_duels]['statisticsItems']

                dribbles_home, dribbles_away = get_statistic_by_name(
                    duels, 'Dribbles')
                possesion_lost_home, possesion_lost_away = get_statistic_by_name(
                    duels, 'Possesion lost')
                duels_won_home, duels_won_away = get_statistic_by_name(
                    duels, 'Duels won')
                aerials_won_home, aerials_won_away = get_statistic_by_name(
                    duels, 'Aerials won')
        else:
            dribbles_home = None
            dribbles_away = None
            possesion_lost_home = None
            possesion_lost_away = None
            duels_won_home = None
            duels_won_away = None
            aerials_won_home = None
            aerials_won_away = None

        # Defending
        index_defending = get_index_of_statistic(
            statistics['statistics'][0]['groups'], 'Defending')
        if index_defending != None:
            if statistics['statistics'][0]['groups'][index_defending]['groupName'] == "Defending":
                defending = statistics['statistics'][0]['groups'][index_defending]['statisticsItems']

                tackles_home, tackles_away = get_statistic_by_name(
                    defending, 'Tackles')
                interceptions_home, interceptions_away = get_statistic_by_name(
                    defending, 'Interceptions')
                clearences_home, clearences_away = get_statistic_by_name(
                    defending, 'Clearences')
        else:
            tackles_home = None
            tackles_away = None
            interceptions_home = None
            interceptions_away = None
            clearences_home = None
            clearences_away = None

    else:
        total_elements = 69
        this_match = [numero_partido if i ==
                      0 else None for i in range(total_elements)]
        return this_match

    this_match = [
        numero_partido,
        home_team,
        away_team,
        home_score,
        away_score,
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
        big_chances_home,
        big_chances_away,
        big_chances_missed_home,
        big_chances_missed_away,
        hit_woodwork_home,
        hit_woodwork_away,
        counter_attacks_home,
        counter_attacks_away,
        counter_attacks_shots_home,
        counter_attacks_shots_away,
        shots_inside_box_home,
        shots_inside_box_away,
        shots_outside_box_home,
        shots_outside_box_away,
        goalkeeper_saves_home,
        goalkeeper_saves_away,
        passes_home,
        passes_away,
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
    return this_match


def main():
    with open('examples_json/league.json', 'r') as file:
        leagues_data = json.load(file).get('leagues')
        for league in leagues_data:
            seasons = league['seasons']
            for season in seasons:
                try:
                    season['year'] = season['year'].replace('/', '-')
                    get_season_stats(league, season)
                except FileNotFoundError as e:
                    continue


# Prepare CSV file for writing
def get_season_stats(league, season):
    if file_exists(league, season, FOLDER):
        return

    if str(season['year']) in str(time.localtime().tm_year):
        return
    print("Getting stats for:", season['name'], "in", league['name'])
    ids = get_season_ids(league, season)
    directory = f"{FOLDER}/{league['slug']}"
    os.makedirs(directory, exist_ok=True)
    with open(f'{FOLDER}/{league["slug"]}/stats_{season["year"]}.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers_csv)

        # Use ThreadPoolExecutor to manage multiple threads
        with ThreadPoolExecutor(max_workers=64) as executor:
            # Submit all tasks
            future_to_id = {executor.submit(
                find_data, id, numero): id for numero, id in enumerate(ids)}

            try:
                # Process futures as they complete
                for future in as_completed(future_to_id):
                    data = future.result()  # This will raise an exception if the task raised one
                    write_to_csv(data, writer)
            except Exception as exc:
                print(f"An exception occurred: {exc}")
                # Here, you can decide whether to cancel remaining tasks or not
                for future in future_to_id:
                    future.cancel()


if __name__ == "__main__":
    main()
