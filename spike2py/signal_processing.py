import numpy as np
from scipy.signal import butter, filtfilt
from sklearn.linear_model import LinearRegression


class SignalProcessing:
    """Mixin class that adds signal processing methods"""

    def _setattr(self, name):
        setattr(self, name, self.values)

    def remove_mean(self, first_n_samples=None):
        """Subtracts mean calculated from all `values` (default) or first
        n samples.

        Parameters
        ----------
        first_n_samples: int

        """
        values_slice = slice(0, -1)
        if first_n_samples:
            values_slice = slice(0, first_n_samples)
        self.values -= np.mean(self.values[values_slice])
        self._setattr('proc_remove_mean')
        return self

    def remove_value(self, value):
        """Subtracts value from `values`

        Parameters
        ----------
        value: int, float

        """
        self.values -= value
        self._setattr(f'proc_remove_value_{value}')
        return self

    def lowpass(self, cutoff, order=4):
        """Apply dual-pass Butterworth lowpass filter to `values`

        Parameters
        ----------
        cutoff: int, float
        order: int

        """
        self._filt(cutoff, order, 'lowpass')
        return self

    def highpass(self, cutoff, order=4):
        """Apply dual-pass Butterworth highpass filter to `values`

        Parameters
        ----------
        cutoff: int, float
        order: int

        """
        self._filt(cutoff, order, 'highpass')
        return self

    def bandpass(self, cutoff, order=4):
        """Apply dual-pass Butterworth bandpass filter to `values`

        Parameters
        ----------
        cutoff: list[int, int], list[float, float]
        order: int

        """
        self._filt(np.array(cutoff), order, 'bandpass')
        return self

    def bandstop(self, cutoff, order=4):
        """Apply dual-pass Butterworth bandstop filter to `values`

        Parameters
        ----------
        cutoff: list[int, int], list[float, float]
        order: int

        """
        self._filt(np.array(cutoff), order, 'bandstop')
        return self

    def _filt(self, cutoff, order, filt_type):
        critical_fq = cutoff / (self.details.sampling_frequency / 2)
        filt_coef_b, filt_coef_a = butter(N=order,
                                          Wn=critical_fq,
                                          btype=filt_type)
        self.values = filtfilt(filt_coef_b, filt_coef_a, self.values)
        self._setattr(f'proc_filt_{cutoff}_{filt_type}')

    def calibrate(self, slope=None, offset=None):
        """Calibrate `values` using linear formula y=slope*x+offset

        Parameters
        ----------
        slope: float
        offset: float

        """
        if not offset:
            self.values = self.values * slope
        if slope and offset:
            self.values = (self.values * slope) - offset
        self._setattr(f'proc_calib')
        return self

    def norm_percentage(self):
        """Normalise `values` to 0-100%"""
        self.values = (self.values / np.max(self.values)) * 100
        self._setattr(f'proc_norm_percentage')
        return self

    def norm_proportion(self):
        """Normalise `values` to 0-1"""
        self.values = (self.values / np.max(self.values))
        self._setattr(f'proc_norm_proportion')
        return self

    def norm_percent_value(self, value):
        """Normalise `values` to a percentage of `value`

        Parameters
        ----------
        value: int, float
        """
        self.values = (self.values / value) * 100
        self._setattr(f'proc_norm_value')
        return self

    def rect(self):
        """Rectify `values"""
        self.values = abs(self.values)
        self._setattr('rect')
        return self

    def interp_new_times(self, new_times):
        """Interpolate `values` to a new time axis

        Parameters
        ----------
        new_times: list, np.array

        """

        self._interp(new_times)
        self._setattr('interp_new_times')
        return self

    def interp_new_fs(self, new_sampling_frequency):
        """Interpolate `values` to a new sampling frequency

        Parameters
        ----------
        new_sampling_frequency: int

        """
        new_times = np.arrange(start=self.times[0],
                               stop=self.times(-1),
                               step=1 / new_sampling_frequency)
        self._interp(new_times)
        self._setattr('interp_new_fs')
        return self

    def _interp(self, new_times):
        self.values = np.interp(x=new_times,
                                xp=self.times,
                                fp=self.values)

    def linear_detrend(self):
        """Remove linear trend from `values`"""
        times = np.reshape(self.times, (len(self.times), 1))
        model = LinearRegression()
        model.fit(times, self.values)
        trend = model.predict(times)
        self.values = [self.values[i] - trend[i]
                       for i in range(0, len(self.values))]
        return self
