#!/usr/bin/env python3

"""
Script:	hangman.py
Date:	2020-04-27

Platform: MacOS/Windows/Linux

Description:
A Cryptogram game using a simple substitution cipher.
"""
__author__ = 'thedzy'
__copyright__ = 'Copyright 2020, thedzy'
__license__ = 'GPL'
__version__ = '1.0'
__maintainer__ = 'thedzy'
__email__ = 'thedzy@hotmail.com'
__status__ = 'Developer'

import argparse
import random
import os

# TODO: empty space count

def main():
    latin_chars = list('abcdefghijklmnopqrstuvwxyz')

    if options.file is None:
        puzzle_phrase = ' '.join(options.phrase).lower()
    else:
        puzzle_phrase = options.file.read().replace('\n', ' ').lower()
        options.file.close()

    puzzle_length = len(puzzle_phrase)
    # Get the puzzle characters instead of assuming a latin based character set
    puzzle_chars = []
    for char in puzzle_phrase:
        if char.isalnum():
            if char not in puzzle_chars:
                puzzle_chars.append(char)
                if char in latin_chars:
                    latin_chars.remove(char)

    puzzle_chars.sort()
    puzzle_chars_ordered = puzzle_chars
    # Append, randomise and trim so that we always have a list equal to the character set used
    puzzle_chars_unordered = puzzle_chars + latin_chars
    puzzle_chars = puzzle_chars_unordered
    random.shuffle(puzzle_chars_unordered)

    # Trim to match characters in puzzle
    puzzle_chars_unordered = puzzle_chars_unordered[:len(puzzle_chars_ordered)]

    # Create a character map
    puzzle_chars_map = str.maketrans(''.join(puzzle_chars_ordered), ''.join(puzzle_chars_unordered))
    puzzle_reordered = puzzle_phrase.translate(puzzle_chars_map)

    # Sort for displaying the key mappings
    puzzle_chars.sort()

    guesses = {}
    set_cursor()
    while True:
        if options.debug:
            print('Character map:')
            print('Represented: ', ' '.join(puzzle_chars_unordered).upper())
            print('Actual:      ', ' '.join(puzzle_chars_ordered).upper())
            print()

        set_cursor(5, 0, False)

        print('Mapped letters')
        for character in puzzle_chars:
            if character in guesses:
                print(character.upper(), end='')
            else:
                print(' ', end='')
        print()
        for character in puzzle_chars:
            try:
                print(guesses[character].upper(), end='')
            except KeyError:
                print(' ', end='')
        print('\n\n')

        window_width, _ = os.get_terminal_size()
        answer = ''

        # Wrap to window for puzzles longer than screen size, breaking lines at spaces
        remaining = len(puzzle_phrase)
        first_position = 0
        last_position = window_width
        empty_positions = 0
        while True:
            sample = puzzle_phrase[first_position:last_position]

            if remaining > window_width:
                last_position = first_position + sample.rfind(' ')
            line = puzzle_phrase[first_position:last_position]

            for char in puzzle_reordered[first_position:last_position].lstrip():
                if char.isalnum():
                    if char in guesses:
                        print(guesses[char].upper(), end='')
                        answer += guesses[char]

                    else:
                        print('_', end='')
                        answer += '_'
                        empty_positions += 1
                else:
                    print(char, end='')
                    answer += char

            print()
            # Draw puzzle
            print(puzzle_reordered[first_position:last_position].lstrip().upper())
            print()
            # If debugging, draw answer
            if options.debug:
                print(puzzle_phrase[first_position:last_position].lstrip())
                print()

            first_position = last_position
            last_position = last_position + window_width

            remaining = remaining - len(line)
            if remaining <= 0:
                break

        if answer.replace(' ', '') == puzzle_phrase.replace(' ', ''):
            print('You cracked the code')
            exit()

        # Print remaining spaces
        print('-' * 30)
        print('{:5d} space(s) remain unfilled'.format(empty_positions))
        print('-' * 30)

        # Get guess
        guess_key = input('\nLetter or exit? ')
        if guess_key.lower() == 'exit':
            exit()

        if len(guess_key) == 0:
            continue
        if len(guess_key) == 2:
            guess_value = guess_key[1]
        else:
            guess_value = input('\n{} is actually? '.format(guess_key[0].upper()))

        if len(guess_key) > 0:
            guess_key = guess_key[0].lower()
        else:
            set_cursor()
            continue
        if len(guess_value) > 0:
            guess_value = guess_value[0].lower()
        else:
            set_cursor()
            if guess_key in guesses.keys():
                del guesses[guess_key]
                print('Removed mapping', guess_key.upper())
            continue

        set_cursor()
        if guess_key.isalnum() and guess_value.isalnum():
            # If value is in dictionary remove it
            if guess_value in guesses.values():
                for key, value in dict(guesses).items():
                    if key != guess_key:
                        if value == guess_value:
                            del guesses[key]
                            print('Removed mapping', key.upper(), '=', guess_value.upper())

            # Add/edit dictionary
            if guess_key in guesses.keys():
                print('Remapping', guess_key.upper(), '=', guess_value.upper())
            else:
                print('Created mapping', guess_key.upper(), '=', guess_value.upper())
            guesses[guess_key] = guess_value


