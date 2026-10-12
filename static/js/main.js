const spin_button = document.getElementById("spin-button");
const stop_button = document.getElementById("stop-button");
const balance = document.getElementById("balance");
const winnings = document.getElementById("winnings");
const strips = document.querySelectorAll(".strip");
const reset_balance = document.getElementById("reset-balance");
const balance_error = document.getElementById("balance-error")
const SYMBOLS = ["🍋", "🍒", "🍊", "🍉", "🍇", "👑", "🃏", "⭐"];
const SYMBOL_HEIGHT = 100
const SPEED = 1
const OVERSHOOT = 30
const BOUNCE_MS = 120
const FIRST = 2
const GAP = 3
const COUNT_UP_MS = 2000;
const reels = [];

let bet_buttons = document.getElementsByClassName("bet-amount");
let spin_result = null;
let spin_data = null;
let stopping = false;
let landed = 0;
let show_index = 0;
let win_timer = null;
let spin_state = "IDLE";
let player_balance
let player_bet

strips.forEach((strip, index) => {
	reels.push({
		index: index,
		strip: strip,
		tiles: [...strip.querySelectorAll(".symbol")],
		y: 0,
		state: "IDLE",
		queue: [],
		steps: 0,
		bounceStart: 0,
		landing_sound: new Audio("/static/sounds/land.wav"),
	});
});

function random_symbol() {
	return SYMBOLS[Math.floor(Math.random() * SYMBOLS.length)];
}

function draw(reel) {
	reel.strip.style.transform = `translateY(${reel.y - SYMBOL_HEIGHT}px)`;
}

function shiftDown(reel) {
	for (let i = 3; i > 0; i--) {
		reel.tiles[i].textContent = reel.tiles[i-1].textContent
	}

	if (reel.queue.length > 0) {
		reel.tiles[0].textContent = reel.queue.shift();
	} else {
		reel.tiles[0].textContent = random_symbol();
	}

	reel.steps++;
}

let last = performance.now()
function frame(now) {
	const dt = Math.min(now - last, 50)
	last = now
	for (const reel of reels) update(reel, now, dt);
	requestAnimationFrame(frame)
}

function update(reel, now, dt) {
	if (reel.state === "SPINNING" || reel.state === "LAND" || reel.state === "OVERSHOOT") {
		reel.y += SPEED * dt
	}
	while (reel.y >= SYMBOL_HEIGHT && reel.state !== "OVERSHOOT") {
		reel.y -= SYMBOL_HEIGHT
		shiftDown(reel)
		if (reel.state === "LAND" && reel.queue.length === 0) {
			reel.state = "OVERSHOOT"
		}
	}
	if (reel.state === "OVERSHOOT" && reel.y >= OVERSHOOT) {
		reel.y = OVERSHOOT
		reel.landing_sound.currentTime = 0;
		reel.landing_sound.play().catch(() => {});
		reel.state = "BOUNCE"
		reel.bounceStart = now
	}
	if(reel.state === "BOUNCE") {
		const t = Math.min((now - reel.bounceStart) / BOUNCE_MS, 1)
		reel.y = OVERSHOOT * (1 - t) ** 3
		if (t === 1) {
			reel.state = "IDLE"

			landed++;
			if (landed === reels.length) {
				display_wins();

				if (spin_data.wins.length > 0) {
					win_timer = setInterval(show_next_win, 300);
				}
			}
		}
	}
	if (reel.state === "SPINNING" && spin_result !== null && (stopping || reel.steps >= FIRST + reel.index * GAP)) {
		startLanding(reel)
	}
	draw(reel)	
}

function startLanding(reel) {
	const column = spin_result[reel.index]
	reel.queue = [column[2], column[1], column[0], random_symbol()]
	reel.state = "LAND"
}

async function loadState() {
	const response = await fetch("/state");
	const data = await response.json();

	player_balance = data.balance
	player_bet = data.bet_size

	balance.textContent = "Balance: $" + data.balance;
	winnings.textContent = "Last Win: $" + data.last_win;
}

spin_button.addEventListener("click", doSpin);

document.body.onkeyup = function (e) {
	if (e.code == "Space") {
		if (spin_state == "IDLE") {
			doSpin();
		} else if (spin_state == "SPINNING" && spin_result !== null) {
			stop_spin()
		}
	}
};

for (let i = 0; i < bet_buttons.length; i++) {
	bet_buttons[i].addEventListener("click", async (e) => {
		if (spin_state == "IDLE") {
			await fetch("/bet", {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({ bet_size: Number(e.target.dataset.bet) }),
			});
			player_bet = Number(e.target.dataset.bet)
			doSpin();
		}		
		stop_spin()
	});
}

stop_button.addEventListener("click", stop_spin);


reset_balance.addEventListener("click", async () => {
	const response = await fetch("/reset-balance", { method: "POST" });
	const data = await response.json();

	balance_error.style.display = "none"
	player_balance = data
	balance.textContent = "Balance: $" + data;
});

async function doSpin() {
	if (player_balance < player_bet) {
		balance_error.style.display = "block"
		return
	}
	if (spin_state == "IDLE") {
		balance_error.style.display = "none"
		spin_result = null;
		stopping = false;
		landed = 0;
		show_index = 0;
		clearInterval(win_timer);
		clear_wins();
		change_spin_state("WAITING");
		for (const reel of reels) reel.state = "SPINNING";
		const response = await fetch("/spin", { method: "POST" });
		const data = await response.json();
		spin_data = data;

		if (response.ok) {
			change_spin_state("SPINNING");

			player_balance = data.spin_balance
			balance.textContent = "Balance: $" + data.spin_balance;

			spin_result = data.screen;
			for (const reel of reels) reel.steps = 0
		}
	}
}

function count_up_winnings() {
	let startValue = 0,
		endValue = spin_data.winnings,
		duration = Math.floor(COUNT_UP_MS / endValue);
	let counter = setInterval(function () {
		startValue += 1;
		winnings.textContent = "Winnings: $" + startValue;
		if (startValue >= endValue) {
			clearInterval(counter);
		}
	}, duration);
}

function display_wins() {
	change_spin_state("IDLE");
	if (spin_data.winnings > 0) {
		count_up_winnings();
	} else {
		winnings.textContent = "Last Win: $" + spin_data.last_win;
	}

	player_balance = spin_data.balance
	balance.textContent = "Balance: $" + spin_data.balance;
}

function clear_wins() {
	document
		.querySelectorAll(".symbol")
		.forEach((s) => s.classList.remove("lit"));
}

function light_wins(i) {
	for (const [reel, row] of spin_data.wins[i].cells) {
		reels[reel].tiles[row+1].classList.add("lit");
	}
}

function show_next_win() {
	if (show_index == spin_data.wins.length) {
		clear_wins();
		for (let i = 0; i < spin_data.wins.length; i++) {
			light_wins(i);
		}
		clearInterval(win_timer);
	} else {
		clear_wins();
		light_wins(show_index);
		show_index += 1;
	}
}

function change_spin_state(new_state) {
	spin_state = new_state

	spin_button.disabled = new_state !== "IDLE"
	stop_button.disabled = new_state !== "SPINNING"
	reset_balance.disabled = new_state !== "IDLE"
	spin_button.style.display = new_state === "IDLE" ? "block" : "none"
	stop_button.style.display = new_state === "SPINNING" ? "block" : "none"
}

function stop_spin() {
	if (spin_result === null) return;
	stopping = true;
	stop_button.disabled = true;
}

loadState();
requestAnimationFrame(frame)
