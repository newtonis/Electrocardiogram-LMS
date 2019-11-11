from get_data import all_signals
import matplotlib.pyplot as plt
from getPeaks import getPeaks
from scipy.signal import detrend
from filterARF import filterARF
import numpy as np
import random
from test02filterTrain import plotSignal

def anomaly_plotter(axis, anomalies, timespan, min, max):
    for ai in anomalies:
        if ai < timespan:
            axis.plot([ai, ai], [min, max], 'orange')

minimo = 100000
maximo = -100000

fs = 360
timespan = 5000
time_cycle = 1.4


for nombre in all_signals.keys():

    plotSignal(nombre)

    plt.savefig("output/%s.png" % nombre, dpi=1000)
    print("Almacenado output/%s.png" % nombre)
    plt.close()

