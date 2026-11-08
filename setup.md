# NBA Database Setup Guide

This guide provides complete instructions for settin up the NBA Player Performance Tracker using a relational database.


## Prerequisites

- PostgreSQL 12 or higher installed
- Python 3.8 or higher installed
- Required Python packages:
```bash
pip install sqlalchemy psycopg2-binary
```
- NBA dataset CSV files (download from [Kaggle](https://www.kaggle.com/datasets/nathanlauga/nba-games))

## Step 1: Download Dataset

1. Download the NBA Games dataset from Kaggle
2. Get the following CSV files into an `nba-data/` directory:
    - `teams.csv`
    - `players.csv`
    - `games.csv`
    - `games_details.csv`

**Note:** The `nba-data/` directory is excluded from git through `.gitignore` due to file size.

## Step 2: Create Database
```bash
# Connect to PostgreSQL
psql -U postgres

# Create the database
CREATE DATABASE nba_db;

# Exit psql
\q
```

## Step 3: Set Environment 
```bash

### On Windows PowerShell:
```powershell
$env:DB_URL = "postgresql://postgres:YOUR_PASSWORD@localhost/nba_db"


Replace `YOUR_PASSWORD` with your actual PostgreSQL password.

## Step 4: Create Schema
```bash
psql $env:DB_URL -f schema/schema.sql
```

This creates four tables:
- `teams` - NBA team information
- `players` - Player records by season
- `games` - Game results and statistics
- `games_details` - Individual player game statistics

## Step 5: Load Data

Load data in this specific order

```bash
# 1. Load teams
python loaders/load_teams.py | psql $env:DB_URL

# 2. Load players
python loaders/load_players.py | psql $env: DB_URL

# 3. Load games
python loaders/load_games.py | psql $env:DB_URL

# 4. Load game details
python loaders/load_games_details.py | psql $env: DB_URL
```

**Expected Results:**
- Teams: ~30 rows
- Players ~1,769 rows
- Games: ~26,622 rows
- Games Details: ~372,185 rows

## Step 6: Verify Data Load
```bash
python tests/test_database_loading.py
```

This test script verifies:
- All tables have data
- Foreign key relationships are valid
- No orphaned records exist
- Sample data displays correctly

## Step 7: Create Indexes

Create indexes to optimize query performance:
```bash
psql $env:DB_URL -f schema/indexes.sql
```

This creates the following indexes:
- `idx_players_name` - For player name searches
- `idx_teams_abbreviation` - For team lookups
- `idx_games_date` - For date range queries
- `idx_games_season` - For season filtering
- `idx_games_details_player` - For player statistics
- `idx_players_team_season` - For team+season queries

## Index Performance Impact

We benchmarked a representative query that searches for players by name and calculates their statistics across seasons:
```sql
SELECT p.PLAYER_NAME, t.ABBREVIATION, p.SEASON,
       COUNT(gd.GAME_ID) as games_played,
       AVG(gd.PTS) as avg_points
FROM players players p
INNER JOIN teams t ON p.TEAM_ID = t.TEAM_ID
INNER JOIN games_details gd ON p.PLAYER_ID = gd.PLAYER_ID
WHERE p.PLAYER_NAME LIKE '%James%'
GROUP BY p.PLAYER_NAME, t.ABBREVIATION, p.SEASON;
```

### Query Plan Changes

**BEFORE Indexes:**
```

Execution Time: 318.695 ms
Planning Time: 24.023 ms

Key observations:
- Parallel Seq Scan on games_details (cost=0.00..14045.00)
- Sequential scans on players and teams tables
- Buffers: shared hit=72 read=11592
- Heavy reliance on disk reads
```

**AFTER Indexes:**
```
Execution Time: 194.223 ms
Planning Time: 12.604 ms

Key observations:
- Parallel Seq Scan on games_details (cost=0.00..14045.84)
- Improved buffer utilization: shared hit=1388 read=10276
- Significantly more data served from memory(shared hit increased 19x)
- Faster query planning (47% reduction in planning time)
```

### Timing Results

| Metric | Before Indexes | After Indexes | Improvement

| Query Execution | 318.7 ms | 194.2 ms | **39% faster** |
| Planning Time | 24.0 ms | 12.6 ms | **47% faster** |
| Run 1 (total) | 435.1 ms | 460.5 ms | - |
| Run 2 (total) | 404.2 ms | 443.7 ms | - |
| Run 3 (total) | 391.3 ms | 519.2 ms | - |

**Note:** Total command times include connection above and can vary. The key metric is the query execution time from EXPLAIN ANALYZE, which shows a consistent **39% improvement**.

**Conclusion:** The indexes significantly improve query execution performance by increasing buffer cache hits (19x improvement) and reducing planning time. The 39% reduction in execution time shows the value of proper indexing for the player name searches and aggregate statistics queries, which are integral operations in the NBA Player Performance Tracker application.

## Step 8: Test the Application

Test the command-line interface programs:
```bash
# Search for players
python cli/search_players.py LAL 2019

# Get player details
python cli/get_player.py 2544

# Add a new player
python cli/add_player.py "Test Player" LAL 2019

# Update a player
python cli/update_player.py --team GSW --season 2019

# Delete a player
python cli/delete_player.py -- confirm
```

## Next Steps

Once setup is complete, you can:
1. Use the CLI programs to interact with the database
2. Import the DAL in your own Python applications
3. Explore the data with custom SQL queries
4. Extend the application with additional features



