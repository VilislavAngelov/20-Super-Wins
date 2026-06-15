const spin_button = document.getElementById('spin-button');
const balance = document.getElementById('balance');
const winnings = document.getElementById('winnings');
const cells = document.querySelectorAll('.symbol');
const bet_select = document.getElementById('bet-select')

balance.textContent = 'Balance: $' + playerBalance;

//This kind of works but can be abused because someone can use inspect on a bet amount, change it locally and then bet $800 instead of 80 for examle. I think bet sizes should be server size as well as the balance

bet_select.addEventListener('click', function(e) {
    BET = parseInt(e.target.dataset.bet);
})

spin_button.addEventListener('click', async () => {
    const response = await fetch('/spin');
    const data = await response.json();

    cells.forEach((cell, i) => {
      cell.textContent = data.screen[i % 5][Math.floor(i / 5)]
    });

    balance.textContent = 'Balance: $' + data.balance;
    winnings.textContent = 'Winnings: $' + data.winnings; 
})


