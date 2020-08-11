import numpy as np
from scipy.signal import welch
from spike2py import signal_processing


def test_mixin_methods_present(mixin_methods):
    mixin = signal_processing.SignalProcessing()
    for method in mixin_methods:
        assert method in mixin.__dir__()


def test_mixin_remove_mean_all_values(mixin):
    mixin.remove_mean()
    assert 'proc_remove_mean' in mixin.__dir__()
    expected = 2072868243385
    actual = int(np.mean(mixin.values) * 10e15)
    assert actual == expected


def test_mixin_remove_mean_first_thousand(mixin):
    mixin.remove_mean(first_n_samples=1000)
    assert 'proc_remove_mean' in mixin.__dir__()
    expected = 223791399750
    actual = int(np.mean(mixin.values) * 10e10)
    assert actual == expected


def test_mixin_remove_value(mixin):
    mixin.remove_value(2.5)
    assert 'proc_remove_value_2_5' in mixin.__dir__()
    expected = 5002509452495857
    actual = int(np.mean(mixin.values) * 10e15)
    assert actual == expected


def test_mixin_lowpass_cutoff(mixin):
    mixin.lowpass(cutoff=5)
    assert 'proc_filt_5_lowpass' in mixin.__dir__()
    freq, power_spectral_density = welch(x=mixin.values,
                                         fs=mixin.details.sampling_frequency,
                                         nperseg=1024,
                                         detrend='linear')
    mean_low_fq = int(np.mean(power_spectral_density[freq < 5]) * 10e15)
    mean_high_fq = int(np.mean(power_spectral_density[freq > 5]) * 10e15)
    assert mean_low_fq == 1034230483173
    assert mean_high_fq == 277778547


def test_mixin_lowpass_cutoff_order(mixin):
    mixin.lowpass(cutoff=50, order=2)
    assert 'proc_filt_50_lowpass' in mixin.__dir__()
    freq, power_spectral_density = welch(x=mixin.values,
                                         fs=mixin.details.sampling_frequency,
                                         nperseg=1024,
                                         detrend='linear')
    mean_low_fq = int(np.mean(power_spectral_density[freq < 50]) * 10e15)
    mean_high_fq = int(np.mean(power_spectral_density[freq > 50]) * 10e15)
    assert mean_low_fq == 1204601335257
    assert mean_high_fq == 9108669488


def test_mixin_high_cutoff(mixin):
    mixin.highpass(cutoff=250)
    assert 'proc_filt_250_highpass' in mixin.__dir__()
    freq, power_spectral_density = welch(x=mixin.values,
                                         fs=mixin.details.sampling_frequency,
                                         nperseg=1024,
                                         detrend='linear')
    mean_low_fq = int(np.mean(power_spectral_density[freq < 100]) * 10e15)
    mean_high_fq = int(np.mean(power_spectral_density[freq > 100]) * 10e15)
    assert mean_low_fq == 6463207
    assert mean_high_fq == 955046880433


def test_mixin_high_cutoff_order(mixin):
    mixin.highpass(cutoff=150, order=8)
    assert 'proc_filt_150_highpass' in mixin.__dir__()
    freq, power_spectral_density = welch(x=mixin.values,
                                         fs=mixin.details.sampling_frequency,
                                         nperseg=1024,
                                         detrend='linear')
    mean_low_fq = int(np.mean(power_spectral_density[freq < 100]) * 10e15)
    mean_high_fq = int(np.mean(power_spectral_density[freq > 100]) * 10e15)
    assert mean_low_fq == 9790724
    assert mean_high_fq == 1389422764285


def test_mixin_bandpass_cutoff(mixin):
    mixin.bandpass(cutoff=[50, 100])
    assert 'proc_filt_50_100_bandpass' in mixin.__dir__()
    freq, power_spectral_density = welch(x=mixin.values,
                                         fs=mixin.details.sampling_frequency,
                                         nperseg=1024,
                                         detrend='linear')
    fq_bandpass_bool = list((freq > 50) & (freq < 100))
    fq_not_bandpass_bool = [not boolean for boolean in fq_bandpass_bool]
    mean_not_bandpass_fq = int(
        np.mean(power_spectral_density[fq_not_bandpass_bool] * 10e15))
    mean_bandpass_fq = int(
        np.mean(power_spectral_density[fq_bandpass_bool] * 10e15))
    assert mean_not_bandpass_fq == 5909656213
    assert mean_bandpass_fq == 1396973349240


def test_mixin_bandpass_cutoff_order(mixin):
    mixin.bandpass(cutoff=[5, 200], order=2)
    assert 'proc_filt_5_200_bandpass' in mixin.__dir__()
    freq, power_spectral_density = welch(x=mixin.values,
                                         fs=mixin.details.sampling_frequency,
                                         nperseg=1024,
                                         detrend='linear')
    fq_bandpass_bool = list((freq > 5) & (freq < 200))
    fq_not_bandpass_bool = [not boolean for boolean in fq_bandpass_bool]
    mean_not_bandpass_fq = int(
        np.mean(power_spectral_density[fq_not_bandpass_bool] * 10e15))
    mean_bandpass_fq = int(
        np.mean(power_spectral_density[fq_bandpass_bool] * 10e15))
    assert mean_not_bandpass_fq == 38579335669
    assert mean_bandpass_fq == 1291038336160


def test_mixin_bandstop_cutoff(mixin):
    mixin.bandstop(cutoff=[50, 100])
    assert 'proc_filt_50_100_bandstop' in mixin.__dir__()
    freq, power_spectral_density = welch(x=mixin.values,
                                         fs=mixin.details.sampling_frequency,
                                         nperseg=1024,
                                         detrend='linear')
    fq_bandstop_bool = list((freq > 50) & (freq < 100))
    fq_not_bandstop_bool = [not boolean for boolean in fq_bandstop_bool]
    mean_not_bandstop_fq = int(
        np.mean(power_spectral_density[fq_not_bandstop_bool] * 10e15))
    mean_bandstop_fq = int(
        np.mean(power_spectral_density[fq_bandstop_bool] * 10e15))
    assert mean_not_bandstop_fq == 1580149786346
    assert mean_bandstop_fq == 28136638802


def test_mixin_bandstop_cutoff_order(mixin):
    mixin.bandstop(cutoff=[5, 200], order=2)
    assert 'proc_filt_5_200_bandstop' in mixin.__dir__()
    freq, power_spectral_density = welch(x=mixin.values,
                                         fs=mixin.details.sampling_frequency,
                                         nperseg=1024,
                                         detrend='linear')
    fq_bandstop_bool = list((freq > 5) & (freq < 200))
    fq_not_bandstop_bool = [not boolean for boolean in fq_bandstop_bool]
    mean_not_bandstop_fq = int(
        np.mean(power_spectral_density[fq_not_bandstop_bool] * 10e15))
    mean_bandstop_fq = int(
        np.mean(power_spectral_density[fq_bandstop_bool] * 10e15))
    assert mean_not_bandstop_fq == 1369084776753
    assert mean_bandstop_fq == 57886781964
