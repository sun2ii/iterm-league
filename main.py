import time
import os
import threading

# Constants
LANE_LENGTH = 40  # Length of the lane
RED_START = 0     # Starting position of the red minion
BLUE_START = LANE_LENGTH - 1  # Starting position of the blue minion
MOVE_INTERVAL = 1  # seconds

# ANSI color codes
RED = '\033[91m'
BLUE = '\033[94m'
ENDC = '\033[0m'

# Minion class to manage position and color
class Minion:
    def __init__(self, color, position):
        self.color = color
        self.position = position

    def __str__(self):
        return f"{self.color}●{ENDC}"

    def move(self, direction):
        self.position += direction

# Game class to manage the lane and minions
class Game:
    def __init__(self):
        self.lane = [' '] * LANE_LENGTH
        self.red_minion = Minion(RED, RED_START)
        self.blue_minion = Minion(BLUE, BLUE_START)
        self.lock = threading.Lock()

    def display(self):
        os.system('clear')
        self.lane = [' '] * LANE_LENGTH
        self.lane[self.red_minion.position] = str(self.red_minion)
        self.lane[self.blue_minion.position] = str(self.blue_minion)
        print("--" * LANE_LENGTH)
        print(' '.join(self.lane))
        print("--" * LANE_LENGTH)
        print('\nPress Ctrl+C to quit.')

    def move_minions(self):
        with self.lock:
            if self.red_minion.position < self.blue_minion.position - 1:
                self.red_minion.move(1)
                self.blue_minion.move(-1)

    def game_loop(self):
        while self.red_minion.position < self.blue_minion.position - 1:
            self.display()
            self.move_minions()
            time.sleep(MOVE_INTERVAL)
        self.display()
        print("The minions have met!")

if __name__ == "__main__":
    game = Game()

    # Run the game loop in a separate thread
    game_thread = threading.Thread(target=game.game_loop)
    game_thread.daemon = True
    game_thread.start()

    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nGame over!")
