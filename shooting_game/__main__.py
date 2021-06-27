# program entry point
from assets.director import Director
from assets import constants
from assets.actor import Actor
import random
import arcade
import math
import os

def main():

    cast = {}

    player_sprite = Actor()
    cast["player_sprite"] = [player_sprite]

    cast["enemys"] = []

    for i in range(constants.ENEMY_COUNT):
        pass

    cast["bullet"] = []

    script = {}

    # start the game
    director = Director(cast, script)
    actor.setup()
    arcade.run()


if __name__ == "__main__":
    main()