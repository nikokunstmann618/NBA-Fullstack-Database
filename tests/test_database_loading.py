#!/usr/bin/env python3
"""
Test script to verify NBA database has been loaded correctly.
This checks row counts, data integrity, and foreign key relationships.

Usage:
    python test_database_loading.py
"""

import os
import sys
from sqlalchemy import create_engine, text

def test_database():
    """Run comprehensive tests on the NBA database."""
    
    # Check for DB_URL
    if 'DB_URL' not in os.environ:
        print("ERROR: DB_URL environment variable is not set.")
        print("Please set it like: export DB_URL='postgresql://user:pass@localhost/dbname'")
        return False
    
    try:
        db = create_engine(os.environ['DB_URL'])
        print(" Successfully connected to database\n")
    except Exception as e:
        print(f" ERROR: Could not connect to database: {e}")
        return False
    
    all_tests_passed = True
    
    with db.connect() as conn:
        print("=" * 70)
        print("TABLE ROW COUNTS")
        print("=" * 70)
        
        # Test 1: Check teams table
        result = conn.execute(text("SELECT COUNT(*) FROM teams"))
        teams_count = result.scalar()
        print(f"Teams: {teams_count} rows")
        if teams_count == 0:
            print(" WARNING: No teams found!")
            all_tests_passed = False
        elif teams_count == 30:
            print(" Expected ~30 NBA teams")
        else:
            print(f" Found {teams_count} teams (expected ~30)")
        
        # Test 2: Check players table
        result = conn.execute(text("SELECT COUNT(*) FROM players"))
        players_count = result.scalar()
        print(f"\nPlayers: {players_count} rows")
        if players_count == 0:
            print(" ERROR: No players found!")
            all_tests_passed = False
        else:
            print(f" Players loaded")
        
        # Test 3: Check games table
        result = conn.execute(text("SELECT COUNT(*) FROM games"))
        games_count = result.scalar()
        print(f"\nGames: {games_count} rows")
        if games_count == 0:
            print(" ERROR: No games found!")
            all_tests_passed = False
        else:
            print(f" Games loaded")
        
        # Test 4: Check games_details table
        result = conn.execute(text("SELECT COUNT(*) FROM games_details"))
        details_count = result.scalar()
        print(f"\nGames Details: {details_count} rows")
        if details_count == 0:
            print(" ERROR: No game details found!")
            all_tests_passed = False
        else:
            print(f" Game details loaded")
        
        print("\n" + "=" * 70)
        print("DATA INTEGRITY CHECKS")
        print("=" * 70)
        
        # Test 5: Check for NULL team_ids in players
        result = conn.execute(text("SELECT COUNT(*) FROM players WHERE TEAM_ID IS NULL"))
        null_teams = result.scalar()
        print(f"\nPlayers with NULL team_id: {null_teams}")
        if null_teams > 0:
            print(f" WARNING: {null_teams} players have no team assigned")
        else:
            print(" All players have teams")
        
        # Test 6: Check foreign key integrity - players to teams
        result = conn.execute(text("""
            SELECT COUNT(*) 
            FROM players p 
            LEFT JOIN teams t ON p.TEAM_ID = t.TEAM_ID 
            WHERE p.TEAM_ID IS NOT NULL AND t.TEAM_ID IS NULL
        """))
        orphaned_players = result.scalar()
        print(f"\nPlayers with invalid team_id: {orphaned_players}")
        if orphaned_players > 0:
            print(f" ERROR: {orphaned_players} players reference non-existent teams!")
            all_tests_passed = False
        else:
            print(" All player team references are valid")
        
        # Test 7: Check foreign key integrity - games to teams
        result = conn.execute(text("""
            SELECT COUNT(*) 
            FROM games g 
            LEFT JOIN teams ht ON g.HOME_TEAM_ID = ht.TEAM_ID 
            WHERE g.HOME_TEAM_ID IS NOT NULL AND ht.TEAM_ID IS NULL
        """))
        orphaned_home_games = result.scalar()
        
        result = conn.execute(text("""
            SELECT COUNT(*) 
            FROM games g 
            LEFT JOIN teams vt ON g.VISITOR_TEAM_ID = vt.TEAM_ID 
            WHERE g.VISITOR_TEAM_ID IS NOT NULL AND vt.TEAM_ID IS NULL
        """))
        orphaned_away_games = result.scalar()
        
        print(f"\nGames with invalid home team: {orphaned_home_games}")
        print(f"Games with invalid visitor team: {orphaned_away_games}")
        if orphaned_home_games > 0 or orphaned_away_games > 0:
            print(f" ERROR: Some games reference non-existent teams!")
            all_tests_passed = False
        else:
            print(" All game team references are valid")
        
        # Test 8: Check foreign key integrity - games_details
        result = conn.execute(text("""
            SELECT COUNT(*) 
            FROM games_details gd 
            LEFT JOIN games g ON gd.GAME_ID = g.GAME_ID 
            WHERE g.GAME_ID IS NULL
        """))
        orphaned_details_games = result.scalar()
        
        result = conn.execute(text("""
            SELECT COUNT(*) 
            FROM games_details gd 
            LEFT JOIN players p ON gd.PLAYER_ID = p.PLAYER_ID 
            WHERE p.PLAYER_ID IS NULL
        """))
        orphaned_details_players = result.scalar()
        
        print(f"\nGame details with invalid game_id: {orphaned_details_games}")
        print(f"Game details with invalid player_id: {orphaned_details_players}")
        if orphaned_details_games > 0 or orphaned_details_players > 0:
            print(f" ERROR: Some game details have invalid references!")
            all_tests_passed = False
        else:
            print(" All game detail references are valid")
        
        print("\n" + "=" * 70)
        print("SAMPLE DATA CHECKS")
        print("=" * 70)
        
        # Test 9: Show sample teams
        print("\nSample Teams:")
        result = conn.execute(text("""
            SELECT ABBREVIATION, NICKNAME, CITY 
            FROM teams 
            ORDER BY ABBREVIATION 
            LIMIT 5
        """))
        for row in result:
            print(f"  {row[0]}: {row[2]} {row[1]}")
        
        # Test 10: Show sample players
        print("\nSample Players:")
        result = conn.execute(text("""
            SELECT p.PLAYER_NAME, t.ABBREVIATION, p.SEASON 
            FROM players p
            JOIN teams t ON p.TEAM_ID = t.TEAM_ID
            ORDER BY p.PLAYER_NAME 
            LIMIT 5
        """))
        for row in result:
            print(f"  {row[0]} ({row[1]}, {row[2]})")
        
        # Test 11: Show sample games
        print("\nSample Games:")
        result = conn.execute(text("""
            SELECT g.GAME_DATE_EST, ht.ABBREVIATION, vt.ABBREVIATION, 
                   g.PTS_home, g.PTS_away
            FROM games g
            JOIN teams ht ON g.HOME_TEAM_ID = ht.TEAM_ID
            JOIN teams vt ON g.VISITOR_TEAM_ID = vt.TEAM_ID
            ORDER BY g.GAME_DATE_EST DESC
            LIMIT 5
        """))
        for row in result:
            print(f"  {row[0]}: {row[1]} {row[3]} - {row[4]} {row[2]}")
        
        # Test 12: Check seasons available
        print("\nSeasons available:")
        result = conn.execute(text("""
            SELECT DISTINCT SEASON 
            FROM games 
            ORDER BY SEASON
        """))
        seasons = [row[0] for row in result]
        print(f"  {', '.join(map(str, seasons))}")
        if len(seasons) == 0:
            print(" WARNING: No seasons found in games!")
            all_tests_passed = False
        
    print("\n" + "=" * 70)
    if all_tests_passed:
        print(" ALL TESTS PASSED - Database is properly loaded!")
    else:
        print(" SOME ISSUES FOUND - See warnings/errors above")
    print("=" * 70)
    
    return all_tests_passed


if __name__ == "__main__":
    success = test_database()
    sys.exit(0 if success else 1)