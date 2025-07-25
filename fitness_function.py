
import yfinance as yf
import numpy as np
import pandas as pd
from math import sqrt

from indicator_functions import sma, ema, wma, tma, rsi, atr
from ga_config import GENE_KEYS


# Load price data
data = yf.download("^NSEI", start="2007-01-01", end="2020-12-31", progress=False)
data.columns = [col[0] for col in data.columns]
data.dropna(inplace=True)


# Apply indicators based on chromosome
def apply_indicators(df, chromosome):
    gene = dict(zip(GENE_KEYS, chromosome))
    price = df['Close']

    # MA logic
    if gene['ma_type'] == 0:
        df['fast'] = sma(price, gene['fast_ma'])
        df['slow'] = sma(price, gene['slow_ma'])
    elif gene['ma_type'] == 1:
        df['fast'] = ema(price, gene['fast_ma'])
        df['slow'] = ema(price, gene['slow_ma'])
    elif gene['ma_type'] == 2:
        df['fast'] = wma(price, gene['fast_ma'])
        df['slow'] = wma(price, gene['slow_ma'])
    elif gene['ma_type'] == 3:
        df['fast'] = tma(price, gene['fast_ma'])
        df['slow'] = tma(price, gene['slow_ma'])

    # RSI & ATR
    df['rsi'] = rsi(price, gene['rsi_length'])
    df['atr'] = atr(df, gene['atr_period'])

    return df


def backtest_and_metrics(df, chromosome):
    df = df.copy().reset_index(drop=True)
    equity = 1000000
    equity_curve = [equity]
    returns = []
    net_profit = gross_profit = gross_loss = 0
    num_trades = 0
    num_wins = 0
    position = None
    peak_equity = equity
    max_drawdown = 0

    gene = dict(zip(GENE_KEYS, chromosome))
    sl_mult = gene['sl_multiplier']
    tp_mult = gene['tp_multiplier']

    for i in range(1, len(df)):
        row = df.loc[i]
        prev = df.loc[i - 1]

        if position is None:
            if prev['fast'] < prev['slow'] and row['fast'] > row['slow']:
                if row['rsi'] < gene['rsi_oversold']:
                    entry = row['Close']
                    position = {
                        'entry_price': entry,
                        'atr': row['atr'],
                        'qty': equity // entry
                    }
                    position['sl'] = entry - sl_mult * position['atr']
                    position['tp'] = entry + tp_mult * position['atr']
                    continue

        if position:
            low, high = row['Low'], row['High']
            exit_price = None
            if low <= position['sl']:
                exit_price = position['sl']
            elif high >= position['tp']:
                exit_price = position['tp']

            if exit_price:
                profit = (exit_price - position['entry_price']) * position['qty']
                equity += profit
                equity_curve.append(equity)
                ret = profit / (position['entry_price'] * position['qty'])
                returns.append(ret)
                net_profit += profit
                if profit > 0:
                    gross_profit += profit
                    num_wins += 1
                else:
                    gross_loss += abs(profit)
                num_trades += 1
                peak_equity = max(peak_equity, equity)
                drawdown = (peak_equity - equity) / peak_equity
                max_drawdown = max(max_drawdown, drawdown)
                position = None

    if position:
        exit_price = df.loc[len(df) - 1]['Close']
        profit = (exit_price - position['entry_price']) * position['qty']
        equity += profit
        equity_curve.append(equity)
        ret = profit / (position['entry_price'] * position['qty'])
        returns.append(ret)
        net_profit += profit
        if profit > 0:
            gross_profit += profit
            num_wins += 1
        else:
            gross_loss += abs(profit)
        num_trades += 1
        peak_equity = max(peak_equity, equity)
        drawdown = (peak_equity - equity) / peak_equity
        max_drawdown = max(max_drawdown, drawdown)

    duration_days = len(df) / 252
    cagr = (equity / 1000000) ** (1 / duration_days) - 1 if duration_days > 0 else 0
    if returns and np.std(returns) != 0:
        sharpe = (np.mean(returns) / np.std(returns)) * sqrt(252)
    else:
        sharpe = 0
    win_rate = num_wins / num_trades if num_trades > 0 else 0

    return {
        'net_profit': net_profit,
        'gross_profit': gross_profit,
        'gross_loss': gross_loss,
        'num_trades': num_trades,
        'returns': returns,
        'equity_curve': equity_curve,
        'cagr': cagr,
        'sharpe': sharpe,
        'max_drawdown': max_drawdown,
        'win_rate': win_rate,
        'final_equity': equity
    }


# FITNESS FUNCTION
def fitness(chromosome):
    df = data.copy()
    df = apply_indicators(df.copy(), chromosome)
    stats = backtest_and_metrics(df, chromosome)

    net = stats['net_profit']
    gp = stats['gross_profit']
    gl = stats['gross_loss']
    nt = stats['num_trades']

    if nt == 0 or gl == 0:
        return 0

    ppt = net / nt
    rank = ppt * (1 - 1 / np.sqrt(nt)) * (gp / gl)
    return rank
