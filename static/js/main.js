const spin_button = document.getElementById("spin-button")
const stop_button = document.getElementById("stop-button")
const double_button = document.getElementById("double-button")
const receive_button = document.getElementById("receive-button")
const balance = document.getElementById("balance-number")
const winnings = document.getElementById("win-label")
const winnings_number = document.getElementById("win-number")
const strips = document.querySelectorAll(".strip")
const reset_balance = document.getElementById("reset-balance")
const player_alert = document.getElementById("player-alert")
const SYMBOLS = ["🍋", "🍒", "🍊", "🍉", "🍇", "👑", "🃏", "⭐"]
const SYMBOL_HEIGHT = 1
const SPEED = 0.01 
const OVERSHOOT = 0.3
const BOUNCE_MS = 120
const FIRST = 2
const GAP = 3
const COUNT_UP_MS = 1000
const reels = [];
const audio_context = new AudioContext()

let bet_buttons = document.getElementsByClassName("bet-amount")
let spin_result = null
let spin_data = null
let stopping = false
let stopping_sound = false
let landed = 0
let show_index = 0
let win_timer = null
let spin_state = "IDLE"
let player_balance
let player_bet
let landSound = null
loadSound("/static/sounds/land.wav").then(buffer => landSound = buffer)

async function loadSound(url) {
	const response = await fetch(url);
	const data = await response.arrayBuffer();
	return await audio_context.decodeAudioData(data);
}

function play(sound) {
	const source = audio_context.createBufferSource();
	source.buffer = sound;
	source.connect(audio_context.destination);
	source.start();
}

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
		stopped: false
	});
});

function random_symbol() {
	return SYMBOLS[Math.floor(Math.random() * SYMBOLS.length)];
}

function draw(reel) {
	reel.strip.style.transform = `translateY(calc(${reel.y - SYMBOL_HEIGHT} * var(--symbol-h)))`;
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
		if (!reel.stopped){
			play(landSound)
		} else if (!stopping_sound) {
			play(landSound)
			stopping_sound = true
		}

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
				console.log(spin_state)
				display_wins();

				if (spin_data.wins.length > 0) {
					change_spin_state("DOUBLE")
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
	reel.stopped = stopping
}

async function loadState() {
	const response = await fetch("/state");
	const data = await response.json();

	player_balance = data.balance
	player_bet = data.bet_size

	balance.textContent = "$" + data.balance;
	winnings.textContent = "Last Win";
	winnings_number.textContent = "$" + data.last_win;
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

	player_alert.style.display = "none"
	player_balance = data
	balance.textContent = "$" + data;
});

async function doSpin() {
	audio_context.resume()
	if (player_balance < player_bet) {
		player_alert.textContent = "Not enough balance" 
		player_alert.style.display = "block"
		return
	}
	if (spin_state == "IDLE" || spin_state == "DOUBLE") {
		stopping_sound = false
		player_alert.style.display = "none"
		spin_result = null;
		stopping = false;
		landed = 0;
		show_index = 0;
		const last_screen = currentScreen()
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
			balance.textContent = "$" + data.spin_balance;

			spin_result = data.screen;
			for (const reel of reels) reel.steps = 0
		} else {
			reels.forEach((reel) => {
				for (let i = 1; i <= 3; i++) {
					reel.tiles[i].textContent = last_screen[reel.index][i-1]
				}
				reel.state = "IDLE"
				reel.y = 0
			})
			change_spin_state("IDLE")	
			player_alert.textContent = data.detail 
			player_alert.style.display = "block"
		}
	}
}

function count_up_winnings() {

	const endValue = spin_data.winnings
	let start = performance.now()
	
	winnings.textContent = "Winnings"

	function tick(now) {
		const progress = Math.min((now - start) / COUNT_UP_MS, 1)
		winnings_number.textContent = "$" + Math.floor(endValue * progress)

		if(progress < 1) {
			requestAnimationFrame(tick)
		}
	}
	requestAnimationFrame(tick)
}

function display_wins() {
	change_spin_state("IDLE");
	if (spin_data.winnings > 0) {
		count_up_winnings();
	} else {
		winnings.textContent = "Last Win";
		winnings_number.textContent = "$" + spin_data.last_win;
	}

	player_balance = spin_data.balance
	balance.textContent = "$" + spin_data.balance;
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

	spin_button.disabled = new_state !== "IDLE" && new_state !== "DOUBLE"
	stop_button.disabled = new_state !== "SPINNING"
	reset_balance.disabled = new_state !== "IDLE"
	spin_button.style.display = new_state === "IDLE" || new_state === "DOUBLE" ? ""  : "none"
	stop_button.style.display = new_state === "SPINNING" || new_state === "WAITING" ? "block" : "none"

	receive_button.style.display = new_state === "DOUBLE" ? "" : "none";
	receive_button.disabled = new_state !== "DOUBLE"

	double_button.style.display = new_state === "DOUBLE" ? "" : "none";
	double_button.disabled = new_state !== "DOUBLE"



}

function stop_spin() {
	if (spin_result === null) return;
	stopping = true;
	stop_button.disabled = true;
}

function currentScreen() {
	const current_screen = []

	reels.forEach((reel) => {
		const iter_reel = []
		for (let i = 1; i <= 3; i++) {
			iter_reel.push(reel.tiles[i].textContent)
		}
		current_screen.push(iter_reel)
	})

	return current_screen
}

loadState();
requestAnimationFrame(frame)