"""
Problem 1

The gambler's ruin is classic problem in statistics. It has the following characteristics
1. A gambler plays a fair game with a 1/2 chance of winning
2. Winning causes them to double their money
3. The minimum bet is 1 dollar
4. The gambler starts with i and will continue until either they have 0 dollars or achieve
their goal of n dollars

Write a simulation to find the probability of them either winning or going broke.
"""

import random

def gambler_ruin(i, n, trials=10000):
    """
    Simulate the gambler's ruin problem.

    Args:
        i (int): The initial amount of money the gambler has.
        n (int): The goal amount of money the gambler wants to achieve.

    Returns:
        float: The probability of the gambler either winning or going broke.
    """    
    # Initialize the number of wins
    wins = 0    
    
    # Simulate the gambler's ruin problem
    for _ in range(trials):
        current_money = i
        while current_money > 0 and current_money < n:
            if random.random() < 0.5:
                current_money *= 2
            else:
                current_money -= 1

        if current_money == n:
            wins += 1

    return wins / trials


"""
Generalize this problem. Use variables to generalize the following
(a) Their chances of winning p
(b) The payout ratio of the game q
(c) The size of their bet j
(d) Their starting amount i
(e) Their goal amount n
"""

def gambler_ruin_generalized(p, q, j, i, n, trials=10000):
    """
    Simulate the gambler's ruin problem.
    """
    # Initialize the number of wins
    wins = 0    
    
    # Simulate the gambler's ruin problem
    for _ in range(trials):
        current_money = i
        while current_money > 0 and current_money < n:
            if random.random() < p:
                current_money += q * j  
            else:
                current_money -= j

        if current_money == n:
            wins += 1

    return wins / trials


"""
The gambler now has a line of credit and are able to take out a loan up to an amount
k if they hit 0.
"""

def gambler_ruin_with_credit(p, q, j, i, n, k, trials=10000):
    """
    Simulate the gambler's ruin problem.
    """
    # Initialize the number of wins
    wins = 0
    n_changed = False
    # Simulate the gambler's ruin problem
    for _ in range(trials):
        current_money = i
        while current_money > 0-k and current_money < n:
            if random.random() < p:
                current_money += q * j
            else:
                current_money -= j
                if current_money < 0 and n_changed == False:
                    n = n + k
                    n_changed = True

        if current_money == n:
            wins += 1

    return wins / trials    


"""
The gambler is now able to change their bets. To keep things simple, if they are on
a losing streak they will increase their bet by a factor of 1/p. So if p = 1/2 they will
double their bet for each degree of losing streak they have
"""

def gambler_ruin_with_changing_bets(p, q, j, i, n, k, trials=10000):
    # Initialize the number of wins
    wins = 0
    losing_streak = 0
    true_j = j
    n_changed = False
    # Simulate the gambler's ruin problem
    for _ in range(trials):
        current_money = i
        while current_money > 0 and current_money < n:
            if random.random() < p:
                current_money += q * j
                j = true_j
            else:
                current_money -= j
                j = j * (1/p)
                if current_money < 0 and n_changed == False:
                    n = n + k
                    n_changed = True

        if current_money == n:
            wins += 1   

    return wins / trials


"""
The house has implement a maximum bet per table. So the gambler cannot place a
bet larger than m dollars.
"""

def gambler_ruin_with_max_bets(p, q, j, i, n, k, m, trials=10000):
    # Initialize the number of wins
    wins = 0
    losing_streak = 0
    true_j = j
    n_changed = False
    # Simulate the gambler's ruin problem
    for _ in range(trials):
        current_money = i
        while current_money > 0 and current_money < n:
            if random.random() < p:
                current_money += q * j
                j = true_j
            else:
                current_money -= j
                j = min(m, j * (1/p))
                if current_money < 0 and n_changed == False:
                    n = n + k
                    n_changed = True

        if current_money == n:
            wins += 1   

    return wins / trials



