import pytest
from pytest import approx
import numpy as np
from scipy.signal import welch

from spike2py import sig_proc


def test_signal_processing_methods_present(mixin_methods):
    mixin = sig_proc.SignalProcessing()
    for method in mixin_methods:
        assert method in mixin.__dir__()


def test_signal_processing_remove_mean_all_values(mixin):
    mixin.remove_mean()
    assert "proc_remove_mean" in mixin.__dir__()
    assert np.mean(mixin.values) == approx(0.0002072868243385)


def test_signal_processing_remove_mean_first_thousand_values(mixin):
    mixin.remove_mean(first_n_samples=1000)
    assert "proc_remove_mean" in mixin.__dir__()
    assert np.mean(mixin.values) == approx(2.23791399750)


@pytest.mark.parametrize("value", [0, 100001])
def test_signal_processing_remove_mean_first_n_samples_out_of_range(mixin, value):
    with pytest.raises(ValueError):
        mixin.remove_mean(first_n_samples=value)


def test_signal_processing_remove_mean_first_n_samples_type_error(mixin):
    with pytest.raises(TypeError):
        mixin.remove_mean(first_n_samples=4.5)


def test_signal_processing_remove_value_attribute_naming(mixin):
    mixin.remove_value(-2.5)
    assert "proc_remove_value_2_5" in mixin.__dir__()


def test_signal_processing_remove_value(mixin):
    value = -2000
    mean_before = np.mean(mixin.values)
    mixin.remove_value(value)
    mean_after = np.mean(mixin.values)
    assert "proc_remove_value_2000" in mixin.__dir__()
    assert int(mean_before - mean_after) == value


def test_signal_processing_lowpass_with_cutoff(mixin):
    mixin.lowpass(cutoff=5)
    assert "proc_filt_5_lowpass" in mixin.__dir__()
    freq, power_spectral_density = welch(
        x=mixin.values,
        fs=mixin.info.sampling_frequency,
        nperseg=1024,
        detrend="linear",
    )
    mean_low_fq = np.mean(power_spectral_density[freq < 5])
    mean_high_fq = np.mean(power_spectral_density[freq > 5])
    assert mean_low_fq == approx(0.0001016062190551)
    assert mean_high_fq == approx(3.5692679e-08)


@pytest.mark.parametrize("cutoff", [0, 1024])
def test_signal_processing_lowpass_cutoff_out_of_range(mixin, cutoff):
    with pytest.raises(ValueError):
        mixin.lowpass(cutoff=cutoff)


@pytest.mark.parametrize("order", [0, 17])
def test_signal_processing_lowpass_order_out_of_range(mixin, order):
    with pytest.raises(ValueError):
        mixin.lowpass(cutoff=20, order=order)


def test_signal_processing_lowpass_with_cutoff_and_order(mixin):
    mixin.lowpass(cutoff=50, order=2)
    assert "proc_filt_50_lowpass" in mixin.__dir__()
    freq, power_spectral_density = welch(
        x=mixin.values,
        fs=mixin.info.sampling_frequency,
        nperseg=1024,
        detrend="linear",
    )
    mean_low_fq = np.mean(power_spectral_density[freq < 50])
    mean_high_fq = np.mean(power_spectral_density[freq > 50])
    assert mean_low_fq == approx(0.0001216392998562)
    assert mean_high_fq == approx(1.00296037e-06)


def test_signal_processing_highpass_with_cutoff(mixin):
    mixin.highpass(cutoff=250)
    assert "proc_filt_250_highpass" in mixin.__dir__()
    freq, power_spectral_density = welch(
        x=mixin.values,
        fs=mixin.info.sampling_frequency,
        nperseg=1024,
        detrend="linear",
    )
    mean_low_fq = np.mean(power_spectral_density[freq < 100])
    mean_high_fq = np.mean(power_spectral_density[freq > 100])
    assert mean_low_fq == approx(6.082511531e-10)
    assert mean_high_fq == approx(9.58830303178e-05)


def test_signal_processing_highpass_with_cutoff_and_order(mixin):
    mixin.highpass(cutoff=150, order=8)
    assert "proc_filt_150_highpass" in mixin.__dir__()
    freq, power_spectral_density = welch(
        x=mixin.values,
        fs=mixin.info.sampling_frequency,
        nperseg=1024,
        detrend="linear",
    )
    mean_low_fq = np.mean(power_spectral_density[freq < 100])
    mean_high_fq = np.mean(power_spectral_density[freq > 100])
    assert mean_low_fq == approx(9.457695299e-10)
    assert mean_high_fq == approx(0.000141424081)


def test_signal_processing_bandpass_with_cutoff(mixin):
    mixin.bandpass(cutoff=[50, 100])
    assert "proc_filt_50_100_bandpass" in mixin.__dir__()
    freq, power_spectral_density = welch(
        x=mixin.values,
        fs=mixin.info.sampling_frequency,
        nperseg=1024,
        detrend="linear",
    )
    fq_bandpass_bool = list((freq > 50) & (freq < 100))
    fq_not_bandpass_bool = [not boolean for boolean in fq_bandpass_bool]
    mean_not_bandpass_fq = np.mean(power_spectral_density[fq_not_bandpass_bool])
    mean_bandpass_fq = np.mean(power_spectral_density[fq_bandpass_bool])
    assert mean_not_bandpass_fq == approx(4.83518473e-07)
    assert mean_bandpass_fq == approx(0.00014254199)


def test_signal_processing_bandpass_cutoff_out_of_range(mixin):
    with pytest.raises(ValueError):
        mixin.lowpass(cutoff=[5, 1024])


def test_signal_processing_bandpass_with_cutoff_and_order(mixin):
    mixin.bandpass(cutoff=[5, 200], order=2)
    assert "proc_filt_5_200_bandpass" in mixin.__dir__()
    freq, power_spectral_density = welch(
        x=mixin.values,
        fs=mixin.info.sampling_frequency,
        nperseg=1024,
        detrend="linear",
    )
    fq_bandpass_bool = list((freq > 5) & (freq < 200))
    fq_not_bandpass_bool = [not boolean for boolean in fq_bandpass_bool]
    mean_not_bandpass_fq = np.mean(power_spectral_density[fq_not_bandpass_bool])
    mean_bandpass_fq = np.mean(power_spectral_density[fq_bandpass_bool])
    assert mean_not_bandpass_fq == approx(4.02363214e-06)
    assert mean_bandpass_fq == approx(0.00013225323034)


def test_signal_processing_bandstop_with_cutoff(mixin):
    mixin.bandstop(cutoff=[50, 100])
    assert "proc_filt_50_100_bandstop" in mixin.__dir__()
    freq, power_spectral_density = welch(
        x=mixin.values,
        fs=mixin.info.sampling_frequency,
        nperseg=1024,
        detrend="linear",
    )
    fq_bandstop_bool = list((freq > 50) & (freq < 100))
    fq_not_bandstop_bool = [not boolean for boolean in fq_bandstop_bool]
    mean_not_bandstop_fq = np.mean(power_spectral_density[fq_not_bandstop_bool])
    mean_bandstop_fq = np.mean(power_spectral_density[fq_bandstop_bool])
    assert mean_not_bandstop_fq == approx(0.000161772149)
    assert mean_bandstop_fq == approx(3.7779100806e-06)


def test_signal_processing_bandstop_cutoff_and_order(mixin):
    mixin.bandstop(cutoff=[5, 200], order=2)
    assert "proc_filt_5_200_bandstop" in mixin.__dir__()
    freq, power_spectral_density = welch(
        x=mixin.values,
        fs=mixin.info.sampling_frequency,
        nperseg=1024,
        detrend="linear",
    )
    fq_bandstop_bool = list((freq > 5) & (freq < 200))
    fq_not_bandstop_bool = [not boolean for boolean in fq_bandstop_bool]
    mean_not_bandstop_fq = np.mean(power_spectral_density[fq_not_bandstop_bool])
    mean_bandstop_fq = np.mean(power_spectral_density[fq_bandstop_bool])
    assert mean_not_bandstop_fq == approx(0.000139964355325)
    assert mean_bandstop_fq == approx(5.790131269e-06)


def test_signal_processing_calibrate_with_slope(mixin):
    mixin.calibrate(slope=10.4)
    assert "proc_calib" in mixin.__dir__()
    assert int(min(mixin.values)) == 0
    assert int(max(mixin.values)) == 61


def test_signal_processing_calibrate_with_slope_and_offset(mixin):
    mixin.calibrate(slope=10.4, offset=78.3)
    assert int(min(mixin.values)) == -78
    assert int(max(mixin.values)) == -16


def test_signal_processing_norm_percentage(mixin):
    mixin.norm_percentage()
    assert "proc_norm_percentage" in mixin.__dir__()
    assert int(min(mixin.values)) == 0
    assert int(max(mixin.values)) == 100


def test_signal_processing_norm_proportion(mixin):
    mixin.norm_proportion()
    assert "proc_norm_proportion" in mixin.__dir__()
    assert int(min(mixin.values)) == 0
    assert int(max(mixin.values)) == 1


def test_signal_processing_norm_percent_value(mixin):
    mixin.norm_percent_value(35)
    assert "proc_norm_value" in mixin.__dir__()
    assert int(min(mixin.values)) == 0
    assert int(max(mixin.values)) == 17


def test_signal_processing_rect(negative_value_mixin):
    negative_value_mixin.rect()
    assert "proc_rect" in negative_value_mixin.__dir__()
    assert all(value >= 0 for value in negative_value_mixin.values)


def test_signal_processing_interp_new_times(mixin):
    new_times = np.linspace(0, 100, 1000)
    len_new_times = len(new_times)
    mixin.interp_new_times(new_times)
    assert "proc_interp_new_times" in mixin.__dir__()
    assert "times_pre_interp" in mixin.__dir__()
    assert np.mean(mixin.values) == approx(3.00124641)
    assert len(mixin.times) == len_new_times


def test_signal_processing_interp_new_fs(mixin):
    mixin.interp_new_fs(500)
    assert "proc_interp_new_fs" in mixin.__dir__()
    assert "times_pre_interp" in mixin.__dir__()
    assert np.mean(mixin.values) == approx(3.000221)
    assert len(mixin.times) == 50000


def test_signal_processing_linear_detrend(mixin):
    mixin.linear_detrend()
    assert "proc_linear_detrend" in mixin.__dir__()
    assert np.mean(mixin.values) == approx(0.0)
