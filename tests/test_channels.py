from spike2py import channels


def test_channels_event_init(channels_init):
    event = channels.Event(**channels_init['event'])
    assert event.details.name == channels_init['event']['details'].name
    assert event.details.trial == channels_init['event']['details'].trial
    assert list(event.times) == list(channels_init['event']['times'])


def test_channels_keyboard_init(channels_init):
    keyboard = channels.Keyboard(**channels_init['keyboard'])
    assert keyboard.details.name == channels_init['keyboard']['details'].name
    assert keyboard.details.trial == channels_init['keyboard']['details'].trial
    assert list(keyboard.times) == list(channels_init['keyboard']['times'])
    assert keyboard.codes == channels_init['keyboard']['codes']


def test_channels_waveform_init(channels_init):
    waveform = channels.Waveform(**channels_init['waveform'])
    assert waveform.details.name == channels_init['waveform']['details'].name
    assert waveform.details.trial == channels_init['waveform']['details'].trial
    assert list(waveform.times) == list(channels_init['waveform']['times'])
    assert waveform.details.units == channels_init['waveform']['details'].units
    assert list(waveform.values) == list(channels_init['waveform']['values'])
    assert waveform.details.sampling_frequency == channels_init['waveform']['details'].sampling_frequency


def test_channels_wavemark_init(channels_init):
    wavemark = channels.Wavemark(**channels_init['wavemark'])
    assert wavemark.details.name == channels_init['wavemark']['details'].name
    assert wavemark.details.trial == channels_init['wavemark']['details'].trial
    assert list(wavemark.times) == list(channels_init['wavemark']['times'])
    assert wavemark.details.units == channels_init['wavemark']['details'].units
    assert wavemark.details.sampling_frequency == channels_init['wavemark']['details'].sampling_frequency
    assert wavemark.action_potentials == channels_init['wavemark']['action_potentials']
