// Buypolar Capital - Games Module

// Initialize all games
function initializeGames() {
    try {
        initializeRoulette();
        initializeBlackjack();
        initializeDice();
        initializeRandomWalk();
        initializePoker();
        initializeMontyHall();
        initializeKellyCriterion();
        initializeRiskOfRuin();
    } catch (error) {
        handleError(error, 'initializing games');
    }
}

// Roulette game
function initializeRoulette() {
    const spinBtn = document.getElementById('spin-roulette');
    if (spinBtn) {
        spinBtn.addEventListener('click', spinRoulette);
    }
    
    const autoPlayBtn = document.getElementById('auto-play-roulette');
    if (autoPlayBtn) {
        autoPlayBtn.addEventListener('click', autoPlayRoulette);
    }
    
    const resetBtn = document.getElementById('reset-roulette');
    if (resetBtn) {
        resetBtn.addEventListener('click', resetRoulette);
    }
}

function spinRoulette() {
    const wheel = document.getElementById('roulette-wheel');
    const result = Math.floor(Math.random() * 37); // 0-36
    const spins = document.getElementById('roulette-spins');
    const wins = document.getElementById('roulette-wins');
    const losses = document.getElementById('roulette-losses');
    
    // Animate wheel
    const rotation = 360 * 5 + (result * (360 / 37));
    wheel.style.transform = `rotate(${rotation}deg)`;
    
    // Update stats
    const currentSpins = parseInt(spins.textContent) + 1;
    spins.textContent = currentSpins;
    
    // Simple betting on red/black
    const isRed = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36].includes(result);
    const isBlack = [2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35].includes(result);
    
    if (isRed) {
        wins.textContent = parseInt(wins.textContent) + 1;
    } else if (isBlack) {
        losses.textContent = parseInt(losses.textContent) + 1;
    }
    
    updateRouletteStats();
    updateRouletteChart();
}

function autoPlayRoulette() {
    const interval = setInterval(spinRoulette, 1000);
    setTimeout(() => clearInterval(interval), 10000); // Stop after 10 seconds
}

function updateRouletteStats() {
    const spins = parseInt(document.getElementById('roulette-spins').textContent);
    const wins = parseInt(document.getElementById('roulette-wins').textContent);
    const winRate = spins > 0 ? ((wins / spins) * 100).toFixed(1) : '0.0';
    document.getElementById('roulette-win-rate').textContent = winRate + '%';
}

function resetRoulette() {
    document.getElementById('roulette-spins').textContent = '0';
    document.getElementById('roulette-wins').textContent = '0';
    document.getElementById('roulette-losses').textContent = '0';
    document.getElementById('roulette-win-rate').textContent = '0.0%';
    updateRouletteChart();
}

function updateRouletteChart() {
    if (typeof Chart === 'undefined') return;
    
    const ctx = document.getElementById('roulette-chart');
    if (!ctx) return;
    
    const spins = parseInt(document.getElementById('roulette-spins').textContent);
    const wins = parseInt(document.getElementById('roulette-wins').textContent);
    const losses = parseInt(document.getElementById('roulette-losses').textContent);
    
    const data = {
        labels: ['Wins', 'Losses'],
        datasets: [{
            data: [wins, losses],
            backgroundColor: ['#4CAF50', '#f44336'],
            borderWidth: 0
        }]
    };
    
    const config = {
        type: 'doughnut',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    };
    
    try {
        if (window.rouletteChart) {
            window.rouletteChart.destroy();
        }
        window.rouletteChart = new Chart(ctx, config);
    } catch (error) {
        console.log('Error updating roulette chart:', error);
    }
}

// Blackjack game
let blackjackDeck = [];
let playerHand = [];
let dealerHand = [];

