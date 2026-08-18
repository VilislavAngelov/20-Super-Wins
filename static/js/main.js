const spin_button = document.getElementById('spin-button');
const balance = document.getElementById('balance');
const winnings = document.getElementById('winnings');
const strips = document.querySelectorAll('.strip');
const bet_select = document.getElementById('bet-select')
const reset_balance = document.getElementById('reset-balance')
let bet_buttons = document.getElementsByClassName("bet-amount")
//This kind of works but can be abused because someone can use inspect on a bet amount, change it locally and then bet $800 instead of 80 for examle. I think bet sizes should be server size as well as the balance

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

async function loadState() {
    const response = await fetch('/state');
    const data = await response.json();

    balance.textContent = 'Balance: $' + data.balance;
    winnings.textContent = 'Last Win: $' + data.last_win;
}

async function doSpin() {
    const response = await fetch('/spin');
    const data = await response.json();

    if (response.ok){
        strips.forEach((strip, reel) => {
            const symbols = strip.querySelectorAll('.symbol')
                symbols.forEach((symbol, row) => {
                    symbol.textContent = data.screen[reel][row]
            }) 
        });
        balance.textContent = 'Balance: $' + data.balance;
        winnings.textContent = 'Last Win: $' + data.last_win; 
    }
}

spin_button.addEventListener('click', async () => {
    doSpin()
})

reset_balance.addEventListener('click', async () => {
    const response = await fetch('/reset-balance', {method: "POST"});
    const data = await response.json();

    balance.textContent = 'Balance: $' + data
})

loadState()

