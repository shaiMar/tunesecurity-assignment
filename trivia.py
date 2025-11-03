#!/usr/bin/env python3


import os
import sys
from player import Player
from display import clear_screen, display_player_turn_screen, display_results
from config import DEFAULT_MAX_SKIPS, DEFAULT_NUM_TURNS

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
        # Check if player can skip
        if player.get_skips_remaining(game.max_skips) <= 0:
            print(f"\nYou have no skips remaining!")
            input("Press Enter to continue...")
            return game._player_turn(player, player_index, turn_number)
        
        # Use skip
        player.skip_turn()
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

class TriviaGame:
    """Trivia game with question asking functionality."""
    
    def __init__(self, questions_manager):
        """
        Initialize the trivia game with a questions manager.
        
        Args:
            questions_manager (QuestionsManager): Manager for handling trivia questions
        """
        self.questions_manager = questions_manager
        self.players = []  # List to hold Player objects
        self.current_turn = 0
        self.total_turns = 0
        self.max_skips = 0  # Maximum skips allowed per player
        self.menu_options = {}  # Dictionary to hold menu options
    
    def init(self, player_names, max_skips=None):
        """
        Initialize the players list with given player names.
        
        Args:
            player_names (list): List of player names to create Player objects
            max_skips (int): Maximum number of skips per player (default: from config)
        """
        if max_skips is None:
            max_skips = DEFAULT_MAX_SKIPS
        
        self.max_skips = max_skips
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
    
    def start(self, *player_names, num_of_turns=None, max_skips=None):
        """
        Entry point method to start the game.
        
        Args:
            *player_names: Variable number of player names
            num_of_turns (int): Total number of turns for the game (default: from config)
            max_skips (int): Maximum number of skips per player (default: from config)
        """
        if num_of_turns is None:
            num_of_turns = DEFAULT_NUM_TURNS
        if max_skips is None:
            max_skips = DEFAULT_MAX_SKIPS
        # Validate minimum number of players
        if len(player_names) < 2:
            raise ValueError("Game requires at least 2 players")
        
        # Initialize players using the init function
        self.init(list(player_names), max_skips=max_skips)
        self.total_turns = num_of_turns
        
        print(f"\nWelcome to Trivia!")
        
        # Display all players
        if len(self.players) == 2:
            print(f"Players: {self.players[0].name} vs {self.players[1].name}")
        else:
            player_list = ", ".join([player.name for player in self.players])
            print(f"Players: {player_list}")
        
        print(f"Total turns: {num_of_turns}")
        print("-" * 40)
        
        # Main game loop
        for turn in range(1, num_of_turns + 1):
            self.current_turn = turn
            
            # Each player's turn
            for player_index, player in enumerate(self.players):
                self._player_turn(player, player_index, turn)
        
        # Display final results
        display_results(self.players)
    
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
            # Add skip count for Skip Turn option
            if isinstance(option, SkipTurnOption):
                skips_remaining = player.get_skips_remaining(self.max_skips)
                print(f"{key}. {option.description} ({skips_remaining} left)")
            else:
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
    
    def _player_turn(self, player, player_index, turn_number):
        """
        Handle a single player's turn with trivia questions.
        
        Args:
            player (Player): The current player object
            player_index (int): Index of the player in the players list
            turn_number (int): Current turn number
        """
        # Display the player turn screen
        display_player_turn_screen(player, self.players, player_index, turn_number)
        
        # Get next question from the questions manager
        question_data = self.questions_manager.get_next_question()

        if question_data is None:
            print("\nNo more questions available!")
            input("Press Enter to continue...")
            return
        
        # Display the question
        print(f"\nCategory: {question_data['category'].upper()}")
        print(f"Difficulty: {'*' * question_data['difficulty']}")
        print(f"\n{question_data['question']}")
        print("\n" + "-" * 40)
        
        # Display the answers
        for i, answer in enumerate(question_data['answers'], 1):
            print(f"{i}. {answer}")
        
        print("-" * 40)
        
        # Wait for player input
        try:
            player_input = input(f"Your answer (1-{len(question_data['answers'])}) or '?' for options: ").strip()
            
            # Handle special '?' input
            if player_input == '?':
                return self._handle_help_menu(player, player_index, turn_number)
            
            # Validate and check answer
            try:
                answer_num = int(player_input)
                if 1 <= answer_num <= len(question_data['answers']):
                    # Check if correct
                    if answer_num - 1 == question_data['correct_answer_index']:
                        print(f"\nCorrect! Well done {player.name}!")
                        player.score += question_data['difficulty']*10  # Award points for correct answer according to difficulty
                    else:
                        correct_answer = question_data['answers'][question_data['correct_answer_index']]
                        print(f"\nIncorrect! The correct answer was: {correct_answer}")

                    input("\nPress Enter to continue...")
                else:
                    print(f"\nInvalid answer! Please select 1-{len(question_data['answers'])}")
                    input("Press Enter to try pass the question to the next player...")
                    return self._player_turn(player, player_index, turn_number)

            except ValueError:
                print(f"\nInvalid input! Please enter a number 1-{len(question_data['answers'])}")
                input("Press Enter to try again...")
                return self._player_turn(player, player_index, turn_number)

        except KeyboardInterrupt:
            print(f"\n\nGame interrupted by {player.name}!")
            display_results(self.players)
            return
        except EOFError:
            print(f"\n\nInput ended unexpectedly for {player.name}!")
            display_results(self.players)
            return


def start(*player_names, num_of_turns=None, questions=None, max_skips=None):
    """
    Convenience function to start a trivia game.
    
    Args:
        *player_names: Variable number of player names
        num_of_turns (int): Total number of turns for the game (default: from config)
        questions (QuestionsManager): Questions manager instance
        max_skips (int): Maximum number of skips per player (default: from config)
    
    Returns:
        TriviaGame: The game instance (can be used for testing)
    """
    if questions is None:
        raise ValueError("Questions manager is required to start the game")
    
    if num_of_turns is None:
        num_of_turns = DEFAULT_NUM_TURNS
    if max_skips is None:
        max_skips = DEFAULT_MAX_SKIPS
    
    # Create and start the trivia game
    game = TriviaGame(questions)
    game.start(*player_names, num_of_turns=num_of_turns, max_skips=max_skips)
    
    return game


def main():
    """Main function to demonstrate the game."""
    from questions_manager import QuestionsManager
    
    # Example usage - would need actual questions in a real scenario
    print("Starting Trivia game demo...")
    print("Note: This demo requires a questions.json file to run.")
    
    # Example of how to use it:
    # questions_data = [...] # Load from JSON
    # questions_manager = QuestionsManager(questions_data)
    # game = TriviaGame(questions_manager)
    # game.start("Alice", "Bob", "Dalia", num_of_turns=3)


if __name__ == "__main__":
    main()
