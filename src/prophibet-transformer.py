import pandas as pd
import argparse
import os
import time
from datetime import datetime
from tqdm import tqdm

available_leagues = ['primera-division']

N = 5

def calculate_last_n_stats(df, team_col, opp_col, score_col, is_home, N):
    if df.empty:
        return 0, 0, 0, 0, 0, 0

    results = df.groupby(team_col).tail(N)
    results[score_col] = pd.to_numeric(results[score_col], errors='coerce')
    results[opp_col] = pd.to_numeric(results[opp_col], errors='coerce')

    if is_home:
        wins = (results[score_col] > results[opp_col]).sum()
        losses = (results[score_col] < results[opp_col]).sum()
        goal_forward = results[score_col].sum()
        goal_against = results[opp_col].sum()
        g_goal_diff_wins = ((results[score_col] - results[opp_col]) >= 2).sum()
        g_goal_diff_losses = (
            (results[opp_col] - results[score_col]) >= 2).sum()
    else:
        wins = (results[score_col] > results[opp_col]).sum()
        losses = (results[score_col] < results[opp_col]).sum()
        goal_forward = results[score_col].sum()
        goal_against = results[opp_col].sum()
        g_goal_diff_wins = ((results[score_col] - results[opp_col]) >= 2).sum()
        g_goal_diff_losses = (
            (results[opp_col] - results[score_col]) >= 2).sum()

    return wins, losses, goal_forward, goal_against, g_goal_diff_wins, g_goal_diff_losses

def calculate_rate(df, team_col, score_col, opp_col, is_home):
    total_matches = df.groupby(team_col).size()
    if is_home:
        wins = df.groupby(team_col).apply(lambda x: (pd.to_numeric(
            x[score_col], errors='coerce') > pd.to_numeric(x[opp_col], errors='coerce')).sum())
        losses = df.groupby(team_col).apply(lambda x: (pd.to_numeric(
            x[score_col], errors='coerce') < pd.to_numeric(x[opp_col], errors='coerce')).sum())
    else:
        wins = df.groupby(team_col).apply(lambda x: (pd.to_numeric(
            x[score_col], errors='coerce') > pd.to_numeric(x[opp_col], errors='coerce')).sum())
        losses = df.groupby(team_col).apply(lambda x: (pd.to_numeric(
            x[score_col], errors='coerce') < pd.to_numeric(x[opp_col], errors='coerce')).sum())

    win_rate = (wins / total_matches) * 100
    loss_rate = (losses / total_matches) * 100

    return win_rate, loss_rate

def parse_df(league_name):
    folder_path = f"statistics/{league_name}"
    combined_df = pd.DataFrame()
    csv_files = [file for file in os.listdir(
        folder_path) if file.endswith('.csv')]

    for file in tqdm(csv_files, desc="Processing files"):
        df = pd.read_csv(os.path.join(folder_path, file))
        year = file.split('.')[0].split('_')[-1] # stats_2023.csv

        df['Season'] = year

        df.rename(columns={
            'home_odd': '1',
            'draw_odd': 'X',
            'away_odd': '2',
            'team_home': 'Home Team',
            'team_away': 'Away Team',
            'home_score': 'HG',
            'away_score': 'AG'
        }, inplace=True)
        df.dropna(subset=['Home Team', 'Away Team'], inplace=True)

        if df.empty:
            continue
        today_date = datetime.today().strftime('%Y-%m-%d')
        df['Date'] = today_date

        # Calculate additional columns
        df['Result'] = df.apply(lambda row: 'H' if row['HG'] > row['AG'] else (
            'A' if row['HG'] < row['AG'] else 'D'), axis=1)

        # Calculate statistics for home teams
        home_stats = df.apply(lambda row: calculate_last_n_stats(
            df[df['Home Team'] == row['Home Team']] if not df[df['Home Team'] == row['Home Team']].empty else pd.DataFrame(columns=['HG', 'AG']), 'Home Team', 'Away Team', 'HG', True, N), axis=1)
        home_stats = list(zip(*home_stats)) if not home_stats.empty else ([], [], [], [], [], [])
        df['HW'], df['HL'], df['HGF'], df['HGA'], df['HWGD'], df['HLGD'] = home_stats

        # Calculate statistics for away teams
        away_stats = df.apply(lambda row: calculate_last_n_stats(
            df[df['Away Team'] == row['Away Team']] if not df[df['Away Team'] == row['Away Team']].empty else pd.DataFrame(columns=['HG', 'AG']), 'Away Team', 'Home Team', 'AG', False, N), axis=1)
        away_stats = list(zip(*away_stats)) if not away_stats.empty else ([], [], [], [], [], [])
        df['AW'], df['AL'], df['AGF'], df['AGA'], df['AWGD'], df['ALGD'] = away_stats

        # Calculate win/loss rate for home teams
        home_win_rate, home_loss_rate = calculate_rate(
            df, 'Home Team', 'HG', 'AG', True)
        home_win_rate = home_win_rate[df['Home Team']].values
        home_loss_rate = home_loss_rate[df['Home Team']].values
        df['HW%'] = home_win_rate
        df['HL%'] = home_loss_rate

        # Calculate win/loss rate for away teams
        away_win_rate, away_loss_rate = calculate_rate(
            df, 'Away Team', 'AG', 'HG', False)
        away_win_rate = away_win_rate[df['Away Team']].values
        away_loss_rate = away_loss_rate[df['Away Team']].values
        df['AW%'] = away_win_rate
        df['AL%'] = away_loss_rate

        if not df.empty:
            combined_df = pd.concat([combined_df, df], ignore_index=True)

    combined_df = combined_df[['Date', 'Season', 'Home Team', 'Away Team', '1', 'X', '2','HG', 'AG', 'Result', 'HW', 'HL',
                               'HGF', 'HGA', 'HWGD', 'HLGD', 'HW%', 'HL%', 'AW', 'AL', 'AGF', 'AGA', 'AWGD', 'ALGD', 'AW%', 'AL%']]

    combined_df.to_csv(f"prophibet-{league_name}.csv", index=False)

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
