-- NBA Database Indexes
-- Indexes improve query performance for common search patterns

CREATE INDEX idx_players_name ON players(PLAYER_NAME);

CREATE INDEX idx_teams_abbreviation ON teams(ABBREVIATION);

CREATE INDEX idx_games_date ON games(GAME_DATE_EST);

CREATE INDEX idx_games_season ON games(SEASON);

CREATE INDEX idx_games_details_player ON games_details(PLAYER_ID);

CREATE INDEX idx_players_team_season ON players(TEAM_ID, SEASON);