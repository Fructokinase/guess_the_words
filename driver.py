import random
import string
import threading
import time

from words import Game

GAME_TIME_LIMIT = 240
GAME_TIMER_INTERVAL = 30
EXIT_CODE_GAME_TIMEOUT = 1

seconds_remaining = GAME_TIME_LIMIT
game_in_progress = False
print_lock = threading.Lock()


def timer(interval):

    global seconds_remaining
    global game_status

    while not game_in_progress:
        pass

    while seconds_remaining > 0 and game_in_progress:
        with print_lock:
            print("\n{} seconds remaining".format(seconds_remaining))
        time.sleep(interval)
        seconds_remaining -= interval
    print("time's up")



def start_game():

    global game_in_progress

    game = Game()
    game_exit_status = 0

    game_in_progress = True

    timer_thread = threading.Thread(target=timer, args=(GAME_TIMER_INTERVAL,))
    timer_thread.start()

    while not game.player_has_won():

        if seconds_remaining <= 0:
            game_exit_status = EXIT_CODE_GAME_TIMEOUT
            break

        with print_lock:
            print('\n' + '-' * 80)
            print('letters available: {}'.format(' '.join(list(game._letters))))
            print('-' * 80 + '\n')

        user_word = input("enter a word: ")

        if not game.tick(user_word):
            with print_lock:
                print("Invalid input")
            continue

        with print_lock:
            game.print()

    game_in_progress = False

    if game_exit_status == EXIST_CODE_GAME_TIMEOUT:
        print("Exited due to timeout")
        print("SOLUTION")
        game.reveal()
        game.print()

    print("DONE")


if __name__ == '__main__':

    start_game()
