import requests
import json
import time
import os
import threading


class NoMoreRoundsException(Exception):
    pass


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
# Sujeto a cambios
SELECTOR_BTN = "button[role='combobox']"
ROUND_SELECTOR = "div[class='sc-fqkvVR sc-fUnMCh dDIma-D hkwHv ps--active-y'] div ul[role='listbox']"
BACK_BTN_SELECTOR = "button[class='sc-aXZVg bZLkMO']"
season_url = "https://api.sofascore.com/api/v1/unique-tournament/{league_id}/season/{season_id}/events/round/{round}"
MAX_ROUNDS = 40

BROWSER_PREFS = {'profile.default_content_setting_values': {'images': 2, 'popups': 2,
                                                            'plugins': 2, 'geolocation': 2,
                                                            'notifications': 2, 'fullscreen': 2,
                                                            'mouselock': 2, 'mixed_script': 2, 'media_stream': 2,
                                                            'media_stream_mic': 2, 'media_stream_camera': 2,
                                                            'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2,
                                                            'push_messaging': 2, 'metro_switch_to_desktop': 2,
                                                            'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement': 2,
                                                            }}


def get_links_for_season(league, season):
    season['year'] = season['year'].replace('/', '-')
    if str(season['year']) in str(time.localtime().tm_year):
        return
    if file_exists(league, season):
        return
    print("Getting links for:", season['name'])
    for i in range(1, MAX_ROUNDS + 1):
        try:
            find_links(league, season, i)
        except NoMoreRoundsException:
            break


def find_links(league, season, round):
    league_idx = league["id"]
    season_idx = season["id"]
    response_all = requests.get(season_url.format(league_id=league_idx, season_id=season_idx, round=round),
                                headers=headers)
    directory = f"ids/{league['slug']}"
    os.makedirs(directory, exist_ok=True)
    if response_all.status_code == 200:
        all = json.loads(response_all.text)
        events = all["events"]
        for event in events:
            id = event["id"]
            with open(f"ids/{league['slug']}/{season['year']}.txt", 'a') as file:
                file.write(str(id) + '\n')
    else:
        raise NoMoreRoundsException("Error")


def file_exists(league, season):
    try:
        with open(f"ids/{league['slug']}/{season['year']}.txt", 'r') as file:
            data = file.read()
            if data:
                print(
                    f"File ids/{league['slug']}/ids_{season['year']} already exists")
                return True
    except:
        return False


def get_links():
    with open('examples_json/league.json', 'r') as file:
        leagues_data = json.load(file).get('leagues')
        threads = []
        for league in leagues_data:
            seasons = league['seasons']
            for season in seasons:
                thread = threading.Thread(
                    target=get_links_for_season, args=(league, season))
                threads.append(thread)
                thread.start()

        for thread in threads:
            thread.join()
