# NBA Player Performance Tracker

A full-stack relational database application built on PostgreSQL and Python, using ~400,000 records of NBA game data from 2003–2022. It covers the whole stack: schema design, data loading, indexing, a SQLAlchemy data access layer with transactional CRUD, and a command-line interface on top.

Built as the final project for CMSI 3520 Database Systems at Loyola Marymount University (Fall 2025).

![Entity-relationship diagram](schema/NBA%20Dataset%20Schema.png)

## Highlights

- **Normalized relational schema** with four tables (`teams`, `players`, `games`, `games_details`) and foreign keys enforcing integrity across 26,622 games and 372,185 player-game records.
- **Data loaders** that turn the raw Kaggle CSVs into SQL and load them in dependency order.
- **Indexing with measured impact**: six targeted indexes cut execution time on a representative multi-join aggregate query from 318.7 ms to 194.2 ms (**39% faster**) and planning time by 47%, verified with `EXPLAIN ANALYZE`.
- **Data access layer** (SQLAlchemy ORM + raw SQL) with search, statistics, and full create/read/update/delete operations.
- **Transactions**: multi-table operations such as deleting a player run atomically, so the database is never left half-updated.
- **CLI programs** for searching, viewing, adding, updating, and deleting players.

## Tech Stack

PostgreSQL · Python · SQLAlchemy · psycopg2

## Project Structure

```
schema/     DDL, indexes, benchmark query, and ER diagram
loaders/    Scripts that convert the CSV dataset into SQL inserts
dal/        Data access layer (nba_dal.py)
cli/        Command-line programs built on the DAL
tests/      Data-load verification script
about.md    Dataset, application use cases, and design rationale
setup.md    Full setup guide and indexing benchmark results
```

## Data Access Layer

| Function | Purpose |
| --- | --- |
| `search_players_by_team` | Players on a team, optionally filtered by season |
| `search_players_by_name` | Partial-match player search |
| `get_player_by_id` | Single player lookup |
| `get_player_average_stats` | Career or season averages (points, rebounds, assists, steals, blocks) |
| `get_team_season_record` | Win–loss record combining home and away games |
| `add_player_to_team` | Create a player-season record |
| `update_player` | Change team, season, or name (transactional) |
| `delete_player` | Remove a player and their game records atomically |

## Quick Start

1. Download the [NBA Games dataset](https://www.kaggle.com/datasets/nathanlauga/nba-games) and place the CSVs in `nba-data/`.
2. Create a PostgreSQL database and set `DB_URL`, e.g. `postgresql://postgres:<password>@localhost/nba_db`.
3. Install dependencies: `pip install sqlalchemy psycopg2-binary`
4. Create the schema, load the data, and add indexes, following the steps in [setup.md](setup.md).
5. Try the CLI:

```bash
python cli/search_players.py LAL 2019
python cli/get_player.py 2544
```

## Design Notes

PostgreSQL was chosen over MongoDB and Neo4j (both prototyped earlier in the course) because the data is naturally relational, the application depends on joins and aggregates, and foreign keys plus transactions keep the data consistent. The full rationale, including trade-offs and lessons learned, is in [about.md](about.md).
