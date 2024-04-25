const headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'
};

const competitionId = 34;
const seasonId = 23872;
const year = '2019-20';
const total_rounds = 34;
const folder = 'ligue_1';

const roundApi = (competitionId, seasonId, round) =>
    `https://api.sofascore.com/api/v1/unique-tournament/${competitionId}/season/${seasonId}/events/round/${round}`;
const statisticsApi = (matchId) =>
    `https://api.sofascore.com/api/v1/event/${matchId}/statistics`;
const incidentsApi = (matchId) =>
    `https://api.sofascore.com/api/v1/event/${matchId}/incidents`;

const statsKeys = [
    'round', 'team_home', 'team_away', 'score_home', 'score_away',
    'expected_goals_home', 'expected_goals_away', 'possession_home', 'possession_away',
    'total_shots_home', 'total_shots_away', 'shots_on_target_home', 'shots_on_target_away',
    'shots_off_target_home', 'shots_off_target_away', 'blocked_shots_home', 'blocked_shots_away',
    'corners_home', 'corners_away', 'offsides_home', 'offsides_away', 'fouls_home', 'fouls_away',
    'yellow_cards_home', 'yellow_cards_away', 'red_cards_home', 'red_cards_away', 'free_kicks_home',
    'free_kicks_away', 'throw_ins_home', 'throw_ins_away', 'goal_kicks_home', 'goal_kicks_away',
    'big_chances_home', 'big_chances_away', 'big_chances_missed_home', 'big_chances_missed_away',
    'counter_attacks_home', 'counter_attacks_away', 'counter_attacks_shots_home',
    'counter_attacks_shots_away', 'shots_inside_box_home', 'shots_inside_box_away',
    'shots_outside_box_home', 'shots_outside_box_away', 'goalkeeper_saves_home',
    'goalkeeper_saves_away', 'passes_home', 'passes_away', 'accurate_passes_home',
    'accurate_passes_away', 'long_balls_home', 'long_balls_away', 'crosses_home', 'crosses_away',
    'dribbles_home', 'dribbles_away', 'possession_lost_home', 'possession_lost_away',
    'duels_won_home', 'duels_won_away', 'aerials_won_home', 'aerials_won_away', 'tackles_home',
    'tackles_away', 'interceptions_home', 'interceptions_away', 'clearances_home', 'clearances_away'
];

const stats = {};

async function getRoundData(competitionId, seasonId, round) {
    const response = await fetch(roundApi(competitionId, seasonId, round), {
        headers
    });

    if (response.ok) {
        const data = await response.json();
        return data.events || [];
    } else {
        console.error(`Error fetching round data for round ${round}: ${response.status}`);
        throw new Error(`Failed to fetch round data, status code: ${response.status}`);
    }
}

async function getMatchId(event) {
    return event.id;
}

async function getMatchScore(event, matchId) {
    const response = await fetch(incidentsApi(matchId), { headers });

    if (response.ok) {
        const data = await response.json();
        const incident = data.incidents[0];
        stats['team_home'] = event.homeTeam.name;
        stats['score_home'] = incident.homeScore;
        stats['team_away'] = event.awayTeam.name;
        stats['score_away'] = incident.awayScore;
    } else {
        throw new Error(`Error fetching match score, status code: ${response.status}`);
    }
}

async function getMatchStatistics(matchId) {
    const response = await fetch(statisticsApi(matchId), { headers });

    if (response.ok) {
        const data = await response.json();
        const allPeriod = data.statistics.find((item) => item.period === 'ALL');
        if (!allPeriod) {
            console.warn('No period "ALL" found');
            return;
        }

        const groups = allPeriod.groups || [];
        for (const group of groups) {
            const groupName = group.groupName;
            const statisticsItems = group.statisticsItems || [];

            if (groupName === 'Expected') {
                expectedGoals(statisticsItems);
            } else if (groupName === 'Possession') {
                possession(statisticsItems);
            } else if (groupName === 'Shots') {
                shots(statisticsItems);
            } else if (groupName === 'TVData') {
                tvData(statisticsItems);
            } else if (groupName === 'Shots extra') {
                shotsExtra(statisticsItems);
            } else if (groupName === 'Passes') {
                passes(statisticsItems);
            } else if (groupName === 'Duels') {
                duels(statisticsItems);
            } else if (groupName === 'Defending') {
                defending(statisticsItems);
            }
        }
    } else {
        throw new Error(`Error fetching match statistics, status code: ${response.status}`);
    }
}

