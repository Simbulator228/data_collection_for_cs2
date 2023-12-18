import pandas as pd
import matplotlib.pyplot as plt


pd.set_option('display.max_rows', None)
dt = pd.read_csv('result.csv')
dt = dt.sort_values(by='spread')
dt['mk_price'] = dt['mk_price']*0.9025
# dt['mk_price'].plot(x='x', y='y',kind='hist', bins=20)
# plt.show()


# diction = {
#     'Row_1':[1,2,3],
#     'Row_2':[4,5,6],
#     'Row_3':[1,5,3]
# }
# col = ['kek', 'mek', 'shpek']
# row = ['m', 'p1', 'p2']
# df2 = pd.DataFrame.from_dict(diction, orient='index', columns=col)
# print(df2['kek'].value_counts())


# print(df2)
# df = pd.read_csv('data/skins_market_21_10_2023-15:56:13.csv')
# print(dt[['name.1','buff_price','steam_price','spread','sales']])

print(dt)
