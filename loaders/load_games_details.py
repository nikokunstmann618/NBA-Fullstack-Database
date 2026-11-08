import csv
import os
from sqlalchemy import create_engine, text

db = create_engine(os.environ['DB_URL'])

seen_game_players = set()
valid_players = set()
valid_games = set()

print("Loading valid player and game IDs...", flush=True)
with db.connect() as conn:
    result = conn.execute(text("SELECT PLAYER_ID FROM players"))
    valid_players = {row[0] for row in result}
    
    result = conn.execute(text("SELECT GAME_ID FROM games"))
    valid_games = {row[0] for row in result}

print(f"Found {len(valid_players)} players and {len(valid_games)} games", flush=True)

print('BEGIN;')

GAMES_DETAILS_FILE = r'nba-data/games_details.csv'

def sql_quote(s):
    if not s or s.strip() == '':
        return 'NULL'
    return "'" + str(s).replace("'", "''") + "'"

def sql_num(s):
    if not s or s.strip() == '':
        return 'NULL'
    s = s.strip()
    
    try:
        num = float(s)
        if s.endswith('.0'):
            return str(int(num))
        if 0 <= num <= 1:
            return str(round(num, 3))
        if num == int(num):
            return str(int(num))
        return str(round(num, 3))
    except ValueError:
        return s

skipped = 0
inserted = 0

with open(GAMES_DETAILS_FILE, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        game_id_raw = row.get('GAME_ID')
        player_id_raw = row.get('PLAYER_ID')
        
        try:
            game_id_int = int(game_id_raw) if game_id_raw else None
            player_id_int = int(player_id_raw) if player_id_raw else None
            
            if game_id_int not in valid_games or player_id_int not in valid_players:
                skipped += 1
                continue
        except (ValueError, TypeError):
            skipped += 1
            continue
        
        # Skip duplicates
        game_player_key = (game_id_raw, player_id_raw)
        if game_player_key in seen_game_players:
            skipped += 1
            continue
        seen_game_players.add(game_player_key)
        
        game_id = sql_num(game_id_raw)
        team_id = sql_num(row.get('TEAM_ID'))
        player_id = sql_num(player_id_raw)
        team_abbreviation = sql_quote(row.get('TEAM_ABBREVIATION'))
        team_city = sql_quote(row.get('TEAM_CITY'))
        player_name = sql_quote(row.get('PLAYER_NAME'))
        nickname = sql_quote(row.get('NICKNAME'))
        start_position = sql_quote(row.get('START_POSITION'))
        comment = sql_quote(row.get('COMMENT'))
        min_time = sql_quote(row.get('MIN'))
        fgm = sql_num(row.get('FGM'))
        fga = sql_num(row.get('FGA'))
        fg_pct = sql_num(row.get('FG_PCT'))
        fg3m = sql_num(row.get('FG3M'))
        fg3a = sql_num(row.get('FG3A'))
        fg3_pct = sql_num(row.get('FG3_PCT'))
        ftm = sql_num(row.get('FTM'))
        fta = sql_num(row.get('FTA'))
        ft_pct = sql_num(row.get('FT_PCT'))
        oreb = sql_num(row.get('OREB'))
        dreb = sql_num(row.get('DREB'))
        reb = sql_num(row.get('REB'))
        ast = sql_num(row.get('AST'))
        stl = sql_num(row.get('STL'))
        blk = sql_num(row.get('BLK'))
        to = sql_num(row.get('TO'))
        pf = sql_num(row.get('PF'))
        pts = sql_num(row.get('PTS'))
        plus_minus = sql_num(row.get('PLUS_MINUS'))

        print(f"INSERT INTO games_details VALUES({game_id}, {team_id}, {player_id}, {team_abbreviation}, {team_city}, {player_name}, {nickname}, {start_position}, {comment}, {min_time}, {fgm}, {fga}, {fg_pct}, {fg3m}, {fg3a}, {fg3_pct}, {ftm}, {fta}, {ft_pct}, {oreb}, {dreb}, {reb}, {ast}, {stl}, {blk}, {to}, {pf}, {pts}, {plus_minus});")
        inserted += 1

print('COMMIT;')
print(f"-- Inserted: {inserted}, Skipped: {skipped}", flush=True)