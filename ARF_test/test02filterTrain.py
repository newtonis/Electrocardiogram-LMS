from get_data import all_signals
import matplotlib.pyplot as plt
from getPeaks import getPeaks
from scipy.signal import detrend
from filterARF import filterARF
import numpy as np

### revisamos el funcionamiento de getPeaks

## usamos la 202

fs = 360
timespan = 400
time_cycle = 1.4

señal = all_signals["202"]["upper"][:timespan*fs]
t = np.arange(len(señal)) / fs

#errores = all_signals["202"]["anomalies"].keys()

señal = detrend(señal)

peaks = getPeaks(señal, fs, time_cycle / 2, time_cycle / 10)

myFilterARF = filterARF(500, 0.1)
filtered, error = myFilterARF.train(peaks, señal)

fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, sharex=True)

ax1.plot(señal)

#for ei in errores:
#    ax1.plot([ei], [0], 'bo')

ax2.plot(peaks)

ax3.plot(filtered)

ax4.plot(error)

plt.show()