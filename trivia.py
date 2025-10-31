#!/usr/bin/env python3
"""
Dou - A 2-Player Command Line Game

A simple turn-based game where two players take turns providing input,
and at the end, all inputs from each player are displayed.
"""

import os
import sys
from player import Player
from display import clear_screen, display_player_turn_screen, display_results

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
        display_results(game.players)
        return "cancel"

class ContinuePlayingOption(MenuOption):
    """Option to continue playing (return to turn)."""
    
    def __init__(self):
        super().__init__("Continue Playing", "Continue playing")
    
    def execute(self, game, player, player_index, turn_number):
        return game._player_turn(player, player_index, turn_number)

class TurnBaseGame:
    def __init__(self):
        self.players = []  # List to hold Player objects
        self.current_turn = 0
        self.total_turns = 0
        self.menu_options = {}  # Dictionary to hold menu options
    
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
        display_results(self.players)
    
    def _player_turn(self, player, player_index, turn_number):
        """
        Handle a single player's turn.
        
        Args:
            player (Player): The current player object
            player_index (int): Index of the player in the players list
            turn_number (int): Current turn number
        """
        # Display the player turn screen
        display_player_turn_screen(player, self.players, player_index, turn_number)
        
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
            display_results(self.players)
            return
        except EOFError:
            print(f"\n\nInput ended unexpectedly for {player.name}!")
            display_results(self.players)
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
        clear_screen()
        
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


def main():
    """Main function to demonstrate the game."""
    game = TurnBaseGame()
    
    # Example usage
    print("Starting DOU game demo...")
    game.start("Alice", "Bob", "Dalia", num_of_turns=3)


if __name__ == "__main__":
    main()
