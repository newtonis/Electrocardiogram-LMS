from get_data import all_signals

# observar señal 210


def detectPeaks(signal):
    maxvalue = max(signal)
    wait = 0

    peakpoints = []

    for i in signal:
        if wait == 0 and i > maxvalue * 0.5:
            peakpoints.append(i)
            wait = 250
        elif wait > 0:
            wait -= 1

    return peakpoints

print(detectPeaks(all_signals["210"]))
