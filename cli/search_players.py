#!/usr/bin/env python3
"""
NBA Player Search Program

This program demonstrates the NBA DAL retrieval functions by searching for players
and displaying their statistics.

Usage:
    python search_players.py <team_abbreviation> [season]
    
Examples:
    python search_players.py LAL
    python search_players.py GSW 2021
    python search_players.py BOS 2022
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dal.nba_dal import search_players_by_team, get_player_average_stats


def print_help():
    print(__doc__)


def validate_arguments(args):
    if len(args) < 2:
        print("Error: Team abbreviation is required.")
        print_help()
        return False
    
    team_abbreviation = args[1].upper()
    
    if len(team_abbreviation) != 3:
        print(f"Error: Team abbreviation '{team_abbreviation}' should be 3 characters.")
        return False
    
    if len(args) > 2:
        try:
            season = int(args[2])
            if season < 2000 or season > 2030:
                print(f"Error: Season '{season}' seems invalid. Expected range: 2000-2030")
                return False
        except ValueError:
            print(f"Error: Season '{args[2]}' is not a valid number.")
            return False
    
    return True


def display_player_results(players):
    if not players:
        print("No players found matching the criteria.")
        return
    
    print(f"\nFound {len(players)} player(s):")
    print("-" * 80)
    print(f"{'Player Name':<25} {'Team':<8} {'Season':<8} {'Player ID':<10}")
    print("-" * 80)
    
    for player in players:
        player_name = player[1] if len(player) > 1 else "Unknown"
        team_abbr = player[4] if len(player) > 4 else "Unknown"
        season = player[3] if len(player) > 3 else "Unknown"
        player_id = player[0] if len(player) > 0 else "Unknown"
        
        print(f"{player_name:<25} {team_abbr:<8} {season:<8} {player_id:<10}")


def display_player_stats(player_id, season=None):
    stats = get_player_average_stats(player_id, season)
    
    if stats:
        season_text = f" in {season}" if season else ""
        print(f"\nPlayer Statistics{season_text}:")
        print("-" * 40)
        print(f"Games Played: {stats['games_played']}")
        print(f"Average Points: {stats['avg_points']}")
        print(f"Average Rebounds: {stats['avg_rebounds']}")
        print(f"Average Assists: {stats['avg_assists']}")
        print(f"Average Steals: {stats['avg_steals']}")
        print(f"Average Blocks: {stats['avg_blocks']}")
    else:
        print(f"No statistics found for player ID {player_id}")


def main():
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', 'help']:
        print_help()
        return
    
    if not validate_arguments(sys.argv):
        sys.exit(1)
    
    team_abbreviation = sys.argv[1].upper()
    season = int(sys.argv[2]) if len(sys.argv) > 2 else None
    
    try:
        if 'DB_URL' not in os.environ:
            print("Error: DB_URL environment variable is not set.")
            print("Please set your database connection string:")
            print("  export DB_URL='postgresql://username:password@localhost/database'")
            sys.exit(1)
        
        print(f"Searching for players on team '{team_abbreviation}'" + 
              (f" in season {season}" if season else ""))
        
        players = search_players_by_team(team_abbreviation, season)
        
        display_player_results(players)
        
        """if players:
            first_player_id = players[0][0]
            print(f"\nShowing detailed stats for first player (ID: {first_player_id}):")
            display_player_stats(first_player_id, season)
        """
    except Exception as e:
        print(f"Error: {e}")
        print("Please check your database connection and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()