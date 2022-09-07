import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy.stats import pearsonr, spearmanr, linregress
from datetime import datetime, timedelta
import codecs
from scipy.stats.mstats import winsorize



# df = pd.read_csv(f'data/ts-volume.csv', converters={'time': lambda x: datetime.strptime(x, "%Y-%m-%d")},
#                  index_col=None)
# df.set_index('time', inplace=True)
def read_1m_cap_coins():
    coins_1m = []
    with codecs.open('coins-1m-cap.txt', 'r') as fin:
        for line in fin:
            coins_1m.append(line.strip())

    return coins_1m

coins_1m = read_1m_cap_coins()



df_close = pd.read_csv(f'data/ts-close.csv', converters={'time': lambda x: datetime.strptime(x, "%Y-%m-%d")},
                 index_col=None)
df_close.set_index('time', inplace=True)
df_close = df_close[coins_1m]


for c in df_close:
    if False:
        """
        Previous attempt to deal with outliers
        """
        # print('\n\n\n')
        # print(c)
        vals = df_close[c]

        # print(vals)
        # mask = ~np.isnan(vals)
        # vals = vals[mask]
        # print(mask)
        # print(np.min(vals), np.max(vals))

        winsorize(vals, limits=[0.1, 0.1], inplace=True, nan_policy='propagate')
        # winsorize(vals, limits=[0.01, 0.01], inplace=True, nan_policy='omit')

        # print('\n\n')
        # print(vals)
        # print(np.min(vals), np.max(vals))
        # input()

    p = 5.0
    assert(0.0 < p < 100.0)
    vals = df_close[c]
    mask = ~np.isnan(vals)
    if len(vals[mask]) == 0:
        continue

    v_low = np.percentile(vals[mask], p)
    v_high = np.percentile(vals[mask], 100-p)

    key = 'BTX-BITCORE'
    if c == key:
        print(v_low, v_high)
        print(vals)
        print(np.min(vals), np.max(vals))

    vals[vals < v_low] = v_low
    vals[vals > v_high] = v_high

    if c == key:
        print(vals)
        print(np.min(vals), np.max(vals))
        input()

# vals = df_close['BTX-BITCORE']
# print(vals[~np.isnan(vals)])
# print(np.max(vals))


df_mcap = pd.read_csv(f'data/ts-market_cap.csv', converters={'time': lambda x: datetime.strptime(x, "%Y-%m-%d")},
                 index_col=None)
df_mcap.set_index('time', inplace=True)
df_mcap = df_mcap[coins_1m]


df_returns = df_close.pct_change(7)

# df_sub = df_close[['ANC-ANONCOIN', 'BTC-BITCOIN', 'CBX-BULLION', 'DGC-DIGITALCOIN', 'TAG-TAGCOIN']]
# df_sub = df_close[['SXC-SEXCOIN']]

# print(df_sub.head(50))
# 13.01 -- first monday that has weekly returns since 2014
# t0 = datetime.strptime(f'2014-01-13', "%Y-%m-%d")



t0 = datetime.strptime(f'2014-01-08', "%Y-%m-%d")
# t0 += timedelta(days=2589)
print(t0)
# t0 = datetime.strptime(f'2014-01-09', "%Y-%m-%d")
# t0 = datetime.strptime(f'2014-05-01', "%Y-%m-%d")

profits = {'low': [], 'high': [], 'tot': []}
# while t0 <= datetime.strptime(f'2022-02-20', "%Y-%m-%d"):
while t0 <= datetime.strptime(f'2019-01-01', "%Y-%m-%d"):
    coins_t0_returns = set(df_returns.loc[t0].dropna().index)
    coins_t0_mcap = set(df_mcap.loc[t0].dropna().index)

    df_sub = df_mcap.loc[t0].dropna()
    coins_t0_mcap_1m = set(df_sub[df_sub >= 1e+6].index)

    df_sub = df_mcap.loc[t0 - timedelta(days=7)].dropna()
    coins_t1_mcap_1m = set(df_sub[df_sub >= 1e+6].index)

    coins_t0 = coins_t0_mcap & coins_t0_returns & coins_t0_mcap_1m & coins_t1_mcap_1m

    mcap_vals = df_mcap.loc[t0][list(coins_t0)]

    low = np.quantile(mcap_vals, 0.2)
    high = np.quantile(mcap_vals, 0.8)

    portfolio_low = list(mcap_vals[mcap_vals <= low].index)
    portfolio_high = list(mcap_vals[mcap_vals >= high].index)

    # #TODO
    # if t0 > datetime.strptime(f'2014-01-08', "%Y-%m-%d"):
    #     print(df_returns.loc[t0][portfolio_low].sort_values())
    #     print(df_returns.loc[t0][portfolio_high].sort_values())
    #     input()

    weekly_profit_low = np.sum(df_returns.loc[t0][portfolio_low])
    weekly_profit_high = -np.sum(df_returns.loc[t0][portfolio_high])
    weekly_profit = weekly_profit_high + weekly_profit_low

    # print(weekly_profit)
    profits['low'].append(weekly_profit_low)
    profits['high'].append(weekly_profit_high)
    profits['tot'].append(weekly_profit)

    # t0 += timedelta(days=7)
    t0 += timedelta(days=1)

    # break



fig, ax = plt.subplots(figsize=(6,6))

ax.plot(profits['low'], '-', label=f'low, m={np.mean(profits["low"]):.3f}')
ax.plot(profits['high'], '-', label=f'high, m={np.mean(profits["high"]):.3f}')
ax.plot(profits['tot'], '-', label=f'total, m={np.mean(profits["tot"]):.3f}')
ax.grid(alpha=0.4, linestyle='--', linewidth=0.2, color='black')
ax.legend(loc='best')
ax.set_xlabel('Time (days)')
ax.set_ylabel('Profit')
plt.savefig(f'results/market_cap-profits.png', dpi=400, bbox_inches='tight')
plt.show()








# print(df_returns.head(50))


# t0 = datetime.strptime(f'2014-01-07', "%Y-%m-%d")
# t1 = t0 + timedelta(days=7)
# print(t1)
#
# vals = df_mcap.loc[t0].dropna()
# print(vals.index)
#
# vals_1 = df_mcap.loc[t1].dropna()
# print(vals_1.index)
#
# print(set(vals_1.index))


#
# low = np.quantile(vals, 0.2)
# high = np.quantile(vals, 0.8)
#
# print(low, high)
# print(vals[vals <= low])
# # q1 = vals[vals <= low].index()
# print(list(vals[vals <= low].index))
#
#
# portfolio = {}

















