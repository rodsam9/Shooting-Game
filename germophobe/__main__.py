# program entry point
from assets.director import Director
from assets import constants
from assets.actor import Actor
import random
import arcade
import math
import os

def main():
    director = Director()
    director.start_game()
    arcade.run()


if __name__ == "__main__":
    main()