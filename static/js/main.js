const spin_button = document.getElementById('spin-button');
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
let interval = 1000;
let last_reel = false;
//This kind of works but can be abused because someone can use inspect on a bet amount, change it locally and then bet $800 instead of 80 for examle. I think bet sizes should be server size as well as the balance

for(let i = 0; i < bet_buttons.length; i++){
    bet_buttons[i].addEventListener('click', async (e) => {
    fetch('/bet', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({bet_size: Number(e.target.dataset.bet)})
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

function spin_animation() {
    strips.forEach((strip, reel) => {
        strip.addEventListener("transitionend", () => {
            landing_sounds[reel].play()
        }, { once:true })

        strip.style.transition = 'none'
        strip.style.transform = "translateY(-1700px)";
        strip.offsetHeight;

        strip.style.transition = ''
        strip.style.transitionDuration = (1.5 + reel * 0.3) + 's'
        strip.style.transform = "translateY(0)";
    })
    
}

async function doSpin() {
    const response = await fetch('/spin');
    const data = await response.json();

    if (response.ok){
        strips.forEach((strip, reel) => {

            const symbols = strip.querySelectorAll('.symbol')
            const old0 = symbols[0].textContent
            const old1 = symbols[1].textContent
            const old2 = symbols[2].textContent
            let interval = 1000
            
            symbols.forEach((symbol) => {
                symbol.textContent = SYMBOLS[Math.floor(Math.random() * SYMBOLS.length)]
            })

            data.screen[reel].forEach((char, row) => {
                symbols[row].textContent = char
            }) 

            symbols[17].textContent = old0
            symbols[18].textContent = old1
            symbols[19].textContent = old2
        });

        function value() {
            let startValue = 0,
                endValue = data.last_win,
                duration = Math.floor(interval / endValue);
            let counter = setInterval(function () {
                    startValue += 1;
                    winnings.textContent = 'Winnings: $' + startValue;
                    if (startValue == endValue){
                        clearInterval(counter);
                    }
                }, duration);
        }

        

        strips[strips.length - 1].addEventListener("transitionend", () => {
            if (data.winnings > 0) {
                value();
                balance.textContent = 'Balance: $' + data.balance;
            } else {
                winnings.textContent = 'Last Win: $' + data.last_win
                balance.textContent = 'Balance: $' + data.balance;
            }
        }, { once: true })

        
        
    }
}

spin_button.addEventListener('click', async () => {
    spin_animation()
    doSpin()
})

reset_balance.addEventListener('click', async () => {
    const response = await fetch('/reset-balance', {method: "POST"});
    const data = await response.json();

    balance.textContent = 'Balance: $' + data
})

loadState()

