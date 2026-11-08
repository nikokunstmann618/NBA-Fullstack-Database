import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dal.nba_dal import get_player_by_id

def print_help():
    print(__doc__)
    

def validate_arguments(args):
    if len(args) != 2:
        print("Error: Player ID is required.")
        print_help()
        return False
    
    try:
        player_id = int(args[1])
        if player_id <= 0:
            print(f"Error: Player ID must be a positive number.")
            return False
        
    except ValueError:
        print(f"Error: '{args[1]}' is not a valid player ID.")
        return False
    
    return True

def display_player(player):
    print("\n" + "=" * 60)
    print("PLAYER INFORMATION")
    print("=" * 60)
    print(f"Player ID: {player.player_id}")
    print(f"Player Name: {player.player_name}")
    print(f"Team: {player.team.city} {player.team.nickname} ({player.team.abbreviation})")
    print(f"Season: {player.season}--{player.season + 1}")
    print(f"Team ID: {player.team_id}")
    print("=" * 60)
    

def main():
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', 'help']:
        print_help()
        return
    
    if not validate_arguments(sys.argv):
        sys.exit(1)
        
    player_id = int(sys.argv[1])
    
    try:
        if 'DB_URL' not in os.environ:
            print("Error: DB_URL environment variable is not set.")
            print("Please set your database connection string:")
            print("  PowerShell: $env:DB_URL = 'postgresql://username:password@localhost/database'")
            sys.exit(1)
            
        print(f"Retrieving player with ID {player_id}...")
        
        player = get_player_by_id(player_id)
        
        if player:
            display_player(player)
        else:
            print(f"\n Error: No player found with ID {player_id}")
            print("\nTip: Use search_players.py to find player IDs")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n Database Error: {e}")
        print("Please check your database connection and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()
            
        