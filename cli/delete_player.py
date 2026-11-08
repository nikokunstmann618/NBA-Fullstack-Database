import sys
import os
import argparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dal.nba_dal import delete_player, get_player_by_id

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Delete an NBA player from the database',
        epilog='WARNING: This action cannot be undone!'
    )
    
    parser.add_argument('player_id', type=int, help='Player ID to delete')
    parser.add_argument('--confirm', action='store_true',
                        help='Confirm deletion (required to proceed)')
    
    return parser.parse_args()

def display_deletion_summary(result):
    print("\n" + "=" * 70)
    print("DELETION SUMMARY")
    print("=" * 70)
    print(f"Player ID:  {result['player_id']}")
    print(f"Player Name:  {result['player_name']}")
    print(f"Game records deleted: {result['games_deleted']}")
    print(f"Player record deleted: {'Yes' if result['player_deleted'] else 'No'}")
    print("\n Player deleted successfully!")
    print("\nNOTE: This operation used a TRANSACTION to ensure both the player")
    print(" and their game records were deleted atomically.")
    print("=" * 70)
    
    
def main():
    try:
        args = parse_arguments()
    except SystemExit:
        return
    
    
    if not args.confirm:
        print("\n WARNING: This will permanently delete the player and all their game records!")
        print("\nTo confirm deletion, add the --confirm flag:")
        print(f" python delete_player.py {args.player_id} --confirm")
        sys.exit(1)
        
    
    try:
        if 'DB_URL' not in os.environ:
            print("Error: DB_URL environment variable is not set.")
            print("Please set your database connection string:")
            print(" PowerShell: $env:DB_URL = 'postgresql://username:password@localhost/database'")
            sys.exit(1)
            
        print(f"Retrieving player {args.player_id}...")
        player = get_player_by_id(args.player_id)
        
        if not player:
            print(f"\n Error: No player found with ID {args.player_id}")
            print("Tip: Use search_players.py to find valid player IDs")
            sys.exit(1)
            
        print(f"\nPlayer to delete: {player.player_name} ({player.team.abbreviation}, {player.season})")
        
        print("\nDeleting player and all associated game records...")
        print("(Using transaction to ensure data integrity...)")
        
        result = delete_player(args.player_id)
        
        if result:
            display_deletion_summary(result)
        else:
            print(f"\n Error: Deletion failed for player ID {args.player_id}")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n Database Error: {e}")
        print("Transaction was rolled back. No data was deleted.")
        print("Please check your database connection and try again.")
        sys.exit(1)
        
if __name__ == "__main__":
    main()
                        