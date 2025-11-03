
from display import display_playing_player_bar, clear_screen, display_and_get_category_choice, display_game_over, \
    display_question_and_get_answer
from player import Players
from questions_manager import QuestionsManager



class Trivia():
    def __init__(self,players: Players, questions: QuestionsManager):
        self.questions = questions
        self.players: Players = players

    def run(self):
        print(f"\nWelcome to Trivia!")

        turn_index = 0
        player = None
        question = None
        get_new_player = True
        get_new_question = True
        while self.questions.total_available_questions>0:
            clear_screen()
            if get_new_player and get_new_question:
                turn_index += 1
                player_index = (turn_index-1) % self.players.get_player_count()
            else:
                player_index = None

            if get_new_player:
                player = self.players.get_next_player(player_index)

            display_playing_player_bar(self.players, current_player_index=player.idx)
            print(f"\nTurn {turn_index} for player-{player.name}:\n")

            if get_new_question:
                category = display_and_get_category_choice(self.questions.get_categories())
                display_playing_player_bar(self.players, current_player_index=player.idx)
                question = self.questions.get_next_question(category)
                if not question:
                    print("No more questions available. Ending game.")
                    return
            player.update_last_question(question['question'])
            print(f"\nTurn {turn_index} for player-{player.name}:\n")
            answer = display_question_and_get_answer(player, question)

            if answer=='end':
                print(f"{player.name} ended the game.")
                break
            if answer=='skip':
                if player.get_skips_remaining()>0:
                    player.skip_turn()
                    print(f"{player.name} skipped the question. Skips remaining: {player.get_skips_remaining()}")
                    get_new_player = False
                    get_new_question = True
                else:
                    print(f"{player.name} has no skips remaining. Please answer the question.")
                    get_new_player = False
                    get_new_question = False
                continue

            if answer == question['correct_answer_index']:
                score = question['difficulty'] * 10
                player.score += score
                print(f"Correct! {player.name} won {score} points.")
                get_new_player = True
                get_new_question = True
            else:
                next_player = self.players.who_is_the_next_player()
                if next_player.get_last_question() == question['question']:
                    print(f"Incorrect! No more players left to answer this question.")
                    get_new_player = True
                    get_new_question = True
                else:
                    print(f"Incorrect! moving question to next player.")
                    get_new_player = True
                    get_new_question = False
            continue


        display_game_over(self.players)








def start(player_names, questions:QuestionsManager):

    # Validate minimum number of players
    if len(player_names) < 2:
        raise ValueError("Game requires at least 2 players")


    trivia = Trivia(Players(player_names), questions)
    trivia.run()



