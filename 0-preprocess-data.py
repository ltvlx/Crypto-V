import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr, linregress
from datetime import datetime, timedelta
import json
import codecs




def filter_coins():
    """
    Going through all coins and leaving those coins
    that don't have enough capitalization and volume
    """
    def check_cap_volume(df_sub):
        """
        A function that receives subset of dataframe with one coin;
        Then, finds the first date when:
            market_cap >= 1e+6
            volume > 0
        And returns a subset of the database after this date
        If the coin has no such date, return None and ignore it
        """
        df_sub.sort_values('time', ascending=True, inplace=True)

        for i, row in df_sub.iterrows():
            if row['volume'] != np.nan and row['volume'] > 0.0 and \
                row['market_cap'] != np.nan and row['market_cap'] >= 1e+6:
                return df_sub[df_sub['time'] >= row['time']]

        return None

    df = pd.read_csv(f'data/CoinpapricaDaily.csv', converters={'time': int})
    coins = list(set(df['first_currency']))

    time = (df['time'] / 1000).astype(int)
    df['time'] = np.array(list(map(datetime.utcfromtimestamp, time)))

    df = df[['first_currency', 'time', 'open', 'high', 'low',
               'close', 'volume', 'market_cap']]

    dataframes = []
    failed = []
    i = 0
    for c_name in coins:
        print(i, c_name, f'{100*i/len(coins):.4f}%', flush=True)
        df_out = check_cap_volume(pd.DataFrame(df[df['first_currency'] == c_name]))
        if df_out is not None:
            dataframes.append(df_out)
        else:
            failed.append(c_name)
        i += 1

        # if i % 1000 == 0:
        #     print(f'{len(failed)} failed out of {i}')
        #     pd.concat(dataframes, ignore_index=True).to_csv(f'data-filtered-{i:04d}.csv', index=False)
        #     json.dump({'failed': failed}, codecs.open(f'failed-{i:04d}.json', 'w'), indent=2)

    pd.concat(dataframes, ignore_index=True).to_csv('data/CoinpapricaDaily-filtered.csv', index=False)
    json.dump({'failed': failed}, codecs.open(f'data/failed.json', 'w'), indent=2)


def transpose_dataframe():
    """
    Transposing the filtered dataframe and splitting it into separate,
    such that the new have dates as rows and coins as columns

    separate tables are generated for high, close, volume, and market_cap
    """
    df = pd.read_csv(f'data/CoinpapricaDaily-filtered.csv', converters={'time': lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S")})

    coins = list(set(df['first_currency']))

    # df_sub = df[df['first_currency'].isin(['NEO-NEO', 'BTC-BITCOIN'])]
    # print(df_sub)
    # df_reversed = df_sub.pivot(index='time', columns=['first_currency'], values=['close'])

    for key in ['high','low', 'close', 'volume', 'market_cap']:
    # for key in ['high']:
        df_reversed = df.pivot(index='time', columns=['first_currency'], values=[key])
        df_reversed.sort_index(inplace=True)
        # mask = np.array(df_reversed['time'] >= datetime.strptime(f'2014-01-01 23:59:59', "%Y-%m-%d %H:%M:%S"))
        mask = df_reversed.index >= datetime.strptime(f'2014-01-01 23:59:59', "%Y-%m-%d %H:%M:%S")
        df_reversed = df_reversed[mask]
        time_days = list(map(lambda x: x.strftime("%Y-%m-%d"), df_reversed.index))
        df_reversed.index = time_days

        # print(df_reversed[key])
        df_reversed[key].to_csv(f'data/ts-{key}.csv', index=True, index_label='time')





columns = ['first_currency','time','open','high','low','close','volume','market_cap']

# filter_coins()
# transpose_dataframe()




def detect_outliers():
    df_close = pd.read_csv(f'data/ts-close.csv', converters={'time': lambda x: datetime.strptime(x, "%Y-%m-%d")},
                           index_col=None)
    df_close.set_index('time', inplace=True)

    df_returns = df_close.pct_change(7)

    data = {'coin': [], 'returns min': [], 'returns max': []}
    for c in df_returns.columns:
        # print(f'{c:30s};{np.max(df_returns[c])};{np.min(df_returns[c])}')
        data['coin'].append(c)
        data['returns min'].append(np.min(df_returns[c]))
        data['returns max'].append(np.max(df_returns[c]))

    # pd.DataFrame(data).to_excel('data/coins-outliers.xlsx', sheet_name='Sheet0')
    # pd.DataFrame(data).to_csv('data/coins-outliers.csv')




detect_outliers()



