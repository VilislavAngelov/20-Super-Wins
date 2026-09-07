const spin_button = document.getElementById('spin-button');
const stop_button = document.getElementById('stop-button');
const balance = document.getElementById('balance');
const winnings = document.getElementById('winnings');
const strips = document.querySelectorAll('.strip');
const reels = document.querySelectorAll('.reel');
const bet_select = document.getElementById('bet-select');
const reset_balance = document.getElementById('reset-balance');
let bet_buttons = document.getElementsByClassName("bet-amount");
const SYMBOLS = ["🍋", "🍒", "🍊", "🍉", "🍇", "👑", "🃏", "⭐"];
let landing_sound0 = new Audio("/static/sounds/land.wav");
let landing_sound1 = new Audio("/static/sounds/land.wav");
let landing_sound2 = new Audio("/static/sounds/land.wav");
let landing_sound3 = new Audio("/static/sounds/land.wav");
let landing_sound4 = new Audio("/static/sounds/land.wav");
let landing_sounds = [landing_sound0, landing_sound1, landing_sound2, landing_sound3, landing_sound4];
let interval = 2000;
let spin_result = null
let animations = []
let landings = []
let last_lap = [0, 0, 0, 0, 0]
let spin_data = null
let laps_after_result = [0, 0, 0, 0, 0]
let stopping = false
let landed = 0
let show_index = 0
let win_timer = null

for (let i = 0; i < bet_buttons.length; i++) {
    bet_buttons[i].addEventListener('click', async (e) => {
        await fetch('/bet', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ bet_size: Number(e.target.dataset.bet) })
        })
        doSpin()
    })
}

async function loadState() {
    const response = await fetch('/state');
    const data = await response.json();

    balance.textContent = 'Balance: $' + data.balance;
    winnings.textContent = 'Last Win: $' + data.last_win;
}

// I need to make this function spin infinitely until we get a response from the /spin api and a response code
// we have to select the screen and insert it in the infinitely spinning animation
function spin_animation() {
    strips.forEach((strip, reel) => {
        const symbols = strip.querySelectorAll('.symbol')
        const tiles = (symbols.length - 3)
        const travel = tiles * symbols[0].offsetHeight

        for (let i = 0; i < symbols.length - 3; i++) {
            symbols[i].textContent = SYMBOLS[Math.floor(Math.random() * SYMBOLS.length)]
        }

        animations[reel] = strip.animate(
            [
                { transform: `translateY(-${travel}px)` },
                { transform: "translateY(0)" }
            ],
            {
                duration: travel,
                iterations: Infinity
            }
        )
    })
}

function value() {
    let startValue = 0,
        endValue = spin_data.winnings,
        duration = Math.floor(interval / endValue);
    let counter = setInterval(function () {
        startValue += 1;
        winnings.textContent = 'Winnings: $' + startValue;
        if (startValue >= endValue) {
            clearInterval(counter);
        }
    }, duration);
}

function display_wins() {
    change_spin_state('IDLE')
    if (spin_data.winnings > 0) {
        value();
        balance.textContent = 'Balance: $' + spin_data.balance;
    } else {
        winnings.textContent = 'Last Win: $' + spin_data.last_win
        balance.textContent = 'Balance: $' + spin_data.balance;
    }
}

function clear_wins() {
    document.querySelectorAll('.symbol').forEach(s => s.classList.remove('lit'))
}

function light_wins(i) {
    for (const [reel, row] of spin_data.wins[i].cells) {
        strips[reel].querySelectorAll('.symbol')[row].classList.add("lit")
    }
}

function show_next_win() {

    if(show_index == spin_data.wins.length) {
        clear_wins()
        for (let i = 0; i < spin_data.wins.length; i++) {
        light_wins(i)}
        clearInterval(win_timer) 
    } else {
        clear_wins()
        light_wins(show_index)
        show_index += 1
    }  

}

async function doSpin() {
    spin_result = null
    last_lap = [0, 0, 0, 0, 0]
    stopping = false
    landed = 0
    laps_after_result = [0, 0, 0, 0, 0]
    show_index = 0
    clearInterval(win_timer)
    clear_wins()
    change_spin_state('WAITING')
    spin_animation()
    const response = await fetch('/spin', { method: "POST" });
    const data = await response.json();
    spin_data = data

    if (response.ok) {
        change_spin_state('SPINNING')
        balance.textContent = 'Balance: $' + data.spin_balance;

        spin_result = data.screen
    }
}

spin_button.addEventListener('click', async () => {
    doSpin()
})

stop_button.addEventListener('click', () => {
    if (spin_result === null) return
    stopping = true
    stop_button.disabled = true
})

reset_balance.addEventListener('click', async () => {
    const response = await fetch('/reset-balance', { method: "POST" });
    const data = await response.json();

    balance.textContent = 'Balance: $' + data
})

function change_spin_state(spin_state) {
    switch (spin_state) {
        case 'IDLE':
            spin_button.disabled = false;
            spin_button.style.display = 'block';
            stop_button.disabled = true;
            stop_button.style.display = 'none';
            break;
        case 'WAITING':
            spin_button.disabled = true;
            spin_button.style.display = 'none';
            stop_button.disabled = true;
            stop_button.style.display = 'none';
            break;
        case 'SPINNING':
            spin_button.disabled = true;
            spin_button.style.display = 'none';
            stop_button.disabled = false;
            stop_button.style.display = 'block';
            break;
    }
}

function land(reel) {
    const strip = strips[reel]
    const symbols = strip.querySelectorAll('.symbol')
    const travel = (symbols.length - 3) * symbols[0].offsetHeight

    animations[reel].cancel()

    landings[reel] = strip.animate(
        [
            { transform: `translateY(-${travel}px)` },
            { transform: "translateY(0)" }
        ],
        { duration: travel, easing: 'linear' }
    )

    landings[reel].finished.then(() => {
        landing_sounds[reel].currentTime = 0
        landing_sounds[reel].play().catch(() => { })

        symbols[symbols.length - 3].textContent = symbols[0].textContent
        symbols[symbols.length - 2].textContent = symbols[1].textContent
        symbols[symbols.length - 1].textContent = symbols[2].textContent

        landed++
        if (landed === strips.length){
            display_wins()
            
            if (spin_data.wins.length > 0) {
                win_timer = setInterval(show_next_win, 500)
            }
        } 
    })
}

function watch_animation() {
    animations.forEach((animation, reel) => {
        const symbols = strips[reel].querySelectorAll('.symbol')
        let lap = Math.floor(animation.currentTime / animation.effect.getTiming().duration)

        if (animation.playState == 'idle') {

        } else if (lap !== last_lap[reel]) {
            symbols[symbols.length - 3].textContent = symbols[0].textContent
            symbols[symbols.length - 2].textContent = symbols[1].textContent
            symbols[symbols.length - 1].textContent = symbols[2].textContent

            if (spin_result !== null) laps_after_result[reel] += 1

            if (spin_result !== null && (stopping || laps_after_result[reel] > reel)) {
                for (let i = 0; i < 3; i++) {
                    symbols[i].textContent = spin_result[reel][i]
                }
                land(reel)
            } else {
                for (let i = 0; i < 3; i++) {
                    symbols[i].textContent = SYMBOLS[Math.floor(Math.random() * SYMBOLS.length)]
                }
            }
        }
        last_lap[reel] = lap
    })
    requestAnimationFrame(watch_animation)
}

loadState()
requestAnimationFrame(watch_animation)
