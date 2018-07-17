from os.path import join

from clint.textui import colored
from pandas import DataFrame

from data.local import get_pickle
from utils import filenames, STORAGE_PATH


def cleaner():
    fs1 = filenames('eod')
    fs3 = filenames('tiingo')
    syms = set.intersection(*map(set, [fs1, fs3]))
    print('Found %s common symbols' % len(syms))

    for s in syms:
        try:
            name = s.split('.')[0]
            d1 = get_pickle('eod', name)
            d3 = get_pickle('tiingo', name)

            if ((d1['Close'] - d3['close']).mean() > 0) | ((d1['Close'] - d3['close']).mean() < 0):
                diff1 = (d1['Close'] / d3['close']).mean()
                diff2 = (d1['Open'] / d3['open']).mean()
                diff3 = (d1['High'] / d3['high']).mean()
                diff4 = (d1['Low'] / d3['low']).mean()

                if (not ((diff1 > 1.01) | (diff1 < 0.99))) & (not ((diff2 > 1.01) | (diff2 < 0.99))) & \
                    (not ((diff3 > 1.01) | (diff3 < 0.99))) & (not ((diff4 > 1.01) | (diff4 < 0.99))):
                    if (len(d3.loc[d3['volume'] == 0]) == 0) & (len(d3.loc[d3['open'] == 0]) == 0) & \
                        (len(d3.loc[d3['high'] == 0]) == 0) & (len(d3.loc[d3['low'] == 0]) == 0) & \
                        (len(d3.loc[d3['close'] == 0]) == 0):

                        data = DataFrame()
                        data['Open'] = d3['open']
                        data['High'] = d3['high']
                        data['Low'] = d3['low']
                        data['Close'] = d3['close']
                        data['AdjClose'] = d3['adjClose']
                        data['Div'] = d3['divCash']
                        data['Split'] = d3['splitFactor']
                        data['Volume'] = d3['volume']
                        if len(data) > 1000:
                            data.to_pickle(join(STORAGE_PATH, 'accepted', s))
                            print(colored.green(name))
        except Exception as err:
            print(colored.red(err))