function initializeBlackjack() {
    const dealBtn = document.getElementById('deal-blackjack');
    if (dealBtn) {
        dealBtn.addEventListener('click', dealBlackjack);
    }
    
    const hitBtn = document.getElementById('hit-blackjack');
    if (hitBtn) {
        hitBtn.addEventListener('click', hitBlackjack);
    }
    
    const standBtn = document.getElementById('stand-blackjack');
    if (standBtn) {
        standBtn.addEventListener('click', standBlackjack);
    }
    
    const doubleBtn = document.getElementById('double-blackjack');
    if (doubleBtn) {
        doubleBtn.addEventListener('click', doubleBlackjack);
    }
    
    const resetBtn = document.getElementById('reset-blackjack');
    if (resetBtn) {
        resetBtn.addEventListener('click', resetBlackjack);
    }
}

function dealBlackjack() {
    blackjackDeck = createDeck();
    shuffleDeck(blackjackDeck);
    
    playerHand = [blackjackDeck.pop(), blackjackDeck.pop()];
    dealerHand = [blackjackDeck.pop(), blackjackDeck.pop()];
    
    displayBlackjackHands(false);
    updateBlackjackStats();
}

function hitBlackjack() {
    if (playerHand.length === 0) return;
    
    playerHand.push(blackjackDeck.pop());
    displayBlackjackHands(false);
    
    if (calculateHandValue(playerHand) > 21) {
        endBlackjackGame();
    }
}

function standBlackjack() {
    if (playerHand.length === 0) return;
    
    while (calculateHandValue(dealerHand) < 17) {
        dealerHand.push(blackjackDeck.pop());
    }
    
    displayBlackjackHands(true);
    endBlackjackGame();
}

function doubleBlackjack() {
    if (playerHand.length === 2) {
        hitBlackjack();
        if (calculateHandValue(playerHand) <= 21) {
            standBlackjack();
        }
    }
}

function endBlackjackGame() {
    const playerValue = calculateHandValue(playerHand);
    const dealerValue = calculateHandValue(dealerHand);
    
    let result = '';
    if (playerValue > 21) {
        result = 'Bust! You lose.';
    } else if (dealerValue > 21) {
        result = 'Dealer busts! You win!';
    } else if (playerValue > dealerValue) {
        result = 'You win!';
    } else if (dealerValue > playerValue) {
        result = 'Dealer wins.';
    } else {
        result = 'Push!';
    }
    
    document.getElementById('blackjack-result').textContent = result;
    updateBlackjackStats();
}

function createDeck() {
    const suits = ['♠', '♥', '♦', '♣'];
    const values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'];
    const deck = [];
    
    for (let suit of suits) {
        for (let value of values) {
            deck.push({ suit, value });
        }
    }
    
    return deck;
}

function shuffleDeck(deck) {
    for (let i = deck.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [deck[i], deck[j]] = [deck[j], deck[i]];
    }
}

function calculateHandValue(hand) {
    let value = 0;
    let aces = 0;
    
    for (let card of hand) {
        if (card.value === 'A') {
            aces++;
            value += 11;
        } else if (['K', 'Q', 'J'].includes(card.value)) {
            value += 10;
        } else {
            value += parseInt(card.value);
        }
    }
    
    while (value > 21 && aces > 0) {
        value -= 10;
        aces--;
    }
    
    return value;
}

function displayBlackjackHands(showAll = false) {
    const playerDisplay = document.getElementById('player-hand');
    const dealerDisplay = document.getElementById('dealer-hand');
    
    if (playerDisplay) {
        playerDisplay.innerHTML = playerHand.map(card => 
            `<span class="card ${card.suit === '♥' || card.suit === '♦' ? 'red' : ''}">${card.value}${card.suit}</span>`
        ).join('');
        playerDisplay.innerHTML += ` <strong>(${calculateHandValue(playerHand)})</strong>`;
    }
    
    if (dealerDisplay) {
        if (showAll) {
            dealerDisplay.innerHTML = dealerHand.map(card => 
                `<span class="card ${card.suit === '♥' || card.suit === '♦' ? 'red' : ''}">${card.value}${card.suit}</span>`
            ).join('');
            dealerDisplay.innerHTML += ` <strong>(${calculateHandValue(dealerHand)})</strong>`;
        } else {
            dealerDisplay.innerHTML = `<span class="card">${dealerHand[0].value}${dealerHand[0].suit}</span> <span class="card back">?</span>`;
        }
    }
}

