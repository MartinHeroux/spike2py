from typing import Literal, Tuple

import numpy as np
import matplotlib
import matplotlib.pyplot as plt


from spike2py import channels, trial
from spike2py.types import all_channels, ticksline_channels

LINE_WIDTH = 2
FIG_SIZE = (12, 4)
WAVEFORM_FIG_SIZE = (12, 8)
MAX_TRIAL_FIG_HEIGHT = 30
LEGEND_LOC = "upper right"
COLORS = [
    "tab:blue",
    "tab:orange",
    "tab:green",
    "tab:red",
    "tab:purple",
    "tab:brown",
    "tab:pink",
    "tab:gray",
    "tab:olive",
    "tab:cyan",
]
DEFAULT_COLOR = COLORS[0]

matplotlib.rcParams.update({"font.size": 14})


def plot_channel(spike2py_channel: all_channels, save: Literal[True, False]) -> None:
    """Plot individual channels.

    Parameters
    ----------
    spike2py_channel:
        Instance of spike2py.channels.<ch> where possible ch are
        Event, Keyboard, Wavemark and Waveform
    save:
        Whether or not to save the generated figure.

    Returns
    -------
    None
    """

    if len(spike2py_channel.times) == 0:
        print("{spike2py_channel.info.name} channel has no data to plot.")
        return
    channel_type = repr(spike2py_channel).split()[0]
    if channel_type == "Waveform":
        # Split axis generation and plotting to allow reuse of plotting with trial plotting
        fig, ax = plt.subplots(figsize=WAVEFORM_FIG_SIZE)
        _plot_waveform(spike2py_channel, ax)
    else:
        ticks_line = _TicksLine(spike2py_channel)
        if ticks_line.ch_type == "Wavemark":
            fig, ax = plt.subplots(
                1, 2, figsize=FIG_SIZE, gridspec_kw={"width_ratios": [3, 1]}
            )
            ticks_line.plot(ax)
        else:
            fig, ax = plt.subplots(figsize=FIG_SIZE)
            ticks_line.plot(ax)
    title = (
    f"{spike2py_channel.info.subject_id}_"
    f"{spike2py_channel.info.name}_"
    f"{spike2py_channel.info.file.name}"
    )
    ax.text(0, 0, title,
            horizontalalignment='left',
            verticalalignment='top',
            transform=ax.transAxes,
            fontsize=10)
    if save:
        _save_plot(spike2py_channel.info)
    else:
        plt.show()


def _get_color(index: int) -> str:
    return COLORS[index % len(COLORS)]


def _plot_waveform(
    waveform: "channels.Waveform",
    ax: plt.Axes,
    color: str = DEFAULT_COLOR,
) -> None:
    ax.plot(waveform.times, waveform.values, label=waveform.info.name, color=color)
    ax.set_xlim(waveform.times[0], waveform.times[-1])
    units = waveform.info.units if waveform.info.units is True else "a.u."
    ax.set_ylabel(f"amplitude ({units})")
    ax.legend(loc=LEGEND_LOC)
    ax.set_xlabel("time (s)")
    ax.grid()


def _save_plot(channel_info: "channels.ChannelInfo") -> None:
    try:
        fig_name = (
            f"{channel_info.subject_id}_"
            f"{channel_info.trial_name}_"
            f"{channel_info.name}.pdf"
        )
    except AttributeError:
        fig_name = f"{channel_info.subject_id}_" f"{channel_info.name}.pdf"
    fig_path = channel_info.path_save_figures / fig_name
    plt.savefig(fig_path, dpi='figure')
    plt.close()


