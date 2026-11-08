import csv

seen_players = set()

print('BEGIN;')

PLAYERS_FILE = r'nba-data/players.csv'

with open(PLAYERS_FILE, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        player_id = row['PLAYER_ID']
        
        if player_id in seen_players:
            continue
        seen_players.add(player_id)
        
        player_name = row['PLAYER_NAME'].replace("'", "''")
        team_id = row['TEAM_ID'] if row['TEAM_ID'] else 'NULL'
        season = row['SEASON'] if row['SEASON'] else 'NULL'
        
        print(f"INSERT INTO players VALUES({player_id}, '{player_name}', {team_id}, {season});")

print('COMMIT;')

