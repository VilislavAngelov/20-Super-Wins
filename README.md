# 🎰 20 Super Wins - Slot Game Evolution

> Case Study of my First Slot Game as it Goes From a Terminal Version to a Polished GUI

## 📋 Overview

I know the best way to get better at something is by doing it. Hence I picked a fun and enjoyable project that is way above my current level of knowledge.
This case study documents the evolution of a slot machine game from a minimalist terminal-based prototype to a fully-featured graphical user interface (GUI) application. 
The project showcases my learning experience, demonstrates iterative development, UI/UX improvements, and feature expansion.

**Original Concept:** Terminal-based slot machine with 1 row and 3 reels

**Final Product:** GUI-based 20-line slot game with 5 reels and 3 rows

## Backlog
    [ ] Break the project into smaller tasks.
    [ ] Make the balance updates after each spin.
    [ ] Make the basic 1 line, 3 reel terminal version.
    [ ] Implement 3 rows, 5 reels and 20 win lines.
    [ ] Make the joker a wild card.
    [ ] Make the GUI.

## Stage 1 - Terminal 
    

I decided to first make the slot as straightforward as possible and then upgrade on it.
Broke the project into smaller tasks like:

    -How a slot machine works?
    -How to display the reels?
    -Check if you have enough money to spin?
    -How to deduct spin from balance?
    -How to add wins to balance etc?

And started tackling them one by one

You currently get $1000 to spin the machine.
Before you spin the program checks if you have enough balance to make a bet.
3 symbols get picked and put into the row using random.choice()
If the row has 3 of the same symbols you win a variable prize based on the symbols you get.
Prize gets added to balance and we wait for a new spin.
Each spin is initiated on a key press of any kind, meaning you can play using the spacebar.


![](https://github.com/VilislavAngelov/20-Super-Wins/blob/20-super-wins/assets/Terminal%20DEMO.gif)

### The current version accomplishes:

    [X] Break the project into smaller tasks.
    [X] Make the balance updates after each spin.
    [X] Make the basic 1 line, 3 reel terminal version.

### Next Version Should:

    [ ] Implement 3 rows, 5 reels and 20 win lines.
    [ ] Make the joker a wild card.