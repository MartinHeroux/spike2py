import numpy as np


from spike2py import channels


def test_channels_event_init(channels_init):
    event = channels.Event(**channels_init['event'])
    assert event.name == channels_init['event']['name']
    assert event.trial_name == channels_init['event']['trial_name']
    assert list(event.times) == list(channels_init['event']['times'])


def test_channels_keyboard_init(channels_init):
    keyboard = channels.Keyboard(**channels_init['keyboard'])
    assert keyboard.name == channels_init['keyboard']['name']
    assert keyboard.trial_name == channels_init['keyboard']['trial_name']
    assert list(keyboard.times) == list(channels_init['keyboard']['times'])
    assert keyboard.codes == channels_init['keyboard']['codes']


def test_channels_waveform_init(channels_init):
    waveform = channels.Waveform(**channels_init['waveform'])
    assert waveform.name == channels_init['waveform']['name']
    assert waveform.trial_name == channels_init['waveform']['trial_name']
    assert list(waveform.times) == list(channels_init['waveform']['times'])
    assert waveform.units == channels_init['waveform']['units']
    assert list(waveform.values) == list(channels_init['waveform']['values'])
    assert waveform.sampling_frequency == channels_init['waveform']['sampling_frequency']


def test_channels_wavemark_init(channels_init):
    wavemark = channels.Wavemark(**channels_init['wavemark'])
    assert wavemark.name == channels_init['wavemark']['name']
    assert wavemark.trial_name == channels_init['wavemark']['trial_name']
    assert list(wavemark.times) == list(channels_init['wavemark']['times'])
    assert wavemark.units == channels_init['wavemark']['units']
    assert wavemark.sampling_frequency == channels_init['wavemark']['sampling_frequency']
    assert wavemark.action_potentials == channels_init['wavemark']['action_potentials']
