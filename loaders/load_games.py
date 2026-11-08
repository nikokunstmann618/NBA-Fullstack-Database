import csv

seen_games = set()

print('BEGIN;')

GAMES_FILE = r'nba-data/games.csv'

def sql_quote(s):
    if not s or s.strip() == '':
        return 'NULL'
    return "'" + str(s).replace("'", "''") + "'"

def sql_num(s):
    """Normalize numeric CSV strings for SQL literals."""
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

with open(GAMES_FILE, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        game_id = row.get('GAME_ID')
        
        if game_id in seen_games:
            continue
        seen_games.add(game_id)
        
        game_id = sql_num(game_id)
        game_date_est = row.get('GAME_DATE_EST')
        if game_date_est and game_date_est.strip() != '':
            game_date_est = f"'{game_date_est}'"
        else:
            game_date_est = 'NULL'
        game_status_text = sql_quote(row.get('GAME_STATUS_TEXT'))
        home_team_id = sql_num(row.get('HOME_TEAM_ID'))
        visitor_team_id = sql_num(row.get('VISITOR_TEAM_ID'))
        season = sql_num(row.get('SEASON'))
        team_id_home = sql_num(row.get('TEAM_ID_home'))
        pts_home = sql_num(row.get('PTS_home'))
        fg_pct_home = sql_num(row.get('FG_PCT_home'))
        ft_pct_home = sql_num(row.get('FT_PCT_home'))
        fg3_pct_home = sql_num(row.get('FG3_PCT_home'))
        ast_home = sql_num(row.get('AST_home'))
        reb_home = sql_num(row.get('REB_home'))
        team_id_away = sql_num(row.get('TEAM_ID_away'))
        pts_away = sql_num(row.get('PTS_away'))
        fg_pct_away = sql_num(row.get('FG_PCT_away'))
        ft_pct_away = sql_num(row.get('FT_PCT_away'))
        fg3_pct_away = sql_num(row.get('FG3_PCT_away'))
        ast_away = sql_num(row.get('AST_away'))
        reb_away = sql_num(row.get('REB_away'))
        home_team_wins = sql_num(row.get('HOME_TEAM_WINS'))

        print(f"INSERT INTO games VALUES({game_id}, {game_date_est}, {game_status_text}, {home_team_id}, {visitor_team_id}, {season}, {team_id_home}, {pts_home}, {fg_pct_home}, {ft_pct_home}, {fg3_pct_home}, {ast_home}, {reb_home}, {team_id_away}, {pts_away}, {fg_pct_away}, {ft_pct_away}, {fg3_pct_away}, {ast_away}, {reb_away}, {home_team_wins});")

print('COMMIT;')