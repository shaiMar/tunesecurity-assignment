#!/usr/bin/env python3
"""
Dou - A 2-Player Command Line Game

A simple turn-based game where two players take turns providing input,
and at the end, all inputs from each player are displayed.
"""

import os
import sys
from player import Player

class MenuOption:
    """Base class for menu options."""
    
    def __init__(self, name, description):
        self.name = name
        self.description = description
    
    def execute(self, game, player, player_index, turn_number):
        """Execute the option. Should be overridden by subclasses."""
        raise NotImplementedError("Subclasses must implement execute method")

class SkipTurnOption(MenuOption):
    """Option to skip the current turn."""
    
    def __init__(self):
        super().__init__("Skip Turn", "Skip this turn")
    
    def execute(self, game, player, player_index, turn_number):
        player.add_input("[SKIPPED]")
        return None  # Continue to next player

class CancelGameOption(MenuOption):
    """Option to cancel the game."""
    
    def __init__(self):
        super().__init__("Cancel Game", "Cancel game")
    
    def execute(self, game, player, player_index, turn_number):
        print(f"\n{player.name} cancelled the game.")
        input("Press Enter to see results...")
        game._display_results()
        return "cancel"

class ContinuePlayingOption(MenuOption):
    """Option to continue playing (return to turn)."""
    
    def __init__(self):
        super().__init__("Continue Playing", "Continue playing")
    
    def execute(self, game, player, player_index, turn_number):
        return game._player_turn(player, player_index, turn_number)

class DouGame:
    def __init__(self):
        self.players = []  # List to hold Player objects
        self.current_turn = 0
        self.total_turns = 0
        self.menu_options = {}  # Dictionary to hold menu options
    
    def _clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def _display_player_turn_screen(self, player, player_index, turn_number):
        """
        Display the player turn screen with current player, other players, and help info.
        
        Args:
            player (Player): The current player object
            player_index (int): Index of the player in the players list
            turn_number (int): Current turn number
        """
        # Clear screen for fresh display
        self._clear_screen()
        
        # Get all other players (non-current players)
        other_players = [p for i, p in enumerate(self.players) if i != player_index]
        
        # Get terminal width for positioning (default to 80 if can't determine)
        try:
            terminal_width = os.get_terminal_size().columns
        except:
            terminal_width = 80
        
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
    
    def init(self, player_names):
        """
        Initialize the players list with given player names.
        
        Args:
            player_names (list): List of player names to create Player objects
        """
        self.players = []
        for name in player_names:
            self.players.append(Player(name))
        
        # Initialize menu options
        self.menu_options = {
            '1': SkipTurnOption(),
            '2': ContinuePlayingOption()
        }
        
        # Clear any existing game state
        self.current_turn = 0
        self.total_turns = 0
    
    def start(self, *player_names, num_of_turns):
        """
        Entry point method to start the game.
        
        Args:
            *player_names: Variable number of player names
            num_of_turns (int): Total number of turns for the game (keyword argument)
        """
        # Validate minimum number of players
        if len(player_names) < 2:
            raise ValueError("Game requires at least 2 players")
        
        # Initialize players using the init function
        self.init(list(player_names))
        self.total_turns = num_of_turns
        
        print(f"\n🎮 Welcome to DOU! 🎮")
        
        # Display all players
        if len(self.players) == 2:
            print(f"Players: {self.players[0].name} vs {self.players[1].name}")
        else:
            player_list = ", ".join([player.name for player in self.players])
            print(f"Players: {player_list}")
        
        print(f"Total turns: {num_of_turns}")
        print("-" * 40)
        
        # Main game loopgit remote add origin
        for turn in range(1, num_of_turns + 1):
            self.current_turn = turn
            
            # Each player's turn
            for player_index, player in enumerate(self.players):
                self._player_turn(player, player_index, turn)
        
        # Display final results
        self._display_results()
    
    def _player_turn(self, player, player_index, turn_number):
        """
        Handle a single player's turn.
        
        Args:
            player (Player): The current player object
            player_index (int): Index of the player in the players list
            turn_number (int): Current turn number
        """
        # Display the player turn screen
        self._display_player_turn_screen(player, player_index, turn_number)
        
        # Wait for player input
        try:
            player_input = input(f"Enter your move: ").strip()
            
            # Handle special '?' input
            if player_input == '?':
                return self._handle_help_menu(player, player_index, turn_number)
            
            # Store the input in the player object
            player.add_input(player_input)
            
        except KeyboardInterrupt:
            print(f"\n\nGame interrupted by {player.name}!")
            self._display_results()
            return
        except EOFError:
            print(f"\n\nInput ended unexpectedly for {player.name}!")
            self._display_results()
            return
    
    def _handle_help_menu(self, player, player_index, turn_number):
        """
        Handle the help menu when player enters '?'.
        
        Args:
            player (Player): The current player object
            player_index (int): Index of the player in the players list
            turn_number (int): Current turn number
        
        Returns:
            None or calls _player_turn again based on user choice
        """
        self._clear_screen()
        
        print(f"{player.name} - Options Menu")
        print("=" * 30)
        
        # Display options dynamically from menu_options
        for key, option in self.menu_options.items():
            print(f"{key}. {option.description}")
        
        print("-" * 30)
        
        try:
            choice = input(f"Choose an option (1-{len(self.menu_options)}): ").strip()
            
            if choice in self.menu_options:
                # Execute the selected option
                return self.menu_options[choice].execute(self, player, player_index, turn_number)
            else:
                # Invalid choice - show menu again
                print(f"Invalid choice. Please select 1-{len(self.menu_options)}.")
                input("Press Enter to try again...")
                return self._handle_help_menu(player, player_index, turn_number)
                
        except (KeyboardInterrupt, EOFError):
            # If interrupted, continue with the turn
            return self._player_turn(player, player_index, turn_number)
    
    def _display_results(self):
        """Display the final results showing all inputs from each player."""
        # Clear screen for final results
        self._clear_screen()
        
        print("=" * 50)
        print("🏆 GAME RESULTS 🏆")
        print("=" * 50)
        
        # Find the highest score and winners
        highest_score = max(player.get_score() for player in self.players)
        winners = [player for player in self.players if player.get_score() == highest_score]
        
        # Display final scores
        print("\n🏆 FINAL SCORES 🏆")
        print("-" * 30)
        
        # Sort players by score (highest first)
        sorted_players = sorted(self.players, key=lambda p: p.get_score(), reverse=True)
        
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


def main():
    """Main function to demonstrate the game."""
    game = DouGame()
    
    # Example usage
    print("Starting DOU game demo...")
    game.start("Alice", "Bob", "Dalia", num_of_turns=3)


if __name__ == "__main__":
    main()