def set_cursor(y_position=0, x_position=0, reset=True):
    """
    Set the terminal/console cursor position and whether to clear the screen
    :param y_position: (int) Row
    :param x_position: (int) Column
    :param reset: (bool) Clear the screen
    :return: (void)
    """
    if os.name is not 'nt':
        # Send an ansi clear
        if reset:
            print('\033[2J')
        # Set the cursor
        print('\033[{:d};{:d}H'.format(y_position, x_position))


def how_to_play():
    print('Cryptograms are text that have been encrypted using a simple substitution cipher.\n')
    print('At the top is the last change and all the characters you currently have a designated replacement for (map)\n'
          'Example:\n'
          '╒═════════════════════════════════════╕\n'
          '│ Removed mapping K = I               │\n'
          '│ Created mapping Z = I               │\n'
          '│                                     │\n'
          '│ Mapped letters                      │\n'
          '│   EGH   PR  WY                      │\n'
          '│   ZYC   WM  LP                      │\n'
          '╘═════════════════════════════════════╛')
    print('Below is the puzzle\n'
          'Example:\n'
          '╒═════════════════════════════════════╕\n'
          '│ H_W T_ PL_Y _ CRYPT_GR_M P_ZZL_.    │\n'
          '│ BUP IU YWCG C HJGYIUDJCR YOEEWQ.    │\n'
          '│                                     │\n'
          '│ Letter or exit?                     │\n'
          '│                                     │\n'
          '╘═════════════════════════════════════╛')
    print('And below is the input\n'
          'Example:\n'
          '╒═════════════════════════════════════╕\n'
          '│ Letter or exit? s                   │\n'
          '│                                     │\n'
          '│ S is actually? a                    │\n'
          '│                                     │\n'
          '╘═════════════════════════════════════╛')
    print('You can enter in one letter and then the replacement, or enter a two letter combo. ex: sa, sets S as A')
    print('To remove a mapping, enter the letter but enter nothing on the next prompt')

    print('Type \'exit\' to quit\n')

    print('Puzzle will automatically solve when all characters are correct')


if __name__ == '__main__':

    def parser_formatter(format_class, **kwargs):
        """
        Use a raw parser to use line breaks, etc
        :param format_class: (class) formatting class
        :param kwargs: (dict) kwargs for class
        :return: (class) formatting class
        """
        try:
            return lambda prog: format_class(prog, **kwargs)
        except TypeError:
            return format_class

    parser = argparse.ArgumentParser(description='A Cryptogram game using a simple substitution cipher.',
                                     formatter_class=parser_formatter(
                                         argparse.RawTextHelpFormatter,
                                         indent_increment=4, max_help_position=12, width=160))

    parser.add_argument('-f', '--file', type=argparse.FileType('r'),
                        action='store', dest='file', default=None,
                        help='File to use'
                             '\nOverrides phrase')

    parser.add_argument('-p', '--phrase', type=str,
                        action='store', dest='phrase', default=[], nargs='+',
                        help='Word or phrase to use')

    parser.add_argument('-r', '--how-to-play',
                        action='store_true', dest='how', default=False,
                        help='See how to play')

    # Testing and debugging
    parser.add_argument('--debug',
                        action='store_true', dest='debug', default=False,
                        help='Debug the program'
                             '\nDefault: %(default)s')

    options = parser.parse_args()

    if options.how:
        how_to_play()
    else:
        if options.file or options.phrase:
            main()
        else:
            parser.print_help()