class _TicksLine:
    """Class that manages plotting of Event, Keyboard and Wavemark channels"""

    def __init__(
        self,
        ticks_line_channel: ticksline_channels,
        color: str = COLORS[0],
        y_offset: int = 0,
    ):
        """Initialise TicksLine Class

        Parameters
        ----------
        ticks_line_channel:
            Instance of spike2py.channels.< > where possible channel types are Event,
            Keyboard, and Wavemark
        color:
            Set color of ticks and line
        y_offset:
            Offset of ticks and line in the y-direction
        """

        self.ch = ticks_line_channel
        self.color = color
        self.offset = y_offset

        self.ch_type = repr(ticks_line_channel).split()[0]
        self.line_start_end = (self.ch.times[0], self.ch.times[-1])
        self.line_y_vals = (0.5 + y_offset, 0.5 + y_offset)
        self.tick_y_vals = (0.2 + y_offset, 0.8 + y_offset)

    def plot(self, ax: plt.Axes):
        if isinstance(ax, np.ndarray):
            ax1 = ax[0]
            ax2 = ax[1]
        else:
            ax1 = ax
            ax2 = None

        self._plot_ticks_line(ax1)
        self._finalise_plot(ax1)

        if self.ch_type == "Keyboard":
            self._plot_codes(ax1)
        if self.ch_type == "Textmark":
            self._plot_codes(ax1)
        if (self.ch_type == "Wavemark") and ax2:
            self._plot_action_potentials(ax2)

        plt.tight_layout()

    def _plot_ticks_line(self, ax1: plt.Axes):
        for time in self.ch.times:
            ax1.plot(
                (time, time), self.tick_y_vals, linewidth=LINE_WIDTH, color=self.color
            )
        ax1.plot(
            self.line_start_end,
            self.line_y_vals,
            linewidth=LINE_WIDTH,
            label=self.ch.info.name,
            color=self.color,
        )

    def _plot_codes(self, ax1: plt.Axes):
        for time, code in zip(self.ch.times, self.ch.codes):
            ax1.text(
                time, self.tick_y_vals[1] + 0.2, code, color=self.color, fontsize=10
            )

    def _plot_action_potentials(self, ax2: plt.Axes):
        for action_potential in self.ch.action_potentials:
            ax2.plot(action_potential, color=self.color, alpha=0.5)
        ax2.get_yaxis().set_visible(False)
        ax2.get_xaxis().set_visible(False)

    def _finalise_plot(self, ax1: plt.Axes):
        ax1.legend(loc=LEGEND_LOC)
        ax1.set_xlabel("time (s)")
        ax1.get_yaxis().set_visible(False)
        ax1.grid()


def plot_trial(spike2py_trial: "trial.Trial", save: Literal[True, False]) -> None:
    fig_height, n_subplots = _fig_height_n_subplots(spike2py_trial)
    if n_subplots == 1:
        print(
            f"The trial `{spike2py_trial.info.name}` has only one plottable channel."
            "\nPlease use `trial_name.ch_name.plot()` instead."
        )
    fig, ax = plt.subplots(
        sharex=True,
        nrows=n_subplots,
        figsize=(12, fig_height),
        gridspec_kw={"hspace": 0},
    )
    _plot_trial(spike2py_trial, ax)
    title = (
        f"{spike2py_trial.info.subject_id}_"
        f"{spike2py_trial.info.name}_"
        f"{spike2py_trial.info.file.name}"
    )
    ax[-1].text(0, 0, title,
            horizontalalignment='left',
            verticalalignment='top',
            transform=ax[-1].transAxes,
            fontsize=10)

    if save:
        _save_plot(spike2py_trial.info)
    else:
        plt.show()


def _fig_height_n_subplots(spike2py_trial: "trial.Trial") -> Tuple[int, int]:
    """Determine height and number of subplots to plot trial.

    Event, Keyboard and Wavemark channels are all plotted on same subplot at the
    top of the figure.
    Need to make sure these channels have data."""
    fig_height = 4
    n_subplots = 0
    plottable_ticks_line = False
    for channel, channel_type in spike2py_trial.channels:
        current_channel = spike2py_trial.__getattribute__(channel)
        if (
            (channel_type in ["event", "keyboard", "wavemark"])
            and (not plottable_ticks_line)
            and (len(current_channel.times) != 0)
        ):
            fig_height += 2
            plottable_ticks_line = True
            n_subplots += 1
        elif channel_type == "waveform":
            fig_height += 2
            n_subplots += 1
    fig_height = min(fig_height, MAX_TRIAL_FIG_HEIGHT)
    return fig_height, n_subplots


def _plot_trial(spike2py_trial: "trial.Trial", ax: plt.Axes):
    waveform_counter = 1
    other_ch_counter = 0
    n_subplots = len(ax)
    for channel, channel_type in spike2py_trial.channels:
        current_channel = spike2py_trial.__getattribute__(channel)
        if channel_type == "waveform":
            _plot_waveform(
                waveform=current_channel,
                ax=ax[n_subplots - waveform_counter],
                color=_get_color(waveform_counter - 1),
            )
            waveform_counter += 1
        elif len(current_channel.times) != 0:
            ticks_line = _TicksLine(
                ticks_line_channel=current_channel,
                color=_get_color(other_ch_counter),
                y_offset=other_ch_counter,
            )
            ticks_line.plot(ax[0])
            other_ch_counter += 1
