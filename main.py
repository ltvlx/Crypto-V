import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr, linregress



df = pd.read_csv(f'test_crypto.csv')

# print(df)


currencies = ['ETH', 'LTC', 'XRP', 'ETC', 'STR', 'DASH', 'SC', 'XMR', 'XEM', 'BTC']


values = {key: np.array(df[key]) for key in currencies}
# returns = {key: np.ediff1d(values[key]) for key in currencies}
# print(returns['ETH'])

returns7 = {}
# for key in values:
for key in ['ETH']:
    r = []
    nums = values[key]
    i = 0
    while i < 992:
    # for i in range(0, 993, 7):
        r.append(nums[i+6] - nums[i])
        print(i, r[-1])
        # print(nums[i], nums[i+6])
        # print()
        i += 7

    returns7[key] = np.array(r)

# print(returns7)





    # for k1 in currencies:
#     for k2 in currencies:
#         if k1 == k2:
#             continue
#
#         nums1 = data[k1]
#         nums2 = data[k2]




        # c, p = spearmanr(nums1, nums2)
        # c, p = pearsonr(nums1, nums2)

#         print(f'{k1:5s}, {k2:5s}: {c:.4f}, {p:.4e}')
#
#
#
#
#
# fig, ax = plt.subplots(figsize=(8,4))
# for key in currencies:
#     nums = data[key]
#     nums = nums / np.mean(nums)
#     ax.plot(nums)
#
# plt.show()
#


