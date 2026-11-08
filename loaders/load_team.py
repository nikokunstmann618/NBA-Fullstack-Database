import csv


print('BEGIN;')

TEAMS_FILE = r'nba-data/teams.csv'

with open(TEAMS_FILE, 'r', encoding ='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        team_id = row['TEAM_ID']
        league_id = row['LEAGUE_ID'] if row['LEAGUE_ID'] else 'NULL'
        min_year = row['MIN_YEAR'] if row['MIN_YEAR'] else 'NULL'
        max_year = row['MAX_YEAR'] if row['MAX_YEAR'] else 'NULL'
        abbreviation = row['ABBREVIATION'].replace("'", "''")
        nickname = row['NICKNAME'].replace("'", "''")
        year_founded = row['YEARFOUNDED'] if row['YEARFOUNDED'] else 'NULL'
        city = row['CITY'].replace("'", "''")
        arena = row['ARENA'].replace("'", "''") if row['ARENA'] else 'NULL'
        arena_capacity = row['ARENACAPACITY'] if row['ARENACAPACITY'] else 'NULL'
        owner = row['OWNER'].replace("'", "''") if row['OWNER'] else 'NULL'
        general_manager = row['GENERALMANAGER'].replace("'", "''") if row['GENERALMANAGER'] else 'NULL'
        head_coach = row['HEADCOACH'].replace("'", "''") if row['HEADCOACH'] else 'NULL'
        d_league_affiliation = row['DLEAGUEAFFILIATION'].replace("'", "''") if row['DLEAGUEAFFILIATION'] else 'NULL'

        print(f"INSERT INTO teams VALUES({team_id}, {league_id}, {min_year}, {max_year}, '{abbreviation}', '{nickname}', {year_founded}, '{city}', '{arena}', {arena_capacity}, '{owner}', '{general_manager}', '{head_coach}', '{d_league_affiliation}');")

print('COMMIT;')