function updateBlackjackStats() {
    const games = parseInt(document.getElementById('blackjack-games').textContent) + 1;
    document.getElementById('blackjack-games').textContent = games;
}

function resetBlackjack() {
    playerHand = [];
    dealerHand = [];
    blackjackDeck = [];
    
    document.getElementById('player-hand').innerHTML = '';
    document.getElementById('dealer-hand').innerHTML = '';
    document.getElementById('blackjack-result').textContent = '';
}

// Dice game
function initializeDice() {
    const rollBtn = document.getElementById('roll-dice');
    if (rollBtn) {
        rollBtn.addEventListener('click', rollDice);
    }
    
    const rollManyBtn = document.getElementById('roll-many-dice');
    if (rollManyBtn) {
        rollManyBtn.addEventListener('click', rollManyDice);
    }
    
    const resetBtn = document.getElementById('reset-dice');
    if (resetBtn) {
        resetBtn.addEventListener('click', resetDice);
    }
}

function rollDice() {
    const result = Math.floor(Math.random() * 6) + 1;
    const diceDisplay = document.getElementById('dice-result');
    const rolls = document.getElementById('dice-rolls');
    const average = document.getElementById('dice-average');
    
    if (diceDisplay) {
        diceDisplay.innerHTML = getDiceSymbol(result);
    }
    
    const currentRolls = parseInt(rolls.textContent) + 1;
    rolls.textContent = currentRolls;
    
    // Update average
    const currentAvg = parseFloat(average.textContent);
    const newAvg = ((currentAvg * (currentRolls - 1)) + result) / currentRolls;
    average.textContent = newAvg.toFixed(2);
    
    updateDiceStats();
    updateDiceChart();
}

function rollManyDice() {
    const count = 100;
    let total = 0;
    
    for (let i = 0; i < count; i++) {
        total += Math.floor(Math.random() * 6) + 1;
    }
    
    const rolls = document.getElementById('dice-rolls');
    const average = document.getElementById('dice-average');
    
    const currentRolls = parseInt(rolls.textContent) + count;
    rolls.textContent = currentRolls;
    
    const currentAvg = parseFloat(average.textContent);
    const newAvg = ((currentAvg * (currentRolls - count)) + total) / currentRolls;
    average.textContent = newAvg.toFixed(2);
    
    updateDiceStats();
    updateDiceChart();
}

function getDiceSymbol(number) {
    const symbols = ['⚀', '⚁', '⚂', '⚃', '⚄', '⚅'];
    return symbols[number - 1];
}

function updateDiceStats() {
    const rolls = parseInt(document.getElementById('dice-rolls').textContent);
    const average = parseFloat(document.getElementById('dice-average').textContent);
    const expected = 3.5;
    const variance = Math.abs(average - expected);
    document.getElementById('dice-variance').textContent = variance.toFixed(3);
}

function updateDiceChart() {
    if (typeof Chart === 'undefined') return;
    
    const ctx = document.getElementById('dice-chart');
    if (!ctx) return;
    
    const rolls = parseInt(document.getElementById('dice-rolls').textContent);
    const average = parseFloat(document.getElementById('dice-average').textContent);
    
    const data = {
        labels: ['Current Average', 'Expected Value'],
        datasets: [{
            data: [average, 3.5],
            backgroundColor: ['#2196F3', '#FF9800'],
            borderWidth: 0
        }]
    };
    
    const config = {
        type: 'bar',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 6
                }
            }
        }
    };
    
    try {
        if (window.diceChart) {
            window.diceChart.destroy();
        }
        window.diceChart = new Chart(ctx, config);
    } catch (error) {
        console.log('Error updating dice chart:', error);
    }
}

