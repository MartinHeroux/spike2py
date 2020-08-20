from typing import Literal, List, NamedTuple, Tuple

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from spike2py import channels

LINE_WIDTH = 2
FIG_SIZE = (12, 4)
WAVEFORM_FIG_SIZE = (12, 8)
MAX_TRIAL_FIG_HEIGHT = 30
LEGEND_LOC = "upper right"
FIG_HEIGHT_INCREMENT_LOOKUP = {
    "event": 2,
    "keyboard": 2,
    "waveform": 4,
    "wavemark": 2,
}
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

matplotlib.rcParams.update({"font.size": 14})


class TicksLine:
    def __init__(self, spike2py_channel, color=COLORS[0], offset=0):

        self.ch = spike2py_channel
        self.color = color
        self.offset = offset

        self.ch_type = repr(spike2py_channel).split()[0]
        self.line_start_end = (self.ch.times[0], self.ch.times[-1])
        self.line_y_vals = (0.5 + offset, 0.5 + offset)
        self.tick_y_vals = (0.2 + offset, 0.8 + offset)

    def plot(self, ax):
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
        if (self.ch_type == "Wavemark") and ax2:
            self._plot_action_potentials(ax2)

        plt.tight_layout()

    def _plot_ticks_line(self, ax1):
        for time in self.ch.times:
            ax1.plot(
                (time, time), self.tick_y_vals, linewidth=LINE_WIDTH, color=self.color
            )
        ax1.plot(
            self.line_start_end,
            self.line_y_vals,
            linewidth=LINE_WIDTH,
            label=self.ch.details.name,
            color=self.color,
        )

    def _plot_codes(self, ax1):
        for time, code in zip(self.ch.times, self.ch.codes):
            ax1.text(
                time, self.tick_y_vals[1] + 0.2, code, color=self.color, fontsize=10
            )

    def _plot_action_potentials(self, ax2):
        for action_potential in self.ch.action_potentials:
            ax2.plot(action_potential, color=self.color, alpha=0.5)
        ax2.get_yaxis().set_visible(False)
        ax2.get_xaxis().set_visible(False)

    def _finalise_plot(self, ax1):
        ax1.legend(loc=LEGEND_LOC)
        ax1.set_xlabel("time (s)")
        ax1.grid()
        ax1.get_yaxis().set_visible(False)


def channel(spike2py_channel, save: Literal[True, False]) -> None:
    """Interface to plot individual channels."""
    if len(spike2py_channel.times) == 0:
        print("{spike2py_channel.details.name} channel has no data to plot.")
        return
    channel_type = repr(spike2py_channel).split()[0]
    if channel_type == "Waveform":
        _plot_waveform(spike2py_channel)
    else:
        _plot_ticks_line(TicksLine(spike2py_channel))
    plt.show()
    if save:
        _save_plot(spike2py_channel.details)


def _plot_waveform(waveform: "channels.Waveform", color=COLORS[0]) -> None:
    fig, ax = plt.subplots(figsize=WAVEFORM_FIG_SIZE)
    ax.plot(waveform.times, waveform.values, label=waveform.details.name, color=color)
    ax.set_xlim(waveform.times[0], waveform.times[-1])
    units = waveform.details.units if waveform.details.units is True else "a.u."
    ax.set_ylabel(f"amplitude ({units})")
    ax.legend(loc=LEGEND_LOC)
    ax.set_xlabel("time (s)")
    ax.grid()


def _plot_ticks_line(ticks_line):
    if ticks_line.ch_type == "Wavemark":
        fig, ax = plt.subplots(
            1, 2, figsize=FIG_SIZE, gridspec_kw={"width_ratios": [3, 1]}
        )
        ticks_line.plot(ax)
    else:
        fig, ax = plt.subplots(figsize=FIG_SIZE)
        ticks_line.plot(ax)


def _save_plot(channel_details: "channels.ChannelDetails") -> None:
    fig_name = (
        f"{channel_details.subject_id}_"
        f"{channel_details.trial_name}_"
        f"{channel_details.name}.png"
    )
    fig_path = channel_details.path_save_figures / fig_name
    plt.savefig(fig_path)
    plt.close()


