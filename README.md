# 🎰 20 Super Wins - Slot Game Evolution

> Case Study of my First Slot Game as it Goes From a Terminal Version to a Polished Web App

![](assets/STAGE%205.gif)

## 📋 Overview

I know the best way to get better at something is by doing it. Hence I picked a fun and enjoyable project that is way above my current level of knowledge.
This case study documents the evolution of a slot machine game from a minimalist terminal-based prototype to a full web app with a real backend and a database.
The project showcases my learning experience, demonstrates iterative development, UI/UX improvements, and feature expansion.

**Original Concept:** Terminal-based slot machine with 1 row and 3 reels

**Current Version:** Web-based 20-line slot game with 5 reels and 3 rows, a FastAPI backend and a PostgreSQL database

## 🛠️ Tech Stack

**Backend:** Python, FastAPI, SQLAlchemy, PostgreSQL

**Frontend:** Jinja templates, vanilla JavaScript, CSS grid

**Testing:** pytest, Hypothesis

## 🔜 Next Version Should:

The slot is mostly done for now, so the next step is turning it into a whole casino (play money only, just for practice).

**1. Finish the slot**
- [ ] Hold the win after a spin and only add it to the balance when you press a take win button, so double or nothing can be added later.

**2. Restructure into a casino (no new features, just moving things)**
- [ ] Every game gets its own folder and its own FastAPI router.
- [ ] One base template with a header and a sidebar that every page extends.
- [ ] One shared player and balance across all the games.
- [ ] Database changes go through Alembic migrations instead of create_tables.py.

**3. Accounts**
- [ ] Register and login with hashed passwords.
- [ ] Guest players can keep their balance when they make an account.
- [ ] User profiles with a username, an avatar and stats like biggest win and total wagered.
- [ ] A history page with a table and pagination.

**4. Roulette**
- [ ] Everyone plays the same round, there's a countdown, you bet on red, black or green and the strip slides to the result.
- [ ] Rounds run on the server in a background loop and get pushed to every browser live with WebSockets.
- [ ] A live list of everyone's bets in the current round.
- [ ] Provably fair results, so players can check the outcome wasn't changed after they bet.

**5. Sweet Bonanza style slot**
- [ ] 6 reels and 5 rows where 8 or more of the same symbol anywhere on the screen pays.
- [ ] Tumbling, winning symbols explode and new ones fall in from the top.
- [ ] Free spins with multipliers.

**Later**
- [ ] UI upgrade with custom icons, artwork and sounds.
- [ ] Double or nothing after a win.
- [ ] Docker and hosting it online.

## 📜 The Stages

Click a stage to open it.

<details>
<summary><b>Stage 1 - Terminal</b></summary>

<br>

I decided to first make the slot as straightforward as possible and then upgrade on it.
Broke the project into smaller tasks like:

- How a slot machine works?
- How to display the reels?
- Check if you have enough money to spin?
- How to deduct spin from balance?
- How to add wins to balance etc?

And started tackling them one by one.

You currently get $1000 to spin the machine.
Before you spin the program checks if you have enough balance to make a bet.
3 symbols get picked and put into the row using random.choice()
If the row has 3 of the same symbols you win a variable prize based on the symbols you get.
Prize gets added to balance and we wait for a new spin.
Each spin is initiated on a key press of any kind, meaning you can play using the spacebar.

![](assets/Terminal%20DEMO.gif)

**What this version accomplishes:**

- [x] Break the project into smaller tasks.
- [x] Make the balance updates after each spin.
- [x] Make the basic 1 line, 3 reel terminal version.

</details>

<details>
<summary><b>Stage 2 - 20 Lines Terminal</b></summary>

<br>

The initial version was very simple and not really fun. So I wanted to introduce 20 pay lines, wilds, scatter symbols and fix the RTP between 94% and 98%.

![](assets/20%20lines%20DEMO.gif)

**What this version accomplishes:**

- [x] 20 Pay lines across 5 reels and 3 rows.
- [x] Joker is a wild symbol.
- [x] There is now a scatter symbol that pays cash when it lands on reels 1, 3 and 5.
- [x] RTP tested between 94% and 98%.
- [x] Written tests to make sure line combinations pay the right amount by using Hypothesis.

</details>

<details>
<summary><b>Stage 3 - First Web Version</b></summary>

<br>

Decided it's time to get the web version going.