function resetDice() {
    document.getElementById('dice-rolls').textContent = '0';
    document.getElementById('dice-average').textContent = '0.00';
    document.getElementById('dice-variance').textContent = '0.000';
    document.getElementById('dice-result').innerHTML = '';
    updateDiceChart();
}

// Random Walk
function initializeRandomWalk() {
    const walkBtn = document.getElementById('walk-random');
    if (walkBtn) {
        walkBtn.addEventListener('click', simulateRandomWalk);
    }
    
    const manyWalksBtn = document.getElementById('many-walks');
    if (manyWalksBtn) {
        manyWalksBtn.addEventListener('click', simulateManyWalks);
    }
    
    const resetBtn = document.getElementById('reset-random-walk');
    if (resetBtn) {
        resetBtn.addEventListener('click', resetRandomWalk);
    }
}

function simulateRandomWalk() {
    const steps = 100;
    const walk = [0];
    
    for (let i = 1; i <= steps; i++) {
        const step = Math.random() > 0.5 ? 1 : -1;
        walk.push(walk[i-1] + step);
    }
    
    updateRandomWalkChart(walk);
}

function simulateManyWalks() {
    const walks = 10;
    const steps = 100;
    const allWalks = [];
    
    for (let w = 0; w < walks; w++) {
        const walk = [0];
        for (let i = 1; i <= steps; i++) {
            const step = Math.random() > 0.5 ? 1 : -1;
            walk.push(walk[i-1] + step);
        }
        allWalks.push(walk);
    }
    
    updateRandomWalkChart(allWalks[0], allWalks);
}

function updateRandomWalkChart(walk, allWalks = null) {
    if (typeof Chart === 'undefined') return;
    
    const ctx = document.getElementById('random-walk-chart');
    if (!ctx) return;
    
    const labels = Array.from({length: walk.length}, (_, i) => i);
    
    const datasets = [{
        label: 'Random Walk',
        data: walk,
        borderColor: '#2196F3',
        backgroundColor: 'rgba(33, 150, 243, 0.1)',
        borderWidth: 2,
        fill: false
    }];
    
    if (allWalks) {
        allWalks.forEach((w, index) => {
            if (index > 0) {
                datasets.push({
                    label: `Walk ${index + 1}`,
                    data: w,
                    borderColor: `hsl(${index * 30}, 70%, 50%)`,
                    backgroundColor: 'transparent',
                    borderWidth: 1,
                    fill: false
                });
            }
        });
    }
    
    const data = {
        labels: labels,
        datasets: datasets
    };
    
    const config = {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    };
    
    try {
        if (window.randomWalkChart) {
            window.randomWalkChart.destroy();
        }
        window.randomWalkChart = new Chart(ctx, config);
    } catch (error) {
        console.log('Error updating random walk chart:', error);
    }
}

function resetRandomWalk() {
    const ctx = document.getElementById('random-walk-chart');
    if (ctx && window.randomWalkChart) {
        window.randomWalkChart.destroy();
    }
}

// Poker game
function initializePoker() {
    const dealBtn = document.getElementById('deal-poker');
    if (dealBtn) {
        dealBtn.addEventListener('click', dealPokerHand);
    }
    
    const simulateBtn = document.getElementById('simulate-poker');
    if (simulateBtn) {
        simulateBtn.addEventListener('click', simulatePokerHands);
    }
    
    const resetBtn = document.getElementById('reset-poker');
    if (resetBtn) {
        resetBtn.addEventListener('click', resetPoker);
    }
}

