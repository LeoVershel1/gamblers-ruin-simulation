import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from ruin import (
    gambler_ruin,
    gambler_ruin_generalized,
    gambler_ruin_with_credit,
    gambler_ruin_with_changing_bets,
    gambler_ruin_with_max_bets,
)

st.title("Gambler's Ruin Simulation")

st.write("""
This simulation explores the probability of a gambler either achieving their goal amount
or going broke under different conditions. Select the variables you want to include
in the simulation.
""")

# Variable descriptions
variable_descriptions = {
    'p': "Probability of winning each bet (default: 0.5)",
    'q': "Payout ratio when winning (default: 2.0)",
    'j': "Size of each bet (default: 1)",
    'i': "Initial amount of money",
    'n': "Goal amount to win",
    'k': "Credit line (amount that can be borrowed)",
    'm': "Maximum bet allowed per game"
}

# Create columns for better layout
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Select Variables")
    # Base variables are selected by default
    use_p = st.checkbox("Use p", value=True)
    use_q = st.checkbox("Use q", value=True)
    use_j = st.checkbox("Use j", value=True)
    use_i = st.checkbox("Use i", value=True)
    use_n = st.checkbox("Use n", value=True)
    use_k = st.checkbox("Use k", value=False)
    use_m = st.checkbox("Use m", value=False)

with col2:
    st.subheader("Variable Values")
    # Input fields for each variable
    p = st.number_input("p: " + variable_descriptions['p'], min_value=0.0, max_value=1.0, value=0.5, step=0.1) if use_p else 0.5
    q = st.number_input("q: " + variable_descriptions['q'], min_value=1.0, value=2.0, step=0.5) if use_q else 2.0
    j = st.number_input("j: " + variable_descriptions['j'], min_value=1, value=1) if use_j else 1
    i = st.number_input("i: " + variable_descriptions['i'], min_value=1, value=10) if use_i else 10
    n = st.number_input("n: " + variable_descriptions['n'], min_value=i+1, value=20) if use_n else 20
    k = st.number_input("k: " + variable_descriptions['k'], min_value=0, value=5) if use_k else 0
    m = st.number_input("m: " + variable_descriptions['m'], min_value=j, value=10) if use_m else float('inf')

# Number of trials
trials = st.slider("Number of simulation trials", min_value=1000, max_value=100000, value=10000, step=1000)

if st.button("Run Simulation"):
    # Determine which function to use based on selected variables
    if use_k and use_m:
        result = gambler_ruin_with_max_bets(p, q, j, i, n, k, m, trials)
        method = "with maximum bets and credit line"
    elif use_k:
        result = gambler_ruin_with_credit(p, q, j, i, n, k, trials)
        method = "with credit line"
    elif all([use_p, use_q, use_j, use_i, use_n]) and not (use_k or use_m):
        result = gambler_ruin_generalized(p, q, j, i, n, trials)
        method = "generalized"
    else:
        result = gambler_ruin(i, n, trials)
        method = "basic"

    # Display results
    st.subheader("Simulation Results")
    st.write(f"Probability of reaching the goal using {method} simulation: {result:.2%}")

    # Create visualization
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create a simple bar chart showing win vs loss probability
    probabilities = [result, 1 - result]
    labels = ['Win', 'Loss']
    colors = ['green', 'red']
    
    ax.bar(labels, probabilities, color=colors)
    ax.set_ylim(0, 1)
    ax.set_ylabel('Probability')
    ax.set_title(f"Gambler's Ruin Simulation Results ({method})")
    
    # Add percentage labels on top of bars
    for i, prob in enumerate(probabilities):
        ax.text(i, prob, f'{prob:.1%}', ha='center', va='bottom')
    
    st.pyplot(fig)

    # Additional statistics
    st.subheader("Additional Information")
    st.write(f"Expected value per bet: {(p * q * j) - ((1-p) * j):.2f}")
    if use_k:
        st.write(f"Maximum possible loss: {k + i}")
    st.write(f"Required wins to reach goal: {((n - i) / (q * j)):.1f}")
