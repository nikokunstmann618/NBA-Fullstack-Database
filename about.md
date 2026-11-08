# NBA Games Dataset

## Dataset Description

This dataset contains extensive NBA game data including games, player statistics, team information, and rankings.

**Source:** [NBA Games Dataset on Kaggle](https://www.kaggle.com/datasets/nathanlauga/nba-games?resource=download)

## What the Dataset Contains

- **games.csv**: Game-level data including dates, teams, scores, and outcomes (26,622 games from 2003-2022)
- **games_details.csv**: Individual player statistics for each game (372,185 player-game records)
- **players.csv**: Player information including names and team affiliations (1,769 unique player-season combinations)
- **teams.csv**: NBA team information (30 teams with historical data)

## Application: NBA Player Performance Tracker

### General Description

The NBA Player Performance Tracker is a database application for storing, querying, and analyzing NBA player and team statistics across multiple seasons. Users can track player performance, team records, and historical game data through a command-line interface backed by a data access layer.

### Prominent Use Cases

1. **Player Statistics Analysis**
   - Search for players by team and season
   - Calculate career or season averages for points, rebounds, assists, steals, and blocks
   - Track individual player performance across multiple seasons
   - **Underlying Data**: Joins `players`, `teams`, and `games_details` tables to aggregate stats

2. **Player Management**
   - Add new players to teams for specific seasons
   - Update player information when they get traded
   - Remove players from the database (retired players)
   - **Underlying Data**: CRUD operations on the `players` table with cascading to `games_details` to keep everything consistent

3. **Team Performance Tracking**
   - Calculate team win-loss records for specific seasons
   - Analyze team stats (home vs. away performance)
   - Track team roster changes over time
   - **Underlying Data**: Queries the `games` table with home/away logic, joined with `teams`

4. **Historical Game Analysis**
   - Search games by date, team, or season
   - Look at scoring trends and game outcomes
   - Compare player performances in specific games
   - **Underlying Data**: Queries `games` and `games_details` tables with various filters

## Rationale for PostgreSQL (Relational Database)

### Why PostgreSQL Was the Best Fit

After working with this dataset in PostgreSQL, MongoDB, and Neo4j throughout the semester, I chose **PostgreSQL** for these reasons:

1. **The Data Just Makes Sense Relationally**
   - NBA data has clear entities (teams, players, games) with obvious relationships
   - The relational model naturally captures how players belong to teams, and how games involve players
   - Foreign keys ensure data stays consistent 

2. **SQL Makes Complex Queries Way Easier**
   - This application needs a lot of JOINs between tables
   - Calculating averages and aggregating stats is straightforward with SQL's built-in functions
   - The query optimizer handles multi-table joins efficiently with the right indexes

3. **Transactions Actually Matter Here**
   - Deleting a player needs to remove them from multiple tables at once 
   - PostgreSQL's transaction support means either everything succeeds or nothing changes
   - This prevents scenarios where you delete half the data and then hit an error

4. **Indexing Works Really Well**
   - Adding indexes on player names and team abbreviations made queries noticeably faster
   - My benchmarks showed a 39% improvement in execution time after adding indexes
   - EXPLAIN ANALYZE made it easy to see what the database was actually doing

5. **Data Integrity is Built-In**
   - Foreign key constraints caught data issues during loading that would've been bugs later
   - The database enforces rules so I don't have to rely only on application-level checks
   - No orphaned records or invalid references

### What Wasn't Great About PostgreSQL

1. **Schema Changes Are a Pain**
   - Once I loaded all the data, I realized the players table should've had a composite primary key
   - Changing it would've meant dropping and reloading everything, so I just left it

2. **Some Queries Get Verbose**
   - Getting a team's season record required separate queries for home and away games
   - MongoDB's nested documents would've been simpler for this specific case

3. **Not Built for Massive Scale**
   - If this were handling millions of users or real-time game data, NoSQL might be better
   - But for a dataset with ~400k records, PostgreSQL handles it easily

## Assessment: How Did This Choice Work Out?

### What Worked Well

**Performance Was Great**: With proper indexes, queries ran fast. The benchmark showed execution time dropped from 318ms to 194ms (39% faster) just by adding a few indexes.

**Data Integrity Saved Me**: Foreign key constraints caught some issues during data loading. When I tried to load game details before players, it immediately failed. Same thing happened when there were invalid team IDs in the CSV files.

**SQL Was Easier to Use NOW**: Writing queries to calculate player averages, team records, and searching across multiple criteria was pretty straightforward. 

**Transactions Worked**: The delete_player() function needed to remove data from two tables atomically. In PostgreSQL this was pretty easy to do with transactions

### Challenges I Ran Into

**Schema Design Matters More Than I Thought**: I should've spent more time thinking about the players table structure upfront. Realizing it needed a composite primary key after loading 370k+ records was frustrating, but not worth the time to fix at that point.

**SQL Can Get Wordy**: Some queries needed multiple JOINs and subqueries. Getting a team's season record required querying home games and away games separately, then combining them in Python. MongoDB would've been cleaner for this specific query.

**NULL Values Are Confusing**: SQL's three-valued logic (TRUE/FALSE/NULL) tripped me up a few times, especially with optional fields like coach names or arena capacity.

### Final Thoughts

**PostgreSQL Works Well.** It gave me data integrity, flexible queries, and solid performance. MongoDB might've simplified some nested structures, and Neo4j could've modeled player-team relationships as a graph, but neither would've given me the same combo of performance, consistency, and ease of development.

For an NBA stats app that needs accurate calculations, complex queries, and data that stays consistent, **PostgreSQL's relational model was the best choice**. The time I spent on schema design and indexing paid off in faster queries and fewer bugs.

If I were to continue to expand on this, and have it accessible to millions of users or handgle live game data, there would have to be improvements. PostgreSQL did a good job though for its purposes.

## Database Schema

See `schema/schema-diagram.png` for the Entity-Relationship Diagram showing all tables, columns, and relationships.

The schema has four main tables:
- **teams**: Core team information (30 NBA franchises)
- **players**: Player-season records (one row per player per season)
- **games**: Game results and team statistics
- **games_details**: Individual player performance in each game

Key relationships:
- players -> teams (many-to-one via team_id)
- games -> teams (two relationships: home_team_id and visitor_team_id)
- games_details -> players (many-to-one via player_id)
- games_details -> games (many-to-one via game_id)
- games_details -> teams (many-to-one via team_id)