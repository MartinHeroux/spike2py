import matplotlib.pyplot as plt


def event(details, times):
    plt.figure(figsize=(12, 4))
    for time in times:
        plt.plot([time, time], [0, 1], linewidth=3, color='k')
    plt.plot((times[0], times[-1]), (0.5, 0.5), color='k', linewidth=3, label=details.name)
    plt.gca().axes.get_yaxis().set_visible(False)
    plt.ylim(-2, 3)
    _finalise_plot()


def _finalise_plot():
    plt.xlabel('time (s)')
    plt.grid()
    plt.legend()
    plt.tight_layout()
    plt.show()


def keyboard(details, times, codes):
    plt.figure(figsize=(12, 4))
    for time, code in zip(times, codes):
        plt.plot([time, time], [0, 1], linewidth=3, color='k')
        plt.text(time, 1.1, code, color='k', fontsize=10)
    plt.plot((times[0], times[-1]), (-0.1, -0.1), color='k', linewidth=3, label=details.name)
    plt.gca().axes.get_yaxis().set_visible(False)
    plt.ylim(-2, 3)
    _finalise_plot()


def waveform(details, times, values):
    plt.figure(figsize=(12, 8))
    plt.plot(times, values, label=details.name)
    units = details.units if not None else 'a.u.'
    plt.ylabel(f'amplitude ({units})')
    _finalise_plot()


def wavemark(details, times, action_potentials):
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 14, (1, 12))
    for time in times:
        plt.plot([time, time], [0, 1], linewidth=3, color='k')
    plt.plot((times[0], times[-1]), (0.5, 0.5), color='k', linewidth=3, label=details.name)
    plt.gca().axes.get_yaxis().set_visible(False)
    plt.ylim(-2, 3)
    _finalise_plot()
    plt.subplot(1, 14, (13, 14))
    for action_potential in action_potentials:
        plt.plot(action_potential, color='k', alpha=0.5)
        plt.gca().axes.get_yaxis().set_visible(False)
        plt.gca().axes.get_xaxis().set_visible(False)

