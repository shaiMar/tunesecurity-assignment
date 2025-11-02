import random


class QuestionsManager:
    """
    Class to manage trivia questions loaded from a JSON file.
    """
    def __init__(self, questions_data):
        """
        Initialize the QuestionsManager with a list of question dictionaries.
        
        Args:
            questions_data: List of question dictionaries from JSON
        """
        self.questions = questions_data
        self.available_questions_count = len(questions_data)
    
    def get_next_question(self):
        """
        Get the next question from the available questions.
        Randomly selects a question and swaps it with the last available question
        to avoid asking the same question twice.
        
        Also scrambles all answers (right + wrong) into a single 'answers' list
        and provides the correct answer index.
        
        Returns:
            dict: A question dictionary with keys:
                  - 'question': The question text
                  - 'answers': List of all answers in random order
                  - 'correct_answer_index': Index of the correct answer in the answers list
                  - 'category': Question category
                  - 'difficulty': Question difficulty
            None: If no questions are available
        """
        if self.available_questions_count == 0:
            return None
        
        # Generate random index in the range of available questions
        random_index = random.randint(0, self.available_questions_count - 1)
        
        # Get the selected question
        selected_question = self.questions[random_index]
        
        # Swap the selected question with the last available question
        last_index = self.available_questions_count - 1
        self.questions[random_index], self.questions[last_index] = \
            self.questions[last_index], self.questions[random_index]
        
        # Decrement the available questions count
        self.available_questions_count -= 1
        
        # Scramble the answers
        # First, shuffle only the wrong answers
        wrong_answers = selected_question['wrong_answers'].copy()
        random.shuffle(wrong_answers)
        
        # Generate a random index (0-3) to insert the correct answer
        correct_answer_index = random.randint(0, len(wrong_answers))
        
        # Insert the correct answer at the random position
        all_answers = wrong_answers[:correct_answer_index] + \
                      [selected_question['right_answer']] + \
                      wrong_answers[correct_answer_index:]
        
        # Create a new question dict with scrambled answers
        scrambled_question = {
            'question': selected_question['question'],
            'answers': all_answers,
            'correct_answer_index': correct_answer_index,
            'category': selected_question['category'],
            'difficulty': selected_question['difficulty']
        }
        
        # Return the scrambled question
        return scrambled_question

