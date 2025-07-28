# Genetic-Algorithm-Trading-Strategy-Optimizer
This project implements a Genetic Algorithm (GA) to optimize parameters of technical trading strategies. It systematically evolves combinations of indicator parameters (like RSI, MA, ATR, etc.) to maximize performance.

## Why Use Genetic Algorithms for Strategy Optimization?
Optimizing trading strategies with multiple technical indicators quickly becomes a combinatorial challenge. For instance, even modest parameter ranges across just 8 variables can result in billions of possible combinations. Exhaustively testing all of them (grid search) is computationally expensive and inefficient.

This project demonstrates how a Genetic Algorithm (GA) can efficiently explore this space to find high-performing configurations, without needing to test every possibility.

## Chromosome Design and Parameter Ranges

Each individual strategy is represented as an **8-gene chromosome**, where each gene corresponds to a strategy parameter. These genes are initialized and evolved over generations.

**Parameter ranges:**

Description               Range / Options             

MA Type                -->   0=SMA, 1=EMA, 2=WMA, 3=TMA  
Fast MA Length         -->   5 to 30        
Slow MA Length         -->   20 to 100      
RSI Length             -->   5 to 30        
RSI Oversold Threshold -->   10 to 40       
ATR Period             -->   5 to 30        
Stop Loss Multiplier   -->   0.5 to 5.0       
Take Profit Multiplier -->   0.5 to 5.0       

With these ranges, the total number of valid combinations is **in the tens of billions**, making brute-force grid search computationally unfeasible.

## About This Project

- This project demonstrates how genetic algorithms can be applied to optimize a multi-indicator trading strategy. It is a conceptual illustration, not an attempt to create a high-frequency or high-performance production optimizer.
- The fitness function is inspired by the objective functions described in Kaufman’s book, encouraging stable and consistent returns.
- The data used resulted in 12 in-sample and 2 out-of-sample trades — far too few for real-world validation.
- The code prioritizes clarity and modular structure over execution speed or memory efficiency.
- This is not a ready-to-use trading system, but a demonstration of the GA-based optimization framework.
