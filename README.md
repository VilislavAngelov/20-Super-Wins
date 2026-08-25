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

## Stage 2 - 20 Lines Terminal 
    

The initial version was very simple and not really fun. So I wanted to introduce 20 pay lines, wilds, scatter symbols and fix the RTP between 94% and 98%.


![](https://github.com/VilislavAngelov/20-Super-Wins/blob/20-super-wins/assets/20%20lines%20DEMO.gif)

### The current version accomplishes:

    [X] 20 Pay lines across 5 reels and 3 rows.
    [X] Joker is a wild symbol.
    [X] There is now a scatter symbol what pays cash when it lines on reels 1, 3 and 5.
    [X] RTP tested between 94% and 98%
    [X] Written tests to make sure line combination pay the right amount by using Hypothesis

    ### Next Version Should:

    [ ] Web interface.
    [ ] FastAPI integration.

## Stage 3 - First Web Version 
    

Decided it's time to get the web version going


![](https://github.com/VilislavAngelov/20-Super-Wins/blob/20-super-wins/assets/WEB%20DEMO.gif)

### The current version accomplishes:

    [X] Basic web interface
    [X] FastAPI integration

    ### Next Version Should:

    [ ] Server side balance.
    [ ] Properly aligned layout.
    [ ] Animations.
    [ ] Bet amount display.
    [ ] Styled components.
    [ ] Be able to spin with spacebar.

## Stage 4 - Sessions, Real API and Animations 
    

The web version worked but the balance was a single global variable, so every player shared the same money. That had to go first. I gave each player a unique id in a cookie and moved the balance, the bet size and the last screen into a server side session, so now your money is yours and it survives a refresh.

After that I cleaned up the API. GET /state paints your balance and last win on page load, POST /bet validates the bet against the allowed sizes instead of trusting whatever the browser sends, and the status codes actually mean something now, 402 when you can't afford the spin and 401 when there is no session. /spin became a POST too, because a GET is supposed to be safe and mine was taking money, which meant you could spin by pasting the url or by the browser prefetching it.

Then came the part that took the longest, making it feel like a slot machine. I threw away the one shot CSS transition and switched to keyframe animations, one that loops forever and one that lands. The reels now spin until the server answers instead of waiting for it, and each reel is 3 tiles longer than the one before it so they all start together at the same speed but stop one after the other. The distance and the duration both come from the same CSS variable so they can't drift apart. Sounds play on animationend now so they can't desync from the animation, the win counter ticks up after the reels stop instead of spoiling the result, and the spin button has three states so you can't spam it.


![](https://github.com/VilislavAngelov/20-Super-Wins/blob/20-super-wins/assets/STAGE%204.gif)

### The current version accomplishes:

    [X] Unique player id in a cookie with a server side session.
    [X] Balance, bet size and last screen stored per player.
    [X] GET /state, POST /bet and POST /spin with proper status codes.
    [X] Bet size validated on the server instead of trusting the browser.
    [X] Last screen saved and rendered into the page on load so there is no blank flash.
    [X] Reels loop until the server responds instead of waiting for it.
    [X] Reels start together and land one at a time.
    [X] Landing sounds fired by the animation itself, no timers.
    [X] Winnings count up after the reels stop.
    [X] Idle, waiting and spinning states with a spin and a stop button.

### Next Version Should:

    [ ] Stop the reels instantly with the Web Animations API instead of waiting for a wrap point.
    [ ] Keep the reels stopping in order when you hit stop early.
    [ ] Rate limit /spin on the server so it can't be spammed.
    [ ] Move the sessions out of a dict and into a database.
    [ ] Refactor into classes.
    [ ] Be able to spin with spacebar.
