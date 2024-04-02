def file_exists(league, season, folder, file_pre='stats'):
    try:
        with open(f"{folder}/{league['slug']}/{file_pre}_{season['year']}.csv", 'r') as file:
            data = file.read()
            if data:
                print(
                    f"File {folder}/{league['slug']}/{file_pre}_{season['year']} already exists")
                return True
    except:
        return False


def get_season_ids(league, season):
    ids = []

    with open(f"ids/{league['slug']}/{season['year']}.txt", 'r') as file:
        for row in file:
            ids.append(row.strip())
    return ids
