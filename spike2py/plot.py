import matplotlib.pyplot as plt
from typing import Literal, Tuple, List

import numpy as np

from spike2py import channels

COLOR = "black"
LINE_WIDTH = 3
FONTSIZE = 10
TICK_FIG_SIZE = (12, 4)
Y_TICK_VALUES = (0, 1)
Y_LINE_VALUES = (0.5, 0.5)
TICK_Y_LIMIT = (-2, 3)
CHAR_Y_VALUE = 1.1


def channel(spike2py_channel, save: Literal[True, False]) -> None:
    channel_type = repr(spike2py_channel).split()[0]
    _plot_channels()[channel_type](spike2py_channel)
    if save:
        _save_plot(spike2py_channel.channel_details)


def _plot_channels():
    return {
        "Event": _event,
        "Keyboard": _keyboard,
        "Waveform": _waveform,
        "Wavemark": _wavemark,
    }


def _save_plot(channel_details: "channels.ChannelDetails") -> None:
    fig_name = (
        f"{channel_details.subject_id}_"
        f"{channel_details.trial_name}_"
        f"{channel_details.name}.png"
    )
    fig_path = channel_details.path_save_figures / fig_name
    plt.savefig(fig_path)
    plt.close()


def _event(event: "channels.Event") -> None:
    plt.figure(figsize=TICK_FIG_SIZE)
    _plot_ticks(event.times)
    _plot_horiz_line(
        start=event.times[0],
        end=event.times[-1],
        ch_name=event.channel_details.name,
    )
    _finalise_plot(TICK_Y_LIMIT)


def _plot_ticks(times: np.ndarray) -> None:
    for time in times:
        _plot_tick(time)


def _plot_tick(time: float) -> None:
    plt.plot((time, time), Y_TICK_VALUES, linewidth=LINE_WIDTH, color=COLOR)


def _plot_horiz_line(start: float, end: float, ch_name: str) -> None:
    plt.plot(
        (start, end), Y_LINE_VALUES, linewidth=LINE_WIDTH, label=ch_name, color=COLOR
    )


def _finalise_plot(y_lim: Tuple[float, float] = None) -> None:
    if y_lim:
        plt.ylim(TICK_Y_LIMIT)
        plt.gca().axes.get_yaxis().set_visible(False)
    plt.xlabel("time (s)")
    plt.grid()
    plt.legend()
    plt.tight_layout()
    plt.show()


def _keyboard(keyboard: "channels.Keyboard") -> None:
    plt.figure(figsize=TICK_FIG_SIZE)
    _plot_ticks_and_codes(
        keyboard.times,
        keyboard.codes,
        keyboard.channel_details.name,
    )
    _finalise_plot(TICK_Y_LIMIT)


def _plot_ticks_and_codes(times: np.ndarray, codes: List[str], ch_name: str) -> None:
    for time, code in zip(times, codes):
        _plot_tick(time)
        _plot_text(time, code)
    _plot_horiz_line(start=times[0], end=times[-1], ch_name=ch_name)


def _plot_text(time: float, code: str) -> None:
    plt.text(time, CHAR_Y_VALUE, code, color=COLOR, fontsize=FONTSIZE)


def _waveform(waveform: "channels.Waveform") -> None:
    plt.figure(figsize=(12, 8))
    plt.plot(
        waveform.times,
        waveform.values,
        label=waveform.channel_details.name,
        color=COLOR,
    )
    units = waveform.channel_details.units if not None else "a.u."
    plt.ylabel(f"amplitude ({units})")
    _finalise_plot()


def _wavemark(wavemark: "channels.Wavemark") -> None:
    plt.figure(figsize=TICK_FIG_SIZE)
    plt.subplot(1, 14, (1, 12))
    _plot_ticks(wavemark.times)
    _plot_horiz_line(
        start=wavemark.times[0],
        end=wavemark.times[-1],
        ch_name=wavemark.channel_details.name,
    )
    _finalise_plot(TICK_Y_LIMIT)
    plt.subplot(1, 14, (13, 14))
    for action_potential in wavemark.action_potentials:
        plt.plot(action_potential, color=COLOR, alpha=0.5)
    _remove_xy_ticks_labels()


def _remove_xy_ticks_labels() -> None:
    plt.gca().axes.get_yaxis().set_visible(False)
    plt.gca().axes.get_xaxis().set_visible(False)
