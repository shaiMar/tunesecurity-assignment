"""
Player module for Dou game.
"""

class Player:
    """Represents a player in the DOU game."""
    
    def __init__(self, name):
        """
        Initialize a player.
        
        Args:
            name (str): The player's name
        """
        self.name = name
        self.inputs = []
        self.score = 0
        self.skips_used = 0
    
    def add_input(self, player_input):
        """
        Add an input to the player's list of inputs and update score.
        
        Args:
            player_input (str): The input entered by the player
        """
        self.inputs.append(player_input)
        self._update_score(player_input)
    
    def _update_score(self, player_input):
        """
        Update the player's score based on the input.
        Score is the count of 'n', 'm', and 'v' characters (case insensitive).
        
        Args:
            player_input (str): The input to analyze for scoring
        """
        if player_input != "[SKIPPED]":  # Don't count skipped turns
            score_chars = player_input.lower().count('n') + \
                         player_input.lower().count('m') + \
                         player_input.lower().count('v')
            self.score += score_chars
    
    def get_inputs(self):
        """
        Get all inputs from this player.
        
        Returns:
            list: List of all inputs from this player
        """
        return self.inputs
    
    def clear_inputs(self):
        """Clear all inputs and reset score for this player."""
        self.inputs = []
        self.score = 0
        self.skips_used = 0
    
    def get_score(self):
        """
        Get the player's current score.
        
        Returns:
            int: The player's current score
        """
        return self.score
    
    def get_skips_remaining(self, max_skips):
        """
        Get the number of skips remaining for this player.
        
        Args:
            max_skips (int): Maximum number of skips allowed (from game rules)
        
        Returns:
            int: Number of skips remaining
        """
        return max_skips - self.skips_used
    
    def skip_turn(self):
        """
        Mark that the player used a skip.
        Increments the skips_used counter.
        """
        self.skips_used += 1
    
    def __str__(self):
        """String representation of the player."""
        return self.name

