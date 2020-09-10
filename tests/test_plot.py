import pytest

from spike2py import plot


def test_defaults():
    assert plot.LINE_WIDTH == 2
    assert plot.FIG_SIZE == (12, 4)
    assert plot.WAVEFORM_FIG_SIZE == (12, 8)
    assert plot.MAX_TRIAL_FIG_HEIGHT == 30
    assert plot.LEGEND_LOC == "upper right"
    assert plot.COLORS == [
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


@pytest.mark.parametrize(
    "index, color",
    [
        (0, "tab:blue"),
        (4, "tab:purple"),
        (9, "tab:cyan"),
        (13, "tab:red"),
        (18, "tab:olive"),
    ],
)
def test_get_color(index, color):
    assert plot._get_color(index) == color
