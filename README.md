# crypo_puzzle.py

A traditional cryptogram puzzle game.
```
Created mapping R = M


Mapped letters
  EGH   PR  WY
  ZYC   WM  LP


H_W T_ PL_Y _ CRYPT_GR_M P_ZZL_
BUP IU YWCG C HJGYIUDJCR YOEEWQ


Letter or exit?
```

## What?

A Cryptogram game using a simple substitution cipher.

You can use a custom file or phrase.

```bash
usage: crypto_puzzle.py [-h] [-f FILE] [-p PHRASE [PHRASE ...]] [-r] [--debug]

A Cryptogram game using a simple substitution cipher.

optional arguments:
    -h, --help
            show this help message and exit
    -f FILE, --file FILE
            File to use
            Overrides phrase
    -p PHRASE [PHRASE ...], --phrase PHRASE [PHRASE ...]
            Word or phrase to use
    -r, --how-to-play
            See how to play
    --debug
            Debug the program
            Default: False
```

## Why?
I used to love this puzzles as a kid and since creating hangman, realised that it wouldn't be that dissimilar to hangman and easy to create from the code.

## Improvements?
Allow the user to solve, as opposed to automatic solving.  Optional statistics like letter frequency or pattern search

## State?
No known bugs.  Works to the best of my knowledge.