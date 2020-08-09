import matplotlib.pyplot as plt

COLOR = 'black'
LINE_WIDTH = 3
FONTSIZE = 10
TICK_FIG_SIZE = (12, 4)
Y_TICK_VALUES = (0, 1)
Y_LINE_VALUES = (0.5, 0.5)
TICK_Y_LIMIT = (-2, 3)
CHAR_Y_VALUE = 1.1


def event(channel_details, event_times):
    plt.figure(figsize=TICK_FIG_SIZE)
    _plot_ticks(event_times)
    _plot_horiz_line(start=event_times[0],
                     end=event_times[-1],
                     ch_name=channel_details.name,
                     )
    _finalise_plot(TICK_Y_LIMIT)


def _plot_ticks(times):
    for time in times:
        _plot_tick(time)


def _plot_tick(time):
    plt.plot((time, time), Y_TICK_VALUES, linewidth=LINE_WIDTH, color=COLOR)


def _plot_horiz_line(start, end, ch_name):
    plt.plot((start, end), Y_LINE_VALUES,
             linewidth=LINE_WIDTH, label=ch_name, color=COLOR)


def _finalise_plot(y_lim=None):
    if y_lim:
        plt.ylim(TICK_Y_LIMIT)
        plt.gca().axes.get_yaxis().set_visible(False)
    plt.xlabel('time (s)')
    plt.grid()
    plt.legend()
    plt.tight_layout()
    plt.show()


def keyboard(channel_details, times, codes):
    plt.figure(figsize=TICK_FIG_SIZE)
    _plot_ticks_and_codes(times, codes, channel_details.name)
    _finalise_plot(TICK_Y_LIMIT)


def _plot_ticks_and_codes(times, codes, ch_name):
    for time, code in zip(times, codes):
        _plot_tick(time)
        _plot_text(time, code)
    _plot_horiz_line(start=times[0], end=times[-1], ch_name=ch_name)


def _plot_text(time, code):
    plt.text(time, CHAR_Y_VALUE, code, color=COLOR, fontsize=FONTSIZE)


def waveform(channel_details, times, values):
    plt.figure(figsize=(12, 8))
    plt.plot(times, values, label=channel_details.name, color=COLOR)
    units = channel_details.units if not None else 'a.u.'
    plt.ylabel(f'amplitude ({units})')
    _finalise_plot()


def wavemark(channel_details, times, action_potentials):
    plt.figure(figsize=TICK_FIG_SIZE)
    plt.subplot(1, 14, (1, 12))
    _plot_ticks(times)
    _plot_horiz_line(start=times[0],
                     end=times[-1],
                     ch_name=channel_details.name)
    _finalise_plot(TICK_Y_LIMIT)
    plt.subplot(1, 14, (13, 14))
    for action_potential in action_potentials:
        plt.plot(action_potential, color=COLOR, alpha=0.5)
    _remove_xy_ticks_labels()


def _remove_xy_ticks_labels():
    plt.gca().axes.get_yaxis().set_visible(False)
    plt.gca().axes.get_xaxis().set_visible(False)