function dealPokerHand() {
    const deck = createPokerDeck();
    shufflePokerDeck(deck);
    
    const hand = deck.slice(0, 5);
    const handType = evaluatePokerHand(hand);
    
    displayPokerHand(hand);
    document.getElementById('poker-hand-type').textContent = handType;
    
    updatePokerStats();
    updatePokerChart();
}

function simulatePokerHands() {
    const hands = 1000;
    const handTypes = {};
    
    for (let i = 0; i < hands; i++) {
        const deck = createPokerDeck();
        shufflePokerDeck(deck);
        const hand = deck.slice(0, 5);
        const handType = evaluatePokerHand(hand);
        handTypes[handType] = (handTypes[handType] || 0) + 1;
    }
    
    updatePokerChart(handTypes);
}

function createPokerDeck() {
    const suits = ['♠', '♥', '♦', '♣'];
    const values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'];
    const deck = [];
    
    for (let suit of suits) {
        for (let value of values) {
            deck.push({ suit, value });
        }
    }
    
    return deck;
}

function shufflePokerDeck(deck) {
    for (let i = deck.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [deck[i], deck[j]] = [deck[j], deck[i]];
    }
}

function displayPokerHand(hand) {
    const handDisplay = document.getElementById('poker-hand');
    if (handDisplay) {
        handDisplay.innerHTML = hand.map(card => 
            `<span class="card ${card.suit === '♥' || card.suit === '♦' ? 'red' : ''}">${card.value}${card.suit}</span>`
        ).join('');
    }
}

function evaluatePokerHand(hand) {
    const values = hand.map(card => card.value);
    const suits = hand.map(card => card.suit);
    const valueCounts = {};
    
    values.forEach(value => {
        valueCounts[value] = (valueCounts[value] || 0) + 1;
    });
    
    const counts = Object.values(valueCounts).sort((a, b) => b - a);
    const isFlush = suits.every(suit => suit === suits[0]);
    const isStraight = isSequential(values);
    
    if (isFlush && isStraight) return 'Straight Flush';
    if (counts[0] === 4) return 'Four of a Kind';
    if (counts[0] === 3 && counts[1] === 2) return 'Full House';
    if (isFlush) return 'Flush';
    if (isStraight) return 'Straight';
    if (counts[0] === 3) return 'Three of a Kind';
    if (counts[0] === 2 && counts[1] === 2) return 'Two Pair';
    if (counts[0] === 2) return 'One Pair';
    return 'High Card';
}

function isSequential(values) {
    const valueOrder = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'];
    const sortedValues = values.sort((a, b) => valueOrder.indexOf(a) - valueOrder.indexOf(b));
    
    for (let i = 1; i < sortedValues.length; i++) {
        if (valueOrder.indexOf(sortedValues[i]) - valueOrder.indexOf(sortedValues[i-1]) !== 1) {
            return false;
        }
    }
    return true;
}

function updatePokerStats() {
    const hands = parseInt(document.getElementById('poker-hands').textContent) + 1;
    document.getElementById('poker-hands').textContent = hands;
}

function updatePokerChart(handTypes = null) {
    if (typeof Chart === 'undefined') return;
    
    const ctx = document.getElementById('poker-chart');
    if (!ctx) return;
    
    const labels = ['High Card', 'One Pair', 'Two Pair', 'Three of a Kind', 'Straight', 'Flush', 'Full House', 'Four of a Kind', 'Straight Flush'];
    const data = handTypes ? labels.map(label => handTypes[label] || 0) : labels.map(() => Math.random() * 100);
    
    const chartData = {
        labels: labels,
        datasets: [{
            data: data,
            backgroundColor: [
                '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', 
                '#9966FF', '#FF9F40', '#FF6384', '#C9CBCF', '#4BC0C0'
            ],
            borderWidth: 0
        }]
    };
    
    const config = {
        type: 'bar',
        data: chartData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    };
    
    try {
        if (window.pokerChart) {
            window.pokerChart.destroy();
        }
        window.pokerChart = new Chart(ctx, config);
    } catch (error) {
        console.log('Error updating poker chart:', error);
    }
}

