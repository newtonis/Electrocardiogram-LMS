from get_data import all_signals
import matplotlib.pyplot as plt
from getPeaks import getPeaks
from scipy.signal import detrend
from filterARF import filterARF
import numpy as np


fs = 360
timespan = 400
time_cycle = 1.4
# señal = no_noise_signal
señal = all_signals["202"]["upper"][:timespan*fs]
t = np.arange(len(señal)) / fs
errores = list(all_signals["202"]["anomalies"].keys())
errores = [float(errores[i]) / fs for i in range(len(errores))]


def anomaly_plotter(axis, anomalies, timespan, min, max):
  for ai in anomalies:
    if ai < timespan:
        axis.plot([ai, ai], [min, max], 'orange')



señal = detrend(señal)      # quitamos la tendencia que agrega el ruido de línea y de los movimientos corporales
peaks = getPeaks(señal, fs, time_cycle / 2, time_cycle / 10)

myFilterARF = filterARF(500, 0.1)
filtered, error = myFilterARF.train(peaks, señal)

fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, sharex=True)

ax1.plot(t, señal)
anomaly_plotter(axis=ax1, anomalies=errores, timespan=timespan, min=min(señal), max=max(señal))

ax2.plot(t, peaks)
ax3.plot(t, filtered)

anomaly_plotter(axis=ax4, anomalies=errores, timespan=timespan, min=min(error), max=max(error))

ax4.plot(t, abs(error))

plt.show()