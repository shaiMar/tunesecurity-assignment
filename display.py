import os

from config import DEFAULT_TERMINAL_WIDTH
from player import Players





def display_playing_player_bar(players: Players, current_player_index, terminal_width=DEFAULT_TERMINAL_WIDTH):
    """
    Display a horizontal bar showing all players with the current player highlighted.

    Args:
        players : List of player names
        current_player_index (int): Index of the current player in the players list
        terminal_width (int): Width of the terminal for formatting
    """
    bar_elements = []
    for player in players:
        if player.idx == current_player_index:
            bar_elements.append(f"next playing:{player.name}({player.score})\t\t\t\t")  # Highlight current player
        else:
            bar_elements.append(f"{player.name}({player.score})")

    bar = "   ".join(bar_elements)
    print("\n" + "=" * terminal_width)
    print(f"{bar}")
    print("=" * terminal_width + "\n")


def clear_screen():
    if os.name == 'posix' and 'TERM' in os.environ:
        os.system('clear')
    elif os.name != 'posix':
        os.system('cls')



def display_and_get_category_choice(categories: list) -> str | None:
    """
    Display available categories and get user's choice.

    Args:
        categories (list): List of available
    Returns:
        str: Chosen category
    """
    print("Available Categories:")
    for idx, category in enumerate(categories, start=1):
        print(f"{idx}. {category}")

    while True:
        choice = input("Select a category by number (or press Enter for random): ").strip()
        if choice == "":
            clear_screen()
            return None  # Random category
        if choice.isdigit():
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(categories):
                clear_screen()
                return categories[choice_idx]
        print("Invalid choice. Please try again.")

def display_question_and_get_answer(player, question):
    """Display the question and get the player's answer."""

    print(f"Difficulty: {question['difficulty']} | Category: {question['category']}\n")
    print(question['question'])
    for idx, answer in enumerate(question['answers'], start=1):
        print(f"{idx}. {answer}")

    print ("\nType the number of your answer or 'skip' to skip this question. 'end' to end the game.")
    while True:
        answer = input("Your answer (number): ").strip()
        if answer.isdigit():
            answer_idx = int(answer) - 1
            if 0 <= answer_idx < len(question['answers']):
                return answer_idx
            else:
                print("Invalid answer. Please try again.")
        else:
            if answer.lower() == 'skip' or answer.lower() == 'end':
                return answer.lower()
            else:
                print("Invalid answer. Please try again.")


        print("Invalid choice. Please try again.")


def display_game_over(players):
    """Display the game over screen with final scores and winner."""
    print("\n" + "=" * DEFAULT_TERMINAL_WIDTH)
    print("GAME OVER!")
    print("=" * DEFAULT_TERMINAL_WIDTH)
    print("\nFinal Scores:")

    # Display all players and their scores
    for player in players:
        print(f"{player.name}: {player.score} points")

    # Find the winner(s)
    max_score = max(player.score for player in players)
    winners = [player for player in players if player.score == max_score]

    print("\n" + "=" * DEFAULT_TERMINAL_WIDTH)
    if len(winners) > 1:
        winner_names = ", ".join(player.name for player in winners)
        print(f"It's a TIE between: {winner_names}!")
    else:
        print(f"🎉 {winners[0].name} WINS! 🎉")
    print("=" * 80 + "\n")