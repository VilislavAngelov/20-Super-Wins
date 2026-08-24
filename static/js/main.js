const spin_button = document.getElementById('spin-button');
const stop_button = document.getElementById('stop-button');
const balance = document.getElementById('balance');
const winnings = document.getElementById('winnings');
const strips = document.querySelectorAll('.strip');
const bet_select = document.getElementById('bet-select')
const reset_balance = document.getElementById('reset-balance')
let bet_buttons = document.getElementsByClassName("bet-amount")
const SYMBOLS = ["🍋","🍒","🍊","🍉","🍇","👑","🃏","⭐"]
let landing_sound0 = new Audio("/static/sounds/land.wav");
let landing_sound1 = new Audio("/static/sounds/land.wav");
let landing_sound2 = new Audio("/static/sounds/land.wav");
let landing_sound3 = new Audio("/static/sounds/land.wav");
let landing_sound4 = new Audio("/static/sounds/land.wav");
let landing_sounds = [landing_sound0, landing_sound1, landing_sound2, landing_sound3, landing_sound4];
let interval = 2000;
let spin_result = null
let wraps = [0, 0, 0, 0, 0]
let spin_iterations = 2

for(let i = 0; i < bet_buttons.length; i++){
    bet_buttons[i].addEventListener('click', async (e) => {
    await fetch('/bet', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({bet_size: Number(e.target.dataset.bet)})
    })
    doSpin()
})
}

strips.forEach((strip,reel) => {
    const symbols = strip.querySelectorAll('.symbol')
    strip.addEventListener("animationiteration", () => {

        symbols[symbols.length - 3].textContent = symbols[0].textContent
        symbols[symbols.length - 2].textContent = symbols[1].textContent
        symbols[symbols.length - 1].textContent = symbols[2].textContent

        for (let i = 3; i < symbols.length - 3; i++) {
            symbols[i].textContent = SYMBOLS[Math.floor(Math.random() * SYMBOLS.length)]
                
        }
        wraps[reel] += 1 
        if (spin_result != null) {
            if (wraps[reel] < spin_iterations){
                return
            }
            for (let i = 0; i < 3; i++) {
                symbols[i].textContent = spin_result[reel][i]
            }   
            strip.classList.remove('loop')
            strip.classList.add('land')  
        }
    })

    strip.addEventListener("animationend", () => {
        strip.classList.remove('land')
        landing_sounds[reel].currentTime = 0
        landing_sounds[reel].play()
    })
})


async function loadState() {
    const response = await fetch('/state');
    const data = await response.json();

    balance.textContent = 'Balance: $' + data.balance;
    winnings.textContent = 'Last Win: $' + data.last_win;
}

// I need to make this function spin infinitely until we get a response from the /spin api and a response code 
// we have to select the screen and insert it in the infinitely spinning animation 
function spin_animation() {
    strips.forEach((strip,reel) => {
        const symbols = strip.querySelectorAll('.symbol')
        
        symbols[symbols.length - 3].textContent = symbols[0].textContent
        symbols[symbols.length - 2].textContent = symbols[1].textContent
        symbols[symbols.length - 1].textContent = symbols[2].textContent

        for (let i = 3; i < symbols.length - 3; i++) {
                symbols[i].textContent = SYMBOLS[Math.floor(Math.random() * SYMBOLS.length)]
            } 

        strip.classList.add('loop')
    })
}

async function doSpin() {
    spin_result = null
    wraps = [0, 0, 0, 0, 0]
    spin_iterations = 2
    change_spin_state('WAITING')
    spin_animation()
    const response = await fetch('/spin', {method: "POST"});
    const data = await response.json();
    

    if (response.ok){
        change_spin_state('SPINNING')
        balance.textContent = 'Balance: $' + data.spin_balance;
        function value() {
            let startValue = 0,
                endValue = data.winnings,
                duration = Math.floor(interval / endValue);
            let counter = setInterval(function () {
                    startValue += 1;
                    winnings.textContent = 'Winnings: $' + startValue;
                    if (startValue >= endValue){
                        clearInterval(counter);
                    }
                }, duration);
        }

        strips[strips.length - 1].addEventListener("animationend", (strip) => {
            change_spin_state('IDLE')
            if (data.winnings > 0) {
                value();
                balance.textContent = 'Balance: $' + data.balance;
            } else {
                winnings.textContent = 'Last Win: $' + data.last_win
                balance.textContent = 'Balance: $' + data.balance;
            }
        }, { once: true })  
        
        spin_result = data.screen 
    }
}

spin_button.addEventListener('click', async () => {  
    doSpin()
})

stop_button.addEventListener('click', async () => {  
    spin_iterations = 0
    stop_button.disabled = true;
})

reset_balance.addEventListener('click', async () => {
    const response = await fetch('/reset-balance', {method: "POST"});
    const data = await response.json();

    balance.textContent = 'Balance: $' + data
})

function change_spin_state(spin_state) {
    switch(spin_state) {
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

loadState()
