from time import sleep
from assets import constants
import random
import arcade
import math
import os

class Director:
    
    def __init__(self, cast, script):
        """ Initializer """
        # Call the parent class initializer
        super().__init__()#(#SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
  
        self._cast = cast
        self._script = script
        
    def start_game(self):
        """Starts the game loop to control the sequence of play."""
        while True:
            self._cue_action("input")
            self._cue_action("update")
            self._cue_action("output")
            sleep(constants.FRAME_LENGTH)

    def _cue_action(self, tag):
        """Executes the actions with the given tag.
        
        Args:
            tag (string): The given tag.
        """ 
        for action in self._script[tag]:
            action.execute(self._cast)

        # Variables that will hold sprite lists
            self.player_list = None
            self.enemy_list = None
            self.bullet_list = None

            # Set up the player info
            self.player_sprite = None
            self.score = 0
            self.score_text = None