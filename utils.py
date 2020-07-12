import wfdb
from scipy.fftpack import rfft, irfft, fftfreq
from scipy import interpolate
import matplotlib.pyplot as plt
import numpy as np


def _resample_waveform(waveform, fs, new_fs):
    """Resample training sample to set sample frequency."""

    if len(waveform.shape) == 1:
        waveform = waveform.reshape(-1, 1)
    length, leads_num = waveform.shape

    # Get time array
    time = np.arange(length) * 1 / fs

    # Generate new resampling time array
    times_rs = np.arange(0, time[-1], 1 / new_fs)

    interpolated_waves = np.zeros((len(times_rs), leads_num))

    # Setup interpolation function for every leads
    for lean_n in range(leads_num):
        interp_func = interpolate.interp1d(x=time, y=waveform[:, lean_n], kind='linear')

        # Interpolate contiguous segment
        sample_rs = interp_func(times_rs)
        interpolated_waves[:, lean_n] = sample_rs

    return interpolated_waves


# def _resample_waveform(self, waveform, fs):
#     """Resample training sample to set sample frequency."""
#     # Get time array
#     time = np.arange(len(waveform)) * 1 / fs
#
#     # Generate new resampling time array
#     times_rs = np.arange(0, time[-1], 1 / self.fs)
#
#     # Setup interpolation function
#     interp_func = interpolate.interp1d(x=time, y=waveform, kind='linear')
#
#     # Interpolate contiguous segment
#     sample_rs = interp_func(times_rs)
#
#     return sample_rs


def read_mit_data(file):
    NEW_FS = 1000

    def smooth_line(y, fd):
        # fd - частота дискретизации
        W = fftfreq(y.size, 1 / fd)
        f_signal = rfft(y)
        cut_f_signal = f_signal.copy()
        cut_f_signal[(W < 0.25)] = 0
        cut_f_signal[(W > 60)] = 0
        cut_signal = irfft(cut_f_signal)
        return cut_signal

    record = wfdb.rdrecord(file)
    print(record.fs)
    # data = smooth_line(record.adc()[:, 0], record.fs)
    data = record.adc().astype(np.float16)
    if record.fs != NEW_FS:
        data = _resample_waveform(data, fs=record.fs, new_fs=NEW_FS)
    data /= 1000
    return data.transpose()


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