function resetPoker() {
    document.getElementById('poker-hands').textContent = '0';
    document.getElementById('poker-hand').innerHTML = '';
    document.getElementById('poker-hand-type').textContent = '';
    updatePokerChart();
}

// Monty Hall problem
function initializeMontyHall() {
    const selectBtns = document.querySelectorAll('.door-btn');
    selectBtns.forEach(btn => {
        btn.addEventListener('click', () => selectDoor(parseInt(btn.dataset.door)));
    });
    
    const simulateBtn = document.getElementById('simulate-monty');
    if (simulateBtn) {
        simulateBtn.addEventListener('click', simulateMontyHall);
    }
    
    const resetBtn = document.getElementById('reset-monty');
    if (resetBtn) {
        resetBtn.addEventListener('click', resetMonty);
    }
}

let selectedDoor = null;
let revealedDoor = null;

function selectDoor(doorNumber) {
    selectedDoor = doorNumber;
    const carDoor = Math.floor(Math.random() * 3) + 1;
    
    // Reveal a goat door
    let revealDoor;
    do {
        revealDoor = Math.floor(Math.random() * 3) + 1;
    } while (revealDoor === selectedDoor || revealDoor === carDoor);
    
    revealedDoor = revealDoor;
    
    // Show the revealed door
    const revealBtn = document.querySelector(`[data-door="${revealDoor}"]`);
    if (revealBtn) {
        revealBtn.textContent = '🐐';
        revealBtn.disabled = true;
    }
    
    // Enable switch option
    document.getElementById('switch-option').style.display = 'block';
}

function playMontyHall(switchChoice) {
    if (selectedDoor === null) return;
    
    const carDoor = Math.floor(Math.random() * 3) + 1;
    let finalChoice = selectedDoor;
    
    if (switchChoice) {
        // Switch to the remaining door
        for (let i = 1; i <= 3; i++) {
            if (i !== selectedDoor && i !== revealedDoor) {
                finalChoice = i;
                break;
            }
        }
    }
    
    // Show all doors
    const doors = document.querySelectorAll('.door-btn');
    doors.forEach((door, index) => {
        const doorNumber = index + 1;
        if (doorNumber === carDoor) {
            door.textContent = '🚗';
        } else {
            door.textContent = '🐐';
        }
        door.disabled = true;
    });
    
    // Show result
    const result = finalChoice === carDoor ? 'Win!' : 'Lose!';
    document.getElementById('monty-result').textContent = result;
    
    // Update stats
    const wins = document.getElementById('monty-wins');
    const losses = document.getElementById('monty-losses');
    const games = document.getElementById('monty-games');
    
    games.textContent = parseInt(games.textContent) + 1;
    if (finalChoice === carDoor) {
        wins.textContent = parseInt(wins.textContent) + 1;
    } else {
        losses.textContent = parseInt(losses.textContent) + 1;
    }
    
    updateMontyStats();
}

function simulateMontyHall() {
    const games = 1000;
    let switchWins = 0;
    let stayWins = 0;
    
    for (let i = 0; i < games; i++) {
        const carDoor = Math.floor(Math.random() * 3) + 1;
        const initialChoice = Math.floor(Math.random() * 3) + 1;
        
        // Stay strategy
        if (initialChoice === carDoor) {
            stayWins++;
        }
        
        // Switch strategy
        let switchChoice;
        for (let j = 1; j <= 3; j++) {
            if (j !== initialChoice && j !== carDoor) {
                switchChoice = j;
                break;
            }
        }
        if (switchChoice === carDoor) {
            switchWins++;
        }
    }
    
    document.getElementById('monty-stay-win-rate').textContent = ((stayWins / games) * 100).toFixed(1) + '%';
    document.getElementById('monty-switch-win-rate').textContent = ((switchWins / games) * 100).toFixed(1) + '%';
}

