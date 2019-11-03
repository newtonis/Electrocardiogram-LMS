# https://github.com/MIT-LCP/wfdb-python
# https://wfdb.readthedocs.io/en/latest/
import numpy as np
import wfdb
import matplotlib.pyplot as plt
import padasip as pa
from get_data import get_data


import numpy as np
import matplotlib.pyplot as plt

# https://matousc89.github.io/padasip/sources/filters/lms.html#references
# https://matousc89.github.io/padasip/_modules/padasip/filters/lms.html#FilterLMS
# https://matousc89.github.io/padasip/sources/filters/lms.html#references
# https://matousc89.github.io/padasip/_modules/padasip/filters/lms.html#FilterLMS

class FilterLMS():
    """
    This class represents an adaptive LMS filter.

    **Args:**

    * `n` : length of filter (integer) - how many input is input array
      (row of input matrix)

    **Kwargs:**

    * `mu` : learning rate (float). Also known as step size. If it is too slow,
      the filter may have bad performance. If it is too high,
      the filter will be unstable. The default value can be unstable
      for ill-conditioned input data.

    * `w` : initial weights of filter. Possible values are:

        * array with initial weights (1 dimensional array) of filter size

        * "random" : create random weights

        * "zeros" : create zero value weights
    """

    def __init__(self, n, w='zeros', mu=0.01):
        self.n = n
        self.mu = mu
        if w is 'zeros':
            self.w = np.zeros(self.n)
        else:
            if len(w) is self.n:
                self.w = np.array(w)
            else:
                raise ValueError('The size of filter must be the same as the size of the weights vector')

        self.input = np.array([])
        self.desired_response = np.array([])
        self.y = np.array([])
        self.e = np.array([])

    def adapt(self, d, x):
        """
        Adapt weights according one desired value and its input.

        **Args:**

        * `d` : desired value (float)

        * `x` : input array (1-dimensional array)
        """
        y = np.dot(self.w, x)
        e = d - y
        self.w += self.mu * e * x
        return y, e

    def run(self, u, mu):
        m = len(u)
        y = np.zeros(m)
        e = np.zeros(m)
        w = np.zeros((m, self.n + 1))
        n = self.n


        #print(w.shape)
        print(m, n)

        for i in range(m):

            ### Primero actualizo w[n]

            for k in range(0, n+1):
                if i - k - 1 >= 0:
                    w[i][k] = w[i - 1][k] + mu * u[i - k - 1] * e[i - 1]  # formula de LMS
                else:
                    w[i][k] = 0.001

            ### En segundo lugar actualizo la salida
            if i + 1 >= n + 1:
                y[i] = np.dot(w[i], np.flip(u[i + 1 - (n + 1):i + 1]))
            else:
                y[i] = np.dot(w[i][:i + 1], np.flip(u[:i + 1]))

            ### En tercer lugar actualizo el error

            e[i] = u[i] - y[i]

        return y, w, e

    def syntetizar(self, w, m):
        y = np.zeros(m)

        k = len(w)-1
        print(w)
        for i in range(m):
            if i + 1 >= k+1:
                y[i] = np.dot(w, np.flip(y[i+1 - (k+1):i+1])) + np.random.rand() * 0.0001
            else:
                y[i] = np.dot(w[:i+1], np.flip(y[:i+1])) + np.random.rand() * 0.0001
        return y

    def plot(self, x, y, e):
        pass


all_signals = {str(i): dict() for j in (range(100, 125), range(200, 224)) for i in j}
# borramos del dictionary a los archivos que no estan pero que fueron agregados por comodidad
for i in ['110', '120', '204','206','211','216','218']: del all_signals[i]
all_signals['228'] = None
for i in range(230,235) : all_signals[str(i)] = None

for signal_name in all_signals.keys():
    upper_signal, lower_signal, metadata, annotations =  get_data(file_path='data/' + signal_name,sampto=None)
    #print(metadata)
    all_signals[signal_name] = {'upper' : upper_signal, 'lower' : lower_signal, 'meta':metadata, 'annot': annotations}


filter_size = 500

predictor_filter = FilterLMS(n=filter_size, w='zeros', mu=0.005)
sampling_size = 300000

end_sec = 30
start_sec = 0

end = int(end_sec * 360)
start = int(start_sec * 360)

u = all_signals["221"]["upper"][start:end]

ts = 1 / 360
t = np.arange(start_sec, end_sec, ts)

y, w, e = predictor_filter.run(u = u, mu= 0.01)

y2 = predictor_filter.syntetizar(w[-1], 10000)
t2 = np.arange(end, end + 10000*ts, ts)[:10000]

w = np.transpose(w)


#for w_i in w:
#    plt.plot(t, w_i)

plt.plot(t, u, label="señal")
plt.plot(t, y, label="prediccion")
plt.plot(t, e, label="error")
#plt.plot(t2, y2, label="sintetizado")

plt.legend()
plt.show()
