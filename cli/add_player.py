#!/usr/bin/env python3
"""
NBA Player Management Program

This program demonstrates the NBA DAL CUD functions by adding new players
to teams in the database.

Usage:
    python add_player.py <player_name> <team_abbreviation> <season>
    
Examples:
    python add_player.py "LeBron James" LAL 2021
    python add_player.py "Stephen Curry" GSW 2022
    python add_player.py "Jayson Tatum" BOS 2023
"""

import sys
import os


if 'dal.nba_dal' in sys.modules:
    del sys.modules['dal.nba_dal']

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


from dal.nba_dal import add_player_to_team


def print_help():
    print(__doc__)


def validate_arguments(args):
    if len(args) != 4:
        print("Error: All three arguments are required.")
        print_help()
        return False
    
    player_name = args[1]
    team_abbreviation = args[2].upper()
    season_str = args[3]
    
    if not player_name or len(player_name.strip()) == 0:
        print("Error: Player name cannot be empty.")
        return False
    
    if len(team_abbreviation) != 3:
        print(f"Error: Team abbreviation '{team_abbreviation}' should be 3 characters.")
        return False
    
    try:
        season = int(season_str)
        if season < 2000 or season > 2030:
            print(f"Error: Season '{season}' seems invalid. Expected range: 2000-2030")
            return False
    except ValueError:
        print(f"Error: Season '{season_str}' is not a valid number.")
        return False
    
    return True


def display_success(player, team_abbreviation, season):
    print(f"\n Successfully added player to database!")
    print("-" * 50)
    print(f"Player Name: {player.player_name}")
    print(f"Team: {team_abbreviation}")
    print(f"Season: {season}")
    print(f"Player ID: {player.player_id}")
    print(f"Team ID: {player.team_id}")


def display_error(error_type, details=""):
    if error_type == "team_not_found":
        print(f" Error: Team '{details}' not found in database.")
        print("Please check the team abbreviation and try again.")
        print("Valid team abbreviations include: LAL, GSW, BOS, MIA, etc.")
    
    elif error_type == "database_error":
        print(f" Database Error: {details}")
        print("Please check your database connection and try again.")
    
    elif error_type == "validation_error":
        print(f" Validation Error: {details}")
    
    else:
        print(f" Unexpected Error: {details}")


def main():
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', 'help']:
        print_help()
        return
    
    if not validate_arguments(sys.argv):
        sys.exit(1)
    
    player_name = sys.argv[1].strip()
    team_abbreviation = sys.argv[2].upper()
    season = int(sys.argv[3])
    
    try:
        if 'DB_URL' not in os.environ:
            print("Error: DB_URL environment variable is not set.")
            print("Please set your database connection string:")
            print("  export DB_URL='postgresql://username:password@localhost/database'")
            sys.exit(1)
        
        print(f"Adding player '{player_name}' to team '{team_abbreviation}' for season {season}...")
        
        player = add_player_to_team(player_name, team_abbreviation, season)
        
        if player:
            display_success(player, team_abbreviation, season)
        else:
            display_error("team_not_found", team_abbreviation)
            sys.exit(1)
        
    except Exception as e:
        display_error("database_error", str(e))
        sys.exit(1)
    

if __name__ == "__main__":
    main()
