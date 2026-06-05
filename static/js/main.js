const spin_button = document.getElementById('spin-button');
const balance = document.getElementById('balance');
const winnings = document.getElementById('winnings');
const cells = document.querySelectorAll('.symbol');
let playerBalance = 1000;
const BET = 10;

balance.textContent = 'Balance: $' + playerBalance;

spin_button.addEventListener('click', async () => {
    if (playerBalance < BET) return;

    playerBalance -= BET
    const response = await fetch('/spin');
    const data = await response.json();

    cells.forEach((cell, i) => {
      cell.textContent = data.screen[i % 5][Math.floor(i / 5)]
    });

    playerBalance += data.winnings;
    balance.textContent = 'Balance: $' + playerBalance;
    winnings.textContent = 'Winnings: $' + data.winnings; 
})


