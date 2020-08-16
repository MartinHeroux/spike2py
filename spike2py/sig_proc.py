from typing import Union, List, Literal

import numpy as np
from scipy.signal import butter, filtfilt, detrend


class SignalProcessing:
    """Mixin class that adds signal processing methods"""

    def _setattr(self, name: str):
        setattr(self, name, self.values)

    def remove_mean(self, first_n_samples: int = None):
        """Subtract mean of first n samples (default is all samples)"""
        values_slice = slice(0, -1)
        if first_n_samples is not None:
            error_msg = (
                "first_n_samples must be a whole number between 1 and "
                f"the length of the signal (i.e. {len(self.values)})."
            )
            if (first_n_samples < 1) or (first_n_samples > len(self.values)):
                raise ValueError(error_msg)
            if not isinstance(first_n_samples, int):
                raise TypeError(error_msg)
            values_slice = slice(0, first_n_samples)
        self.values -= np.mean(self.values[values_slice])
        self._setattr("proc_remove_mean")
        return self

    def remove_value(self, value: float):
        """Subtracts value from `values` """
        try:
            self.values -= value
            str_value = self._float_to_string_with_underscore(value)
            self._setattr(f"proc_remove_value_{str_value}")
            return self
        except np.core._exceptions.UFuncTypeError:
            raise TypeError("`value` must be a whole number or a decimal number.")

    def _float_to_string_with_underscore(self, float_value: float):
        return str(abs(float_value)).replace(".", "_")

    def lowpass(self, cutoff: float, order: int = 4):
        """Apply dual-pass Butterworth lowpass filter to `values` """
        self._filt(cutoff, order, "lowpass")
        return self

    def highpass(self, cutoff: float, order: int = 4):
        """Apply dual-pass Butterworth highpass filter to `values` """
        self._filt(cutoff, order, "highpass")
        return self

    def bandpass(self, cutoff: List[float], order: int = 4):
        """Apply dual-pass Butterworth bandpass filter to `values` """
        self._filt(np.array(cutoff), order, "bandpass")
        return self

    def bandstop(self, cutoff: List[float], order: int = 4):
        """Apply dual-pass Butterworth bandstop filter to `values` """
        self._filt(np.array(cutoff), order, "bandstop")
        return self

    def _filt(
        self,
        cutoff: Union[List[float], float],
        order: int,
        filt_type: Literal["lowpass", "highpass", "bandstop", "bandpass"],
    ):
        self._check_cutoff_in_range(cutoff)
        self._check_filter_order_appropriate(order)
        critical_fq = cutoff / (self.details.sampling_frequency / 2)
        filt_coef_b, filt_coef_a = butter(order, critical_fq, filt_type)
        self.values = filtfilt(filt_coef_b, filt_coef_a, self.values)
        if not isinstance(cutoff, int):
            cutoff = self._cutoff_to_string(cutoff)
        self._setattr(f"proc_filt_{cutoff}_{filt_type}")

    def _check_cutoff_in_range(self, cutoff: List[float]):
        if isinstance(cutoff, (int, float)):
            cutoff = [cutoff]
        for value in cutoff:
            if (value <= 0) or (value > self.details.sampling_frequency / 2):
                raise ValueError(
                    f"Filter cutoff frequency must be between 0 and "
                    f"{int(self.details.sampling_frequency/2)}"
                )

    def _check_filter_order_appropriate(self, order: int):
        if (order < 1) or (order > 16):
            raise ValueError("Filter order must be a whole number between 1 and 16")

    def _cutoff_to_string(self, cutoff: Union[List[float], float]):
        if isinstance(cutoff, np.ndarray):
            low = self._float_to_string_with_underscore(cutoff[0])
            high = self._float_to_string_with_underscore(cutoff[1])
            return f"{low}_{high}"
        if isinstance(cutoff, float):
            return self._float_to_string_with_underscore(cutoff)

    def calibrate(self, slope: float, offset: float = None):
        """Calibrate `values` using linear formula y=slope*x+offset"""
        if not offset:
            self.values = self.values * slope
        if slope and offset:
            self.values = (self.values * slope) - offset
        self._setattr(f"proc_calib")
        return self

    def norm_percentage(self):
        """Normalise `values` to 0-100%"""
        self.values = (self.values / np.max(self.values)) * 100
        self._setattr(f"proc_norm_percentage")
        return self

    def norm_proportion(self):
        """Normalise `values` to 0-1"""
        self.values = self.values / np.max(self.values)
        self._setattr(f"proc_norm_proportion")
        return self

    def norm_percent_value(self, value: float):
        """Normalise `values` to a percentage of `value`"""
        self.values = (self.values / value) * 100
        self._setattr(f"proc_norm_value")
        return self

    def rect(self):
        """Rectify `values"""
        self.values = abs(self.values)
        self._setattr("proc_rect")
        return self

    def interp_new_times(self, new_times: List[float]):
        """Interpolate `values` to a new time axis

        Parameters
        ----------
        new_times
            New time axis for interpolated data. Cannot be longer in duration
            than current time axis. If includes only a portion of the current
            time axis, only values associated with that portion of the time
            axis will be interpolated.
        """
        self._check_new_times(new_times)
        self._interp(new_times)
        self._setattr("proc_interp_new_times")
        return self

    def _check_new_times(self, new_times: List[float]):
        if new_times[-1] > self.times[-1]:
            raise ValueError(
                "New time axis for interpolation cannot be longer"
                "in duration than current time axis."
            )

    def interp_new_fs(self, new_sampling_frequency: int):
        """Interpolate `values` to a new sampling frequency"""
        new_times = np.arange(
            start=self.times[0], stop=self.times[-1], step=1 / new_sampling_frequency
        )
        self._interp(new_times)
        self._setattr("proc_interp_new_fs")
        return self

    def _interp(self, new_times: List[float]):
        self.values = np.interp(x=new_times, xp=self.times, fp=self.values)
        self.times_pre_interp = self.times
        self.times = new_times

    def linear_detrend(self):
        """Remove linear trend from `values`"""
        self.values = detrend(self.values, type="linear")
        self._setattr("proc_linear_detrend")
        return self
