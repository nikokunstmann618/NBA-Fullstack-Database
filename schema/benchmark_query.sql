SELECT
    p.PLAYER_NAME,
    t.ABBREVIATION as team,
    p.SEASON,
    COUNT(gd.GAME_ID) as games_played,
    ROUND(AVG(gd.PTS), 2) as avg_points,
    ROUND(AVG(gd.REB), 2) as avg_rebounds,
    ROUND(AVG(gd.AST), 2) as avg_assists
FROM players p
INNER JOIN teams t ON p.TEAM_ID = t.TEAM_ID
INNER JOIN games_details gd ON p.PLAYER_ID = gd.PLAYER_ID
WHERE p.PLAYER_NAME LIKE '%James%'
GROUP BY p.PLAYER_NAME, t.ABBREVIATION, p.SEASON
ORDER BY p.SEASON DESC;

