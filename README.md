Minesweeper CLI Game
====================

This repository holds a command line version of Minesweeper in some state of (un)completion. 
I've decided that making everything here less horrible is enough of a project that 
I would like to keep track of it here. 
The code will be committed as it currently lives on my disk and we'll see how far I get
before I hate myself too much to continue.
I'll include a brief to-do list here since it seems overkill to raise issues.

Cleanup:
--------

- [x] Commit everything
- [x] Put in good comments
- [x] Take out bad comments
- [x] Read PEP8 again and everything in this repository
- [x] Try not to cry 
- [ ] Stop using debug.py to test things and write a real goddamn test suite
- [ ] Refactor communication between "twoms" module and runner/debug (also rewrite entire 'play' method
- [ ] Rename pretty much everything

Features:
---------

- [x] Refactor I/O to importing classes (minesweeper module)
- [ ] Finish games that are a tossup
- [ ] Implement patter matching for common patterns (1-2-1, 1-1, 1-2)
- [ ] Variable board size, number of mines and number of runs for runner
- [ ] Silent mode
- [ ] Keep stats
- [ ] Optomize clearing strategy
- [ ] Optomize guessing strategy
- [ ] Add more dimensions
