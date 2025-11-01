"""
Display module for the game.
Handles all terminal/console display operations.
"""

import os
from config import DEFAULT_TERMINAL_WIDTH


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def display_player_turn_screen(player, players, player_index, turn_number):
    """
    Display the player turn screen with current player, other players, and help info.
    
    Args:
        player (Player): The current player object
        players (list): List of all players
        player_index (int): Index of the player in the players list
        turn_number (int): Current turn number
    """
    # Clear screen for fresh display
    clear_screen()
    
    # Get all other players (non-current players)
    other_players = [p for i, p in enumerate(players) if i != player_index]
    
    # Get terminal width for positioning (use default from config if can't determine)
    try:
        terminal_width = os.get_terminal_size().columns
    except:
        terminal_width = DEFAULT_TERMINAL_WIDTH
    
    # Show current player's name on left, all other players with scores in brackets on right
    if len(other_players) == 1:
        other_players_text = f"[{other_players[0].name}:{other_players[0].get_score()}]"
    else:
        other_names_with_scores = ", ".join([f"{p.name}:{p.get_score()}" for p in other_players])
        other_players_text = f"[{other_names_with_scores}]"
    
    spaces_needed = terminal_width - len(player.name) - len(other_players_text)
    if spaces_needed < 1:
        spaces_needed = 1
    
    print(f"{player.name}{' ' * spaces_needed}{other_players_text}")
    print(f"Turn {turn_number}")
    print("-" * 20)
    
    # Add help line at bottom
    print(f"\n\n{' ' * (terminal_width - 20)}Type '?' for options")


def display_results(players):
    """
    Display the final results showing all inputs from each player.
    
    Args:
        players (list): List of all players
    """
    # Clear screen for final results
    clear_screen()
    
    print("=" * 50)
    print("🏆 GAME RESULTS 🏆")
    print("=" * 50)
    
    # Find the highest score and winners
    highest_score = max(player.get_score() for player in players)
    winners = [player for player in players if player.get_score() == highest_score]
    
    # Display final scores
    print("\n🏆 FINAL SCORES 🏆")
    print("-" * 30)
    
    # Sort players by score (highest first)
    sorted_players = sorted(players, key=lambda p: p.get_score(), reverse=True)
    
    for i, player in enumerate(sorted_players, 1):
        score = player.get_score()
        if player in winners:
            if len(winners) == 1:
                print(f"{i}. 🥇 {player.name}: {score} points ⭐ WINNER! ⭐")
            else:
                print(f"{i}. 🥇 {player.name}: {score} points ⭐ TIE WINNER! ⭐")
        else:
            print(f"{i}. {player.name}: {score} points")
    
    # Display winner announcement
    if len(winners) == 1:
        print(f"\n🎉 Congratulations {winners[0].name}! 🎉")
        print(f"You won with {highest_score} points!")
    elif len(winners) > 1:
        winner_names = " and ".join([w.name for w in winners])
        print(f"\n🎉 It's a tie! 🎉")
        print(f"Congratulations {winner_names}!")
        print(f"You all scored {highest_score} points!")
    
    print("\n" + "=" * 50)
    print("Thanks for playing DOU! 🎮")
    print("=" * 50)