#
# def trial(spike2py_trial, save: Literal[True, False]) -> None:
#     fig_height,  other_channel_types_plottable = _fig_height_based_on_channel_number_and_types(spike2py_trial)
#     (
#         n_subplots,
#         subplot_other_channel_types,
#     ) = _subplots_based_on_channel_number_and_types(spike2py_trial, other_channel_types_plottable)
#
#     plt.subplots(ncols=n_subplots, figsize=(12, fig_height))
#     _plot_trial(spike2py_trial, n_subplots, subplot_other_channel_types)
#
#
# def _fig_height_based_on_channel_number_and_types(spike2py_trial) -> Tuple[int, bool]:
#     fig_height = 4
#     other_channel_types_plottable = False
#     for channel, channel_type in spike2py_trial.channels:
#         current_channel = spike2py_trial.__getattribute__(channel)
#         if channel_type in ["event", "keyboard", "wavemark"]:
#             if len(current_channel.times) != 0:
#                 other_channel_types_plottable = True
#                 fig_height += FIG_HEIGHT_INCREMENT_LOOKUP[channel_type]
#         else:
#             fig_height += FIG_HEIGHT_INCREMENT_LOOKUP[channel_type]
#     fig_height = min(fig_height, MAX_TRIAL_FIG_HEIGHT)
#     return fig_height, other_channel_types_plottable
#
#
# def _subplots_based_on_channel_number_and_types(spike2py_trial, other_channel_types_plottable) -> tuple:
#     channel_types = [channel_type for _, channel_type in spike2py_trial.channels]
#     n_waveforms = sum(
#         [True for channel_type in channel_types if channel_type == "waveform"]
#     )
#     if other_channel_types_plottable:
#         n_other_channel_types = sum(
#         [
#             True
#             for channel_type in channel_types
#             if channel_type in ["event", "keyboard", "wavemark"]
#         ]
#         )
#     else:
#         n_other_channel_types = 0
#     if n_other_channel_types == 0:
#         subplot_other_channel_types = None
#         n_subplots = n_waveforms
#     else:
#         subplot_other_channel_types = 1
#         n_subplots = n_waveforms + 1
#     return n_subplots, subplot_other_channel_types
#
#
# def _plot_trial(spike2py_trial, n_subplots, subplot_other_channel_types):
#     waveform_subplot_counter = 0
#     other_channel_type_counter = 0
#     x_lim = None
#     x_lim_found = False
#     for channel, channel_type in spike2py_trial.channels:
#         current_channel = spike2py_trial.__getattribute__(channel)
#         if len(current_channel.times) != 0:
#             if channel_type == 'waveform':
#                 plt.subplot(n_subplots, 1, n_subplots - waveform_subplot_counter)
#                 _plot_waveform_data(current_channel, colors[waveform_subplot_counter-1])
#                 if waveform_subplot_counter == 0:
#                     _add_xlabel()
#                 else:
#                     plt.gca().axes.tick_params(labelbottom=False)
#                 waveform_subplot_counter += 1
#                 _finalise_plot()
#                 if not x_lim_found:
#                     x_lim = (current_channel.times[0], current_channel.times[-1])
#                     x_lim_found = False
#             if (channel_type == 'event') or (channel_type == 'wavemark'):
#                 plt.subplot(n_subplots, 1, subplot_other_channel_types)
#                 ticks_line = TicksLine(
#                     times=current_channel.times,
#                     name=current_channel.details.name,
#                     start_end=(current_channel.times[0], current_channel.times[-1]),
#                     color=colors[other_channel_type_counter],
#                     tick_y_vals=(other_channel_type_counter, other_channel_type_counter + 1),
#                     line_y_vals=(other_channel_type_counter + 0.5, other_channel_type_counter + 0.5))
#                 _plot_ticks(ticks_line)
#                 _plot_horiz_line(ticks_line)
#                 other_channel_type_counter += 1
#             if channel_type == 'keyboard':
#                 plt.subplot(n_subplots, 1, subplot_other_channel_types)
#                 ticks_line = TicksLine(
#                     times=current_channel.times,
#                     name=current_channel.details.name,
#                     start_end=(current_channel.times[0], current_channel.times[-1]),
#                     color=colors[other_channel_type_counter],
#                     tick_y_vals=(other_channel_type_counter, other_channel_type_counter + 1),
#                     codes=current_channel.codes,
#                     code_y_val=other_channel_type_counter + 1.1,
#                     line_y_vals=(other_channel_type_counter + 0.5, other_channel_type_counter + 0.5))
#                 _plot_ticks(ticks_line)
#                 _plot_horiz_line(ticks_line)
#                 _plot_codes(ticks_line)
#                 other_channel_type_counter += 1
#     if subplot_other_channel_types:
#         if x_lim:
#             plt.xlim(x_lim)
#         plt.subplot(n_subplots, 1, subplot_other_channel_types)
#         plt.grid()
#         plt.gca().axes.tick_params(labelbottom=False, labelleft=False)
#     plt.show()
#