function expectedGoals(statisticsItems) {
    for (const statistic of statisticsItems) {
        if (statistic.name === 'Expected goals') {
            stats['expected_goals_home'] = statistic.homeValue;
            stats['expected_goals_away'] = statistic.awayValue;
        }
    }
}

function possession(statisticsItems) {
    for (const statistic of statisticsItems) {
        if (statistic.name === 'Ball possession') {
            stats['possession_home'] = statistic.homeValue;
            stats['possession_away'] = statistic.awayValue;
        }
    }
}

function shots(statisticsItems) {
    for (const statistic of statisticsItems) {
        switch (statistic.name) {
            case 'Total shots':
                stats['total_shots_home'] = statistic.homeValue;
                stats['total_shots_away'] = statistic.awayValue;
                break;
            case 'Shots on target':
                stats['shots_on_target_home'] = statistic.homeValue;
                stats['shots_on_target_away'] = statistic.awayValue;
                break;
            case 'Shots off target':
                stats['shots_off_target_home'] = statistic.homeValue;
                stats['shots_off_target_away'] = statistic.awayValue;
                break;
            case 'Blocked shots':
                stats['blocked_shots_home'] = statistic.homeValue;
                stats['blocked_shots_away'] = statistic.awayValue;
                break;
        }
    }
}

function tvData(statisticsItems) {
    for (const statistic of statisticsItems) {
        switch (statistic.name) {
            case 'Corner kicks':
                stats['corners_home'] = statistic.homeValue;
                stats['corners_away'] = statistic.awayValue;
                break;
            case 'Offsides':
                stats['offsides_home'] = statistic.homeValue;
                stats['offsides_away'] = statistic.awayValue;
                break;
            case 'Fouls':
                stats['fouls_home'] = statistic.homeValue;
                stats['fouls_away'] = statistic.awayValue;
                break;
            case 'Yellow cards':
                stats['yellow_cards_home'] = statistic.homeValue;
                stats['yellow_cards_away'] = statistic.awayValue;
                break;
            case 'Red cards':
                stats['red_cards_home'] = statistic.homeValue;
                stats['red_cards_away'] = statistic.awayValue;
                break;
            case 'Free kicks':
                stats['free_kicks_home'] = statistic.homeValue;
                stats['free_kicks_away'] = statistic.awayValue;
                break;
            case 'Throw-ins':
                stats['throw_ins_home'] = statistic.homeValue;
                stats['throw_ins_away'] = statistic.awayValue;
                break;
            case 'Goal kicks':
                stats['goal_kicks_home'] = statistic.homeValue;
                stats['goal_kicks_away'] = statistic.awayValue;
                break;
        }
    }

    if (!stats['red_cards_home']) {
        stats['red_cards_home'] = 0;
    }
    if (!stats['red_cards_away']) {
        stats['red_cards_away'] = 0;
    }
}