![](assets/WEB%20DEMO.gif)

**What this version accomplishes:**

- [x] Basic web interface.
- [x] FastAPI integration.

</details>

<details>
<summary><b>Stage 4 - Sessions, Real API and Animations</b></summary>

<br>

The web version worked but the balance was a single global variable, so every player shared the same money. That had to go first. I gave each player a unique id in a cookie and moved the balance, the bet size and the last screen into a server side session, so now your money is yours and it survives a refresh.

After that I cleaned up the API. GET /state paints your balance and last win on page load, POST /bet validates the bet against the allowed sizes instead of trusting whatever the browser sends, and the status codes actually mean something now, 402 when you can't afford the spin and 401 when there is no session. /spin became a POST too, because a GET is supposed to be safe and mine was taking money, which meant you could spin by pasting the url or by the browser prefetching it.

Then came the part that took the longest, making it feel like a slot machine. I threw away the one shot CSS transition and switched to keyframe animations, one that loops forever and one that lands. The reels now spin until the server answers instead of waiting for it, and each reel is 3 tiles longer than the one before it so they all start together at the same speed but stop one after the other. The distance and the duration both come from the same CSS variable so they can't drift apart. Sounds play on animationend now so they can't desync from the animation, the win counter ticks up after the reels stop instead of spoiling the result, and the spin button has three states so you can't spam it.

![](assets/STAGE%204.gif)

**What this version accomplishes:**

- [x] Unique player id in a cookie with a server side session.
- [x] Balance, bet size and last screen stored per player.
- [x] GET /state, POST /bet and POST /spin with proper status codes.
- [x] Bet size validated on the server instead of trusting the browser.
- [x] Last screen saved and rendered into the page on load so there is no blank flash.
- [x] Reels loop until the server responds instead of waiting for it.
- [x] Reels start together and land one at a time.
- [x] Landing sounds fired by the animation itself, no timers.
- [x] Winnings count up after the reels stop.
- [x] Idle, waiting and spinning states with a spin and a stop button.
- [x] Be able to spin with spacebar.

</details>

<details open>
<summary><b>Stage 5 - Database, Clean Backend and New Reels</b></summary>

<br>

The sessions lived in a python dict, so every time the server restarted everybody lost their money. So I learned SQLAlchemy and moved everything into PostgreSQL. The Player is a real model now with the screen stored as JSONB, and every spin gets saved into a spins table with a foreign key to the player, so there is a /history route that gives you your last 100 spins.

Then I cleaned up the backend. The routes were doing everything, so I moved all the game and database logic into a CasinoService class and now main.py only does http stuff. Every action that changes money loads the player with a row lock, so you can't fire 20 requests at the same time and spend the same balance twice (I tested it with 20 curls at once and checked the sums in SQL). FastAPI dependencies give every request its own database session and read the cookie, and the player errors carry their own status codes, so one exception handler turns all of them into http errors and the try/excepts are gone.

On the frontend I rewrote the reels again, this time without WAAPI. Every reel is an object with its own state and one requestAnimationFrame loop moves them all at a constant speed using the time between frames, so it's the same on every screen. New symbols spawn in a hidden tile on top, the result drops in first and the reel overshoots a little and bounces back when it lands. If you hit stop all the reels land together, otherwise they land one after the other, and the bet buttons work as stop buttons mid spin.

Last I made it harder to break. There is a 500ms cooldown on /spin so spamming it gets you a 429 before any money is taken, the frontend checks your balance before it even sends a request, a failed spin snaps the reels back and shows the error in a message bar instead of spinning forever, and I fixed the layout so the bet buttons don't change size anymore and everything is centered.

**What this version accomplishes:**

- [x] Players and spins stored in PostgreSQL with SQLAlchemy, so nothing gets lost on a restart.
- [x] Spin history with a /history route.
- [x] All the game logic in a CasinoService, the routes only do http.
- [x] Row locks so the balance can't be double spent with parallel requests.
- [x] FastAPI dependencies for the database session and the cookie.
- [x] One exception handler for all the player errors.
- [x] New requestAnimationFrame reels with a constant speed, an overshoot and a bounce.
- [x] Stopping early lands all the reels together.
- [x] 500ms spin cooldown on the server (429).
- [x] Failed spins show an error instead of spinning forever.
- [x] Fixed and centered layout.

</details>
