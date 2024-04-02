import requests
import json
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from helpers import file_exists, get_season_ids
import threading
import time
import os
import pandas as pd

lock = threading.Lock()


url_lineups = 'https://api.sofascore.com/api/v1/event/{game_id}/lineups'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

FOLDER = 'lineups'
WANTED_STATS = [
    "accuratePass",
    "totalLongBalls",
    "accurateLongBalls",
    "totalClearance",
    "savedShotsFromInsideTheBox",
    "saves",
    "punches",
    "minutesPlayed"
]


def create_team_row(team_data, team_name, game_id: str):
    players = team_data['players']
    player_data = {
        'EventId': game_id,
        'Team': team_name,
        'Formation': team_data.get('formation', 'N/A'),
    }
    player_count = 0
    player_ratings = []

    for i, player in enumerate(players, start=1):
        player_info = player['player']
        player_stats = player['statistics']
        if not bool(player_stats):
            continue
        player_count += 1

        # Basic player information
        player_data[f'Player{i}_Name'] = player_info.get('name', 'N/A')
        player_data[f'Player{i}_code'] = player_info.get('slug', 'N/A')
        player_data[f'Player{i}_Position'] = player_info.get('position', 'N/A')
        player_data[f'Player{i}_substitute'] = player.get('substitute', False)

        rating_versions = player_stats.get('ratingVersions', {})
        original_rating = rating_versions.get('original', 0)
        alternative_rating = rating_versions.get('alternative', 0)
        player_rating = (original_rating + alternative_rating) / \
            2 if alternative_rating else original_rating
        player_data[f'Player{i}_Rating'] = player_rating
        player_ratings.append(player_rating)
        for stat in WANTED_STATS:
            player_data[f'Player{i}_{stat}'] = player_stats.get(stat, 0)

    player_data['PlayerCount'] = player_count
    average_rating = sum(player_ratings) / \
        len(player_ratings) if player_ratings else 0
    player_data['AverageTeamRating'] = average_rating

    return player_data


def json_to_df(data: dict, game_id: str):
    home_row = create_team_row(data['home'], 'Home', game_id)
    away_row = create_team_row(data['away'], 'Away', game_id)
    df = pd.DataFrame([home_row, away_row])
    return df


def find_data(game_id):
    try:
        response_all = requests.get(url_lineups.format(game_id=game_id),
                                    headers=headers)
        if response_all.status_code == 200:
            game_data = json.loads(response_all.text)
            return json_to_df(game_data, game_id)
    except Exception as e:
        # print(f"Error getting data for {game_id}: {e}")
        return


def concat_or_create(df, data):
    if data is None:
        return df
    if df.empty:
        return data
    return pd.concat([df, data], ignore_index=True)


def get_season_stats(league, season):
    if file_exists(league, season, FOLDER, 'lineups'):
        return

    if str(season['year']) in str(time.localtime().tm_year):
        return
    print("Getting stats for:", season['name'], "in", league['name'])
    ids = get_season_ids(league, season)
    directory = f"{FOLDER}/{league['slug']}"
    os.makedirs(directory, exist_ok=True)
    df = pd.DataFrame()

    # Use ThreadPoolExecutor to manage multiple threads
    with ThreadPoolExecutor(max_workers=32) as executor:
        future_to_id = {executor.submit(
            find_data, id): id for id in ids}

        try:
            # Process futures as they complete
            for future in as_completed(future_to_id):
                data = future.result()  # This will raise an exception if the task raised one
                df = concat_or_create(df, data)
        except Exception as exc:
            print(f"An exception occurred: {exc}")
            # Here, you can decide whether to cancel remaining tasks or not
            for future in future_to_id:
                future.cancel()
    df.to_csv(
        f'{FOLDER}/{league["slug"]}/{FOLDER}_{season["year"]}.csv', index=False)


def main():
    with open('examples_json/league.json', 'r') as file:
        leagues_data = json.load(file).get('leagues')
        for league in leagues_data:
            seasons = league['seasons']
            for season in seasons:
                try:
                    season['year'] = season['year'].replace('/', '-')
                    get_season_stats(league, season)
                except FileNotFoundError:
                    continue


if __name__ == "__main__":
    main()