function shotsExtra(statisticsItems) {
    for (const statistic of statisticsItems) {
        switch (statistic.name) {
            case 'Big chances':
                stats['big_chances_home'] = statistic.homeValue;
                stats['big_chances_away'] = statistic.awayValue;
                break;
            case 'Big chances missed':
                stats['big_chances_missed_home'] = statistic.homeValue;
                stats['big_chances_missed_away'] = statistic.awayValue;
                break;
            case 'Counter attacks':
                stats['counter_attacks_home'] = statistic.homeValue;
                stats['counter_attacks_away'] = statistic.awayValue;
                break;
            case 'Counter attack shots':
                stats['counter_attacks_shots_home'] = statistic.homeValue;
                stats['counter_attacks_shots_away'] = statistic.awayValue;
                break;
            case 'Shots inside box':
                stats['shots_inside_box_home'] = statistic.homeValue;
                stats['shots_inside_box_away'] = statistic.awayValue;
                break;
            case 'Shots outside box':
                stats['shots_outside_box_home'] = statistic.homeValue;
                stats['shots_outside_box_away'] = statistic.awayValue;
                break;
            case 'Goalkeeper saves':
                stats['goalkeeper_saves_home'] = statistic.homeValue;
                stats['goalkeeper_saves_away'] = statistic.awayValue;
                break;
        }
    }
}

function passes(statisticsItems) {
    for (const statistic of statisticsItems) {
        switch (statistic.name) {
            case 'Passes':
                stats['passes_home'] = statistic.homeValue;
                stats['passes_away'] = statistic.awayValue;
                break;
            case 'Accurate passes':
                stats['accurate_passes_home'] = statistic.homeValue;
                stats['accurate_passes_away'] = statistic.awayValue;
                break;
            case 'Long balls':
                stats['long_balls_home'] = statistic.homeValue;
                stats['long_balls_away'] = statistic.awayValue;
                break;
            case 'Crosses':
                stats['crosses_home'] = statistic.homeValue;
                stats['crosses_away'] = statistic.awayValue;
                break;
        }
    }
}

function duels(statisticsItems) {
    for (const statistic of statisticsItems) {
        switch (statistic.name) {
            case 'Dribbles':
                stats['dribbles_home'] = statistic.homeValue;
                stats['dribbles_away'] = statistic.awayValue;
                break;
            case 'Possession lost':
                stats['possession_lost_home'] = statistic.homeValue;
                stats['possession_lost_away'] = statistic.awayValue;
                break;
            case 'Duels won':
                stats['duels_won_home'] = statistic.homeValue;
                stats['duels_won_away'] = statistic.awayValue;
                break;
            case 'Aerials won':
                stats['aerials_won_home'] = statistic.homeValue;
                stats['aerials_won_away'] = statistic.awayValue;
                break;
        }
    }
}

function defending(statisticsItems) {
    for (const statistic of statisticsItems) {
        switch (statistic.name) {
            case 'Tackles':
                stats['tackles_home'] = statistic.homeValue;
                stats['tackles_away'] = statistic.awayValue;
                break;
            case 'Interceptions':
                stats['interceptions_home'] = statistic.homeValue;
                stats['interceptions_away'] = statistic.awayValue;
                break;
            case 'Clearances':
                stats['clearances_home'] = statistic.homeValue;
                stats['clearances_away'] = statistic.awayValue;
                break;
        }
    }
}

function restartStats() {
    for (const key of statsKeys) {
        stats[key] = null;
    }
}

async function main() {
    const fs = require('fs');
    const csvWriter = require('csv-writer').createObjectCsvWriter;

    const writer = csvWriter({
        path: `${folder}/stats_${year}.csv`,
        header: statsKeys.map((key) => ({ id: key, title: key })),
    });

    await writer.writeRecords([statsKeys]); // Write header

    for (let round = 1; round <= total_rounds; round++) {
        console.log(`Round ${round}`);
        const events = await getRoundData(competitionId, seasonId, round);
        for (const event of events) {
            restartStats();
            stats['round'] = round;

            const status = event.status?.code ?? 0;
            if (status === 100) {
                const matchId = await getMatchId(event);
                await getMatchScore(event, matchId);
                await getMatchStatistics(matchId);

                await writer.writeRecords([stats]); // Write data to CSV
            }
        }
    }
}

main();