function updateMontyStats() {
    const games = parseInt(document.getElementById('monty-games').textContent);
    const wins = parseInt(document.getElementById('monty-wins').textContent);
    const winRate = games > 0 ? ((wins / games) * 100).toFixed(1) : '0.0';
    document.getElementById('monty-win-rate').textContent = winRate + '%';
}

function resetMonty() {
    document.getElementById('monty-games').textContent = '0';
    document.getElementById('monty-wins').textContent = '0';
    document.getElementById('monty-losses').textContent = '0';
    document.getElementById('monty-win-rate').textContent = '0.0%';
    document.getElementById('monty-result').textContent = '';
    document.getElementById('switch-option').style.display = 'none';
    
    const doors = document.querySelectorAll('.door-btn');
    doors.forEach(door => {
        door.textContent = '🚪';
        door.disabled = false;
    });
    
    selectedDoor = null;
    revealedDoor = null;
}

// Kelly Criterion
function initializeKellyCriterion() {
    const calculateBtn = document.getElementById('calculate-kelly');
    if (calculateBtn) {
        calculateBtn.addEventListener('click', calculateKelly);
    }
    
    const resetBtn = document.getElementById('reset-kelly');
    if (resetBtn) {
        resetBtn.addEventListener('click', resetKelly);
    }
}

function calculateKelly() {
    const p = parseFloat(document.getElementById('win-probability').value);
    const b = parseFloat(document.getElementById('win-multiple').value);
    const a = parseFloat(document.getElementById('loss-fraction').value);
    
    if (isNaN(p) || isNaN(b) || isNaN(a)) {
        alert('Please enter valid numbers');
        return;
    }
    
    const kellyFraction = (p * b - (1 - p) * a) / b;
    const kellyPercent = (kellyFraction * 100).toFixed(2);
    
    document.getElementById('kelly-fraction').textContent = kellyPercent + '%';
    
    if (kellyFraction > 0) {
        document.getElementById('kelly-recommendation').textContent = `Bet ${kellyPercent}% of your bankroll`;
    } else {
        document.getElementById('kelly-recommendation').textContent = 'Do not bet (negative expected value)';
    }
    
    updateKellyChart(p, b, a);
}

function updateKellyChart(p, b, a) {
    if (typeof Chart === 'undefined') return;
    
    const ctx = document.getElementById('kelly-chart');
    if (!ctx) return;
    
    const fractions = [];
    const expectedValues = [];
    
    for (let f = 0; f <= 1; f += 0.01) {
        fractions.push(f * 100);
        const ev = p * Math.log(1 + f * b) + (1 - p) * Math.log(1 - f * a);
        expectedValues.push(ev);
    }
    
    const data = {
        labels: fractions,
        datasets: [{
            label: 'Expected Log Growth',
            data: expectedValues,
            borderColor: '#2196F3',
            backgroundColor: 'rgba(33, 150, 243, 0.1)',
            borderWidth: 2,
            fill: false
        }]
    };
    
    const config = {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Bet Fraction (%)'
                    },
                    grid: {
                        display: false
                    }
                }
            }
        }
    };
    
    try {
        if (window.kellyChart) {
            window.kellyChart.destroy();
        }
        window.kellyChart = new Chart(ctx, config);
    } catch (error) {
        console.log('Error updating Kelly chart:', error);
    }
}

function resetKelly() {
    document.getElementById('win-probability').value = '0.52';
    document.getElementById('win-multiple').value = '1.0';
    document.getElementById('loss-fraction').value = '1.0';
    document.getElementById('kelly-fraction').textContent = '-';
    document.getElementById('kelly-recommendation').textContent = '';
    
    const ctx = document.getElementById('kelly-chart');
    if (ctx && window.kellyChart) {
        window.kellyChart.destroy();
    }
}

