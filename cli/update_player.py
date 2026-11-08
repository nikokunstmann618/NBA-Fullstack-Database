import sys
import os
import argparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dal.nba_dal import update_player, get_player_by_id

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Update NBA player information',
        epilog='At least one update option (--team, --season, or --name) must be provided.'
    )
    
    parser.add_argument('player_id', type=int, help='Player ID to update')
    parser.add_argument('--team', type=str, help='New team abbreviation (e.g., LAL, GSW)')
    parser.add_argument('--season', type=int, help='New season year (e.g., 2023)')
    parser.add_argument('--name', type=str, help='New player name')
    
    return parser.parse_args()


def display_before_after(before, after):
    print("\n" + "=" * 70)
    print("PLAYER UPDATE SUMMARY")
    print("=" * 70)
    
    print("\nBEFORE:")
    print(f" Player ID: {before.player_id}")
    print(f" Name: {before.player_name}")
    print(f" Team: {before.team.abbreviation} ({before.team.nickname})")
    print(f" Season: {before.season}")
    
    print("\nAFTER:")
    print(f" Player ID: {after.player_id}")
    print(f" Name: {after.player_name}")
    print(f" Team: {after.team.abbreviation} ({after.team.nickname})")
    print(f" Season: {after.season}")
    
    print("\n Player updated successfully!")
    print("=" * 70)
    
def main():
    try:
        args = parse_arguments()
    except SystemExit:
        return
    
    
    if not any([args.team, args.season, args.name]):
        print("Error: At least one update option (--team, --season, or --name) must be provided.")
        print("\nUse -h or --help for usage information.")
        sys.exit(1)
        
    try:
        if 'DB_URL' not in os.environ:
            print("Error: DB_URL environment variable is not set.")
            print("Please set your database connection string:")
            print(" PowerShell: $env: DB_URL = 'postgresql://username:password@localhost/database'")
            sys.exit(1)
            
        print(f"Retrieving player {args.player_id}...")
        before = get_player_by_id(args.player_id)
        
        if not before:
            print(f"\n Error: No player found with ID {args.player_id}")
            print("Tip: Use search_players.py to find valid player IDs")
            sys.exit(1)
            
        
        if args.team and len(args.team) != 3:
            print(f"Error: Team abbreviation must be 3 characters (got '{args.team}')")
            sys.exit(1)
            
        
        if args.season and (args.season < 2000 or args.season > 2030):
            print(f"Error: Season {args.season} seems invalid. Expected range: 2000-2030")
            sys.exit(1)
            
        
        print("Updating player...")
        after = update_player(
            args.player_id,
            team_abbreviation=args.team.upper() if args.team else None,
            season=args.season,
            player_name=args.name
        )
        
        if not after:
            print(f"\n Error: Update failed. Team '{args.team}' may not exist.")
            print("Valid team abbreviations include: LAL, GSW, BOS, MIA, etc.")
            sys.exit(1)
            
        display_before_after(before, after)
        
    except Exception as e:
        print(f"\n Database Error: {e}")
        print("Please check your database connection and try again.")
        sys.exit(1)
        
if __name__ == "__main__":
    main()
    