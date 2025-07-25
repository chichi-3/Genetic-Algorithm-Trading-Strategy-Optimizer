
# Genetic Algorithm Configuration File

# Gene Parameter Ranges (G1 to G8)
PARAM_RANGES = {
    "ma_type": [0, 1, 2, 3],                  # G1: MA Type (0=SMA, 1=EMA, 2=WMA, 3=TMA)
    "fast_ma": (5, 30),                       # G2: Fast MA length
    "slow_ma": (20, 100),                     # G3: Slow MA length
    "rsi_length": (5, 30),                    # G4: RSI length
    "rsi_oversold": (10, 40),                 # G5: RSI oversold threshold
    "atr_period": (5, 30),                    # G6: ATR length
    "sl_multiplier": (0.5, 5.0),              # G7: Stop Loss multiplier
    "tp_multiplier": (0.5, 5.0)               # G8: Take Profit multiplier
}

# Gene keys
GENE_KEYS = [
    "ma_type",
    "fast_ma",
    "slow_ma",
    "rsi_length",
    "rsi_oversold",
    "atr_period",
    "sl_multiplier",
    "tp_multiplier"
]

# GA Hyperparameters
POPULATION_SIZE = 1000
NUM_GENERATIONS = 100
MUTATION_RATE = 0.10     # 10% of population will mutate 1 gene
CROSSOVER_RATE = 0.10    # 10% of population will be created via crossover
ELITE_PERCENT = 0.05     # 5% of population will be kept as elites
SURVIVOR_PERCENT = 0.80
