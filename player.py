"""
Player module for Trivia game.
"""

class Player:
    """Represents a player in the Trivia game."""
    
    def __init__(self, name):
        """
        Initialize a player.
        
        Args:
            name (str): The player's name
        """
        self.name = name
        self.score = 0
        self.skips_used = 0
    

    
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

