import pandas as pd
import argparse
import os
from tqdm import tqdm
import ipdb

available_leagues = [
    'primera-division', 'premier-league', 'brasileirao-serie-a', 'bundesliga', 'ligue-1', 'laliga', 'serie-a'
]


def calculate_rates(df, team, is_home):
    team_col = 'Home Team' if is_home else 'Away Team'
    team_df = df[df[team_col] == team]

    total_matches = len(team_df)
    if total_matches == 0:
        return 0, 0, 0

    if is_home:
        win_rate = (team_df['Result'] == 'H').mean()
        draw_rate = (team_df['Result'] == 'D').mean()
        loss_rate = (team_df['Result'] == 'A').mean()
    else:
        win_rate = (team_df['Result'] == 'A').mean()
        draw_rate = (team_df['Result'] == 'D').mean()
        loss_rate = (team_df['Result'] == 'H').mean()

    return win_rate, draw_rate, loss_rate


def calculate_features(df):
    df = df.sort_values(by=['Season', 'number_of_match'], ascending=[
                        False, False]).reset_index(drop=True)

    season_col = df.pop('Season')
    df.insert(0, 'Season', season_col)
    df['Result'] = df.apply(lambda row: 'H' if row['HG'] > row['AG'] else (
        'A' if row['HG'] < row['AG'] else 'D'), axis=1)

    feature_columns = [
        'HTW_rate', 'HTD_rate', 'HTL_rate', 'ATW_rate', 'ATD_rate', 'ATL_rate',
        'HTHW_rate', 'HTHD_rate', 'HTHL_rate', 'ATAW_rate', 'ATAD_rate', 'ATAL_rate',
        '1_Last_HTW', '2_Last_HTW', '3_Last_HTW', '1_Last_HTD', '2_Last_HTD', '3_Last_HTD',
        '1_Last_HTHW', '2_Last_HTHW', '1_Last_ATW', '2_Last_ATW', '3_Last_ATW',
        '1_Last_ATD', '2_Last_ATD', '3_Last_ATD', '1_Last_ATWA', '2_Last_ATWA',
        '7_HTW_rate', '12_HTW_rate', '7_HTD_rate', '12_HTD_rate', '7_ATW_rate', '12_ATW_rate',
        '7_ATD_rate', '12_ATD_rate', '5_HTHW_rate', '5_ATAW_rate'
    ]
    for column in feature_columns:
        df[column] = 0.0

    # Iterate through each row to calculate and update the features
    for index, row in tqdm(df.iterrows(), total=len(df), desc="Calculating features"):
        home_team = row['Home Team']
        away_team = row['Away Team']
        current_season = row['Season']

        # Historical rates
        home_team_df = df[((df['Home Team'] == home_team) | (df['Away Team'] == home_team)) & (df['Season'] == current_season)]
        away_team_df = df[((df['Home Team'] == away_team) | (df['Away Team'] == away_team)) & (df['Season'] == current_season)]

        df.loc[index, 'HTW_rate'], df.loc[index, 'HTD_rate'], df.loc[index, 'HTL_rate'] = calculate_rates(home_team_df, home_team, is_home=True)
        df.loc[index, 'ATW_rate'], df.loc[index, 'ATD_rate'], df.loc[index, 'ATL_rate'] = calculate_rates(away_team_df, away_team, is_home=False)

        # Home and away "wins at home/away" rates

        home_team_home_df = df[(df['Home Team'] == home_team) & (df['Season'] == current_season)]
        away_team_away_df = df[(df['Away Team'] == away_team) & (df['Season'] == current_season)]

        df.loc[index, 'HTHW_rate'] = calculate_rates(home_team_home_df, home_team, is_home=True)[0]
        df.loc[index, 'HTHD_rate'] = calculate_rates(home_team_home_df, home_team, is_home=True)[1]
        df.loc[index, 'HTHL_rate'] = calculate_rates(home_team_home_df, home_team, is_home=True)[2]
        df.loc[index, 'ATAW_rate'] = calculate_rates(away_team_away_df, away_team, is_home=False)[0]
        df.loc[index, 'ATAD_rate'] = calculate_rates(away_team_away_df, away_team, is_home=False)[1]
        df.loc[index, 'ATAL_rate'] = calculate_rates(away_team_away_df, away_team, is_home=False)[2]

        # Last matches results
        home_team_matches = df[(df['Home Team'] == home_team) | (df['Away Team'] == home_team)]
        home_home_matches = df[(df['Home Team'] == home_team)]
        home_away_matches = df[(df['Away Team'] == home_team)]

        away_team_matches = df[(df['Home Team'] == away_team) | (df['Away Team'] == away_team)]
        away_home_matches = df[(df['Home Team'] == away_team)]
        away_away_matches = df[(df['Away Team'] == away_team)]

        offset = 1
        df.loc[index, '1_Last_HTW'] = int((home_team_matches.iloc[index:index+offset]['Result'] == 'H').sum() > offset-1)
        df.loc[index, '1_Last_HTD'] = int((home_team_matches.iloc[index:index+offset]['Result'] == 'D').sum() > offset-1)
        df.loc[index, '1_Last_HTHW'] = int((home_home_matches.iloc[index:index+offset]['Result'] == 'H').sum() > offset-1)
        df.loc[index, '1_Last_ATW'] = int((away_team_matches.iloc[index:index+offset]['Result'] == 'A').sum() > offset-1)
        df.loc[index, '1_Last_ATD'] = int((away_team_matches.iloc[index:index+offset]['Result'] == 'D').sum() > offset-1)
        df.loc[index, '1_Last_ATWA'] = int((away_away_matches.iloc[index:index+offset]['Result'] == 'A').sum() > offset-1)

        offset = 2
        df.loc[index, '2_Last_HTW'] = int((home_team_matches.iloc[index:index+offset]['Result'] == 'H').sum() > offset-1)
        df.loc[index, '2_Last_HTD'] = int((home_team_matches.iloc[index:index+offset]['Result'] == 'D').sum() > offset-1)
        df.loc[index, '2_Last_HTHW'] = int((home_home_matches.iloc[index:index+offset]['Result'] == 'H').sum() > offset-1)
        df.loc[index, '2_Last_ATW'] = int((away_team_matches.iloc[index:index+offset]['Result'] == 'A').sum() > offset-1)
        df.loc[index, '2_Last_ATD'] = int((away_team_matches.iloc[index:index+offset]['Result'] == 'D').sum() > offset-1)
        df.loc[index, '2_Last_ATWA'] = int((away_away_matches.iloc[index:index+offset]['Result'] == 'A').sum() > offset-1)

        offset = 3
        df.loc[index, '3_Last_HTW'] = int((home_team_matches.iloc[index:index+offset]['Result'] == 'H').sum() > offset-1)
        df.loc[index, '3_Last_HTD'] = int((home_team_matches.iloc[index:index+offset]['Result'] == 'D').sum() > offset-1)
        df.loc[index, '3_Last_ATW'] = int((away_team_matches.iloc[index:index+offset]['Result'] == 'A').sum() > offset-1)
        df.loc[index, '3_Last_ATD'] = int((away_team_matches.iloc[index:index+offset]['Result'] == 'D').sum() > offset-1)

        offset = 7
        df.loc[index, '7_HTW_rate'] = (home_team_matches.iloc[index:index+offset]['Result'] == 'H').mean()
        df.loc[index, '7_HTD_rate'] = (home_team_matches.iloc[index:index+offset]['Result'] == 'D').mean()
        df.loc[index, '7_ATW_rate'] = (away_team_matches.iloc[index:index+offset]['Result'] == 'A').mean()
        df.loc[index, '7_ATD_rate'] = (away_team_matches.iloc[index:index+offset]['Result'] == 'D').mean()

        offset = 12
        df.loc[index, '12_HTW_rate'] = (home_team_matches.iloc[index:index+offset]['Result'] == 'H').mean()
        df.loc[index, '12_HTD_rate'] = (home_team_matches.iloc[index:index+offset]['Result'] == 'D').mean()
        df.loc[index, '12_ATW_rate'] = (away_team_matches.iloc[index:index+offset]['Result'] == 'A').mean()
        df.loc[index, '12_ATD_rate'] = (away_team_matches.iloc[index:index+offset]['Result'] == 'D').mean()

        offset = 5
        df.loc[index, '5_HTHW_rate'] = (home_home_matches.iloc[index:index+offset]['Result'] == 'H').mean()
        df.loc[index, '5_ATAW_rate'] = (away_away_matches.iloc[index:index+offset]['Result'] == 'A').mean()

    df = df[['Season', 'number_of_match', 'Home Team', 'Away Team', 'Result', 'HTW_rate', 'HTD_rate', 'HTL_rate', 'ATW_rate', 'ATD_rate', 'ATL_rate', 'HTHW_rate', 'HTHD_rate', 'HTHL_rate', 'ATAW_rate', 'ATAD_rate', 'ATAL_rate', '1_Last_HTW', '2_Last_HTW', '3_Last_HTW', '1_Last_HTD', '2_Last_HTD', '3_Last_HTD', '1_Last_HTHW', '2_Last_HTHW', '1_Last_ATW', '2_Last_ATW', '3_Last_ATW', '1_Last_ATD', '2_Last_ATD', '3_Last_ATD', '1_Last_ATWA', '2_Last_ATWA', '7_HTW_rate', '12_HTW_rate', '7_HTD_rate', '12_HTD_rate', '7_ATW_rate', '12_ATW_rate', '7_ATD_rate', '12_ATD_rate', '5_HTHW_rate', '5_ATAW_rate']]
    return df


def parse_df(league_name):
    folder_path = f"statistics/{league_name}"
    combined_df = pd.DataFrame()
    csv_files = [file for file in os.listdir(
        folder_path) if file.endswith('.csv')]

    for file in csv_files:
        df = pd.read_csv(os.path.join(folder_path, file))
        year = file.split('.')[0].split('_')[-1] # stats_2023.csv
        df['Season'] = year

        df.rename(columns={
            'team_home': 'Home Team',
            'team_away': 'Away Team',
            'home_score': 'HG',
            'away_score': 'AG'
        }, inplace=True)
        df.dropna(subset=['Home Team', 'Away Team'], inplace=True)

        combined_df = pd.concat([combined_df, df], ignore_index=True)

    final_df = calculate_features(combined_df)
    final_df.to_csv(f"features/features-{league_name}.csv", index=False)


def parse_arguments():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('--league', type=str, required=True,
                        help='Select a league', choices=available_leagues)
    return parser.parse_args()


def main():
    args = parse_arguments()
    parse_df(args.league)


if __name__ == '__main__':
    main()
