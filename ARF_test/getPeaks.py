import numpy as np

# get peaks of signal

"""
min_distance: distance of peaks
fs: frecuency sample
signal: samples
"""

def getPeaks(signal, fs, min_distance, impulse_distance = 0):
    power_signal = np.power(signal,2)
    max_value = max(power_signal) # maximo valor de la potencia
    peakSignal = np.zeros(len(signal)) # señal donde almacenamos los picos

    counter = 0
    impulse_ticks = int(impulse_distance * fs)

    for i in range(len(signal)):
        if counter > 0:
            counter -= 1
        elif power_signal[i] > max_value * 0.5:
            counter = min_distance * fs
            if i > impulse_ticks:
                peakSignal[i - impulse_ticks] = 1

    return peakSignal

