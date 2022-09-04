import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr, linregress
from datetime import datetime





def analyze_yearly_coins():
    # df = pd.read_csv(f'FILTER/data-filtered.csv', converters={'time': lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S")})
    df = pd.read_csv(f'data/CoinpapricaDaily-filtered.csv', converters={'time': lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S")})
    coins = list(set(df['first_currency']))
    print(f'total coins: {len(coins)}')

    years = list(range(2014, 2022))
    n_coins = []
    for y in years:
        t0 = datetime.strptime(f'{y}-01-01 23:59:59', "%Y-%m-%d %H:%M:%S")
        df_sub = df[df['time'] == t0]
        coins = list(set(df_sub['first_currency']))

        n_coins.append(len(coins))

        # print(f'coins in {y}: {len(coins)}')

    fig, ax = plt.subplots(figsize=(6,6))

    ax.plot(years, n_coins, 'o-')
    ax.grid(alpha=0.4, linestyle='--', linewidth=0.2, color='black')
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of coins')
    plt.savefig(f'results/N-coins-yearly.png', dpi=400, bbox_inches='tight')
    plt.show()



analyze_yearly_coins()










