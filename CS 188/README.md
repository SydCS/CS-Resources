https://inst.eecs.berkeley.edu/~cs188/

# Search

## Uninformed Search

state space, successor function, start state & goal test $\Longrightarrow$ solution

_Depth-First Search_

_Breadth-First Search_

_Uniform Cost Search_

## Informed Search

**heuristic**: state $\mapsto$ how close it is to the goal

_Greedy_

_A\*_ = UCS + Greedy

Admissibility: estimated cost $\leq$ actual cost to the goal

_A\*_ with admissible heuristic $\Rightarrow$ optimality

---

Graph Search

Consistency:

## Constraint Satisfaction Problems

Variables Domains + Constraints $\Rightarrow$ Solution

Backtracking = DFS + variable ordering + fail on violation

- Filtering: Forward Checking (Constraint Propagation); Arc Consistency (AC-3)
- Ordering: Minimum Remaining Values; Least Constraining Value
- Structure:

Iterative Improvement

## Local Search

Hill Climbing

Simulated Annealing

Genetic Algorithms

## Games

Minimax

Expectimax

# Logic

## First Order Logic

# Probability

## Bayes Nets

Directed Acyclic Graph + Conditional Probability Table

Conditional Independence

$$
P ( X_{1},..., X_{n} ) = \prod_{i} P ( X_{i} \mid \text{Parents} ( X_{i} ) )
$$

> Each node is conditionally independent of its non-descendants given its parents.

---

chain, fork, collider

_D-Separation_

---

Variable Elimination

---

Prior sampling

Rejection sampling

Likelihood weighting

Gibbs sampling

_Markov Chain Monte Carlo_

## Markov Chains

> future is independent of the past given the present.

stationary distribution

## Hidden Markov Models

belief state

---

most likely explanation = shortest path

_Viterbi algorithm_:

---

Particle Filtering

## Dynamic Bayes Nets

# Machine Learning

## Naïve Bayes

(Bayes Net)

---

Parameter Estimation:

_Maximum Likelihood Estimation_: i.i.d. + uniform prior

\+ Laplace smoothing

## Perceptron

## Linear Regression

## Logistic Regression

## Neural Nerwork

# Reinforcement Learning

## Markov Decision Process

**Markov Decision Process**:

- states $s \in S$
- actions $a \in A$
- transition function $P(s^\prime \mid s,a)$
- reward function $R(s, a, s’)$
- start state
- terminal state

policy $\pi(a|s)$

discount $\gamma$

---

V-Value $V^*(s)$

$$
V^{*} ( s ) = \mathop{\max}\limits_{a} \sum_{s^{\prime}} T ( s, a, s^{\prime} ) \, \left[ R ( s, a, s^{\prime} )+\gamma\, V^{*} ( s^{\prime} ) \right]
$$

Q-value $Q^*(s,a)$

$$
Q^{*} ( s, a )=\sum_{s^{\prime}} T ( s, a, s^{\prime} ) \, \Big[ \, R ( s, a, s^{\prime} )+\gamma\operatorname* {m a x}_{a^{\prime}} Q^{*} ( s^{\prime}, a^{\prime} ) \Big]
$$

optimal policy

$$
\pi^{*} ( s ) = \mathop{\arg\max}\limits_{a} Q^{*} ( s, a )
$$

**Value Iteration**

**Policy Iteration**:

- Evaluation: For fixed current policy, find values with policy evaluation
- Improvement: For fixed values, get a better policy using policy extraction

## Bandits

Exploration & Exploitation

## Reinforcement Learning

- Model-Based

- Model-Free
  - Value learning
    - Monte-Carlo evaluation
    - Temporal Difference Learning
  - Q-learning
