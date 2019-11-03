# https://github.com/MIT-LCP/wfdb-python
# https://wfdb.readthedocs.io/en/latest/
import numpy as np
import wfdb
import matplotlib.pyplot as plt
import padasip as pa


def get_data(file_path, sampto='end'):
    """
    get_data devuelve las señales del primer y segundo canal de un archivo que cumple con el estándar wfdb,
    la metadata del mismo y las anotaciones del mismo en caso de haberlas (archivo con el mismo nombre pero con extensión .atr)

    Parámetros:
      file_path: path del archivo de donde conseguir las señales a leer.
      sampto: cantidad de samples a leer. Si 'end', lee todas las samples del archivo.
    Returns:
      signal_0: Señal del primer canal.
      signal_1: Señal del segundo canal.
      metadata: metadata que contiene, entre otras cosas, la sample frequency utilizada para tomar los datos.
      annotation: anotaciones correspondientes al archivo
    """
    # Cada columna de la matriz signals es un canal de las señales grabadas del paciente(signals[0] es el primer canal)
    # metadata tiene información como la sample frequency, importante para el resto del trabajo.
    signals, metadata = wfdb.rdsamp(record_name=file_path, sampto=sampto)
    annotation = wfdb.rdann(record_name=file_path, extension='atr', sampto=sampto)

    return signals[:, 0], signals[:, 1], metadata, annotation