// Risk of Ruin
function initializeRiskOfRuin() {
    const simulateBtn = document.getElementById('simulate-ruin');
    if (simulateBtn) {
        simulateBtn.addEventListener('click', simulateRiskOfRuin);
    }
    
    const resetBtn = document.getElementById('reset-ruin');
    if (resetBtn) {
        resetBtn.addEventListener('click', resetRiskOfRuin);
    }
}

function simulateRiskOfRuin() {
    const initialBankroll = parseFloat(document.getElementById('initial-bankroll').value);
    const betSize = parseFloat(document.getElementById('bet-size').value);
    const winRate = parseFloat(document.getElementById('win-rate').value);
    const simulations = 10000;
    
    if (isNaN(initialBankroll) || isNaN(betSize) || isNaN(winRate)) {
        alert('Please enter valid numbers');
        return;
    }
    
    let ruinCount = 0;
    let totalSessions = 0;
    let maxDrawdown = 0;
    
    for (let i = 0; i < simulations; i++) {
        let bankroll = initialBankroll;
        let sessions = 0;
        let peak = bankroll;
        
        while (bankroll > 0 && bankroll < initialBankroll * 3) {
            sessions++;
            if (Math.random() < winRate) {
                bankroll += betSize;
            } else {
                bankroll -= betSize;
            }
            
            if (bankroll > peak) {
                peak = bankroll;
            }
            
            const drawdown = (peak - bankroll) / peak;
            if (drawdown > maxDrawdown) {
                maxDrawdown = drawdown;
            }
        }
        
        if (bankroll <= 0) {
            ruinCount++;
        }
        totalSessions += sessions;
    }
    
    const ruinProbability = (ruinCount / simulations * 100).toFixed(2);
    const expectedSessions = Math.round(totalSessions / simulations);
    const maxDrawdownPercent = (maxDrawdown * 100).toFixed(1);
    
    document.getElementById('ruin-probability').textContent = ruinProbability + '%';
    document.getElementById('expected-sessions').textContent = expectedSessions;
    document.getElementById('max-drawdown').textContent = maxDrawdownPercent + '%';
    
    updateRuinChart(initialBankroll, betSize, winRate);
}

function updateRuinChart(initialBankroll, betSize, winRate) {
    if (typeof Chart === 'undefined') return;
    
    const ctx = document.getElementById('ruin-chart');
    if (!ctx) return;
    
    const sessions = [];
    const bankrolls = [];
    
    for (let session = 0; session <= 100; session++) {
        sessions.push(session);
        let bankroll = initialBankroll;
        
        for (let i = 0; i < session; i++) {
            if (Math.random() < winRate) {
                bankroll += betSize;
            } else {
                bankroll -= betSize;
            }
        }
        
        bankrolls.push(bankroll);
    }
    
    const data = {
        labels: sessions,
        datasets: [{
            label: 'Bankroll',
            data: bankrolls,
            borderColor: '#2196F3',
            backgroundColor: 'rgba(33, 150, 243, 0.1)',
            borderWidth: 2,
            fill: false
        }]
    };
    
    const config = {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Sessions'
                    },
                    grid: {
                        display: false
                    }
                }
            }
        }
    };
    
    try {
        if (window.ruinChart) {
            window.ruinChart.destroy();
        }
        window.ruinChart = new Chart(ctx, config);
    } catch (error) {
        console.log('Error updating ruin chart:', error);
    }
}

function resetRiskOfRuin() {
    document.getElementById('ruin-probability').textContent = '-';
    document.getElementById('expected-sessions').textContent = '-';
    document.getElementById('max-drawdown').textContent = '-';
    // Reset inputs to defaults
    document.getElementById('initial-bankroll').value = '1000';
    document.getElementById('bet-size').value = '100';
    document.getElementById('win-rate').value = '0.52';
    // Clear the chart
    const chartContainer = document.getElementById('ruin-chart');
    chartContainer.innerHTML = '';
} 