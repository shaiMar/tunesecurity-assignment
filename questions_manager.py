import random
from typing import Dict, List, Optional


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
        self.all_questions = questions_data
        self.questions_by_category: Dict[str, List[dict]] = {}
        for question in questions_data:
            category = question.get('category')
            if category not in self.questions_by_category:
                self.questions_by_category[category] = []
            self.questions_by_category[category].append(question)

        self.category_question_counts = { # This is to hold the count of available questions per category - in case it's 0 - it will be removed
            category: len(questions) for category, questions in self.questions_by_category.items()
        }
        # Also keep track of total questions
        self.total_available_questions = len(questions_data)

    def get_next_question(self, category: str = None) -> Optional[dict]:
        """
        Get the next question from the available category questions.
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
        if self.total_available_questions == 0:
            print("No questions available.")
            return None
        if category and category not in self.category_question_counts:
            print(f"No questions available for the '{category}' category.")
            return None



        category_question_list = []
        if not category:
            # If no category specified, pick a random category
            category = random.choice(list(self.category_question_counts.keys()))

        available_questions_count = self.category_question_counts[category]
        category_question_list = self.questions_by_category[category]

        # Generate random index in the range of available questions
        random_index = random.randint(0, available_questions_count - 1)

        # Get the selected question
        selected_question = category_question_list[random_index]

        # Swap the selected question with the last available question
        last_index = available_questions_count - 1
        category_question_list[random_index], category_question_list[last_index] = \
            category_question_list[last_index], category_question_list[random_index]

        # Decrement the available questions count
        self.category_question_counts[category] -= 1
        self.total_available_questions -= 1
        if self.category_question_counts[category] == 0:
            del self.category_question_counts[category]

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

    def get_categories(self):
        """
        Get the list of available categories with at least one question.

        Returns:
            List[str]: List of category names
        """
        return list(self.category_question_counts.keys())

