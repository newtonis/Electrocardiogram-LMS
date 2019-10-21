

import wfdb
# data, metadata = wfdb.rdsamp('data/100', sampto=3000)
signals, metadata = wfdb.rdsamp(record_name='data/100', sampto=3000)
# annotation = wfdb.rdann(record_name='data/100', 'atr', sampto=3000)

signal_0 = signals[:, 0]
signal_1 = signals[:, 1]

all_signals = [i for i in range(10)]
