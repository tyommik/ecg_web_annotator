import wfdb
from scipy.fftpack import rfft, irfft, fftfreq
import matplotlib.pyplot as plt


def read_mit_data(file):
    def smooth_line(y, fd):
        # fd - частота дискретизации
        W = fftfreq(y.size, 1 / fd)
        f_signal = rfft(y)
        cut_f_signal = f_signal.copy()
        cut_f_signal[(W < 0.25)] = 0
        cut_f_signal[(W > 60)] = 0
        cut_signal = irfft(cut_f_signal)
        return cut_signal

    plt.cla()
    record = wfdb.rdrecord(file)
    # data = smooth_line(record.adc()[:, 0], record.fs)
    data = record.adc()[:, 0]

    return data


def read_mit_fig(file):
    def smooth_line(y, fd):
        # fd - частота дискретизации
        W = fftfreq(y.size, 1 / fd)
        f_signal = rfft(y)
        cut_f_signal = f_signal.copy()
        cut_f_signal[(W < 0.25)] = 0
        cut_f_signal[(W > 60)] = 0
        cut_signal = irfft(cut_f_signal)
        return cut_signal

    plt.cla()
    record = wfdb.rdrecord(file)
    fig = wfdb.plot_items(signal=smooth_line(record.p_signal[:, 0], record.fs),
                        title='V1', time_units='seconds',
                        fs=record.fs,
                        figsize=(10,2), return_fig=True)#, ecg_grids='all')

    return fig