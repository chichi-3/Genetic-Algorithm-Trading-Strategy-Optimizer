# Genetic-Algorithm-Trading-Strategy-Optimizer
This project implements a Genetic Algorithm (GA) to optimize parameters of technical trading strategies. It systematically evolves combinations of indicator parameters (like RSI, MA, ATR, etc.) to maximize performance.

## Why Use Genetic Algorithms for Strategy Optimization?
Optimizing trading strategies with multiple technical indicators quickly becomes a combinatorial challenge. For instance, even modest parameter ranges across just 8 variables can result in billions of possible combinations. Exhaustively testing all of them (grid search) is computationally expensive and inefficient.

This project demonstrates how a Genetic Algorithm (GA) can efficiently explore this space to find high-performing configurations, without needing to test every possibility.

## Chromosome Design and Parameter Ranges

Each individual strategy is represented as an **8-gene chromosome**, where each gene corresponds to a strategy parameter. These genes are initialized and evolved over generations.

**Parameter ranges:**

Description               Range / Options             

- MA Type                -->   0=SMA, 1=EMA, 2=WMA, 3=TMA
- Fast MA Length         -->   5 to 30
- Slow MA Length         -->   20 to 100
- RSI Length             -->   5 to 30
- RSI Oversold Threshold -->   10 to 40
- ATR Period             -->   5 to 30
- Stop Loss Multiplier   -->   0.5 to 5.0
- Take Profit Multiplier -->   0.5 to 5.0       

With these ranges, the total number of valid combinations is **in the tens of billions**, making brute-force grid search computationally unfeasible.

## Genetic Algorithm Process

#### 1. Initialization
- A large initial population (1,000–5,000 chromosomes) is randomly generated.
- Each chromosome is an 8-gene string, representing one unique strategy configuration.
- This population represents the first generation of strategies.

#### 2. Evaluation & Propagation
- Each chromosome is evaluated using a fitness function (e.g., Information Ratio).
- Chromosomes are ranked by fitness in descending order.
- Top-performing chromosomes are copied multiple times to form the core of the next generation.
- This step retains and promotes the fittest solutions for further evolution.

#### 3. Mating (Crossover)
- Two parent chromosomes are randomly selected from the pool.
- A random crossover point (1 to 7) divides their genes into two segments.
- Genes before and after the crossover point are swapped between parents to produce two new offspring.
- This continues until 10–15% of the new generation is created through crossover.

#### 4. Mutation
- A subset of chromosomes is randomly chosen for mutation.
- One gene in each selected chromosome is randomly replaced with a new valid value from its range.
- Mutation is applied to around 10% of the population to preserve genetic diversity and explore new regions of the solution space.

#### 5. Convergence & Repetition
- After each generation, the top-performing chromosome and its fitness score are saved.
- The GA continues for a fixed number of generations (typically around 100).
- To improve robustness, the entire GA process is repeated up to 5 times with different random seeds.
- The best chromosome from all runs is selected as the final solution.

Once the best-performing parameter set is found using in-sample data, it is tested on a separate out-of-sample dataset. This helps verify the strategy's robustness and ensures it has not been overfitted. Performance on OOS data confirms whether the solution generalizes well beyond the training window.

## About This Project

- This project demonstrates how genetic algorithms can be applied to optimize a multi-indicator trading strategy. It is a conceptual illustration, not an attempt to create a high-frequency or high-performance production optimizer.
- The fitness function is inspired by the objective functions described in Perry J Kaufman’s book, Trading Systems and Methods.
- The data used resulted in 12 in-sample and 2 out-of-sample trades — far too few for real-world validation.
- The code prioritizes clarity over execution speed or memory efficiency.
- This is not a ready-to-use trading system, but a demonstration of the GA-based optimization framework.

### Note
This is a learning project and not a recommendation to trade with the strategies produced. The results are based on limited sample data and are not suitable for real-money use.
