from spike2py import channels


def test_channels_event_init(channels_init, channels_mock):
    event = channels.Event(**channels_init['event'])
    assert event.details.name == channels_mock['event']['details'].name
    assert list(event.times) == list(channels_mock['event']['times'])


def test_channels_keyboard_init(channels_init, channels_mock):
    keyboard = channels.Keyboard(**channels_init['keyboard'])
    assert keyboard.details.name == channels_mock['keyboard']['details'].name
    assert list(keyboard.times) == list(channels_mock['keyboard']['times'])
    assert keyboard.codes == channels_mock['keyboard']['codes']


def test_channels_waveform_init(channels_init, channels_mock):
    waveform = channels.Waveform(**channels_init['waveform'])
    assert waveform.details.name == channels_mock['waveform']['details'].name
    assert list(waveform.times) == list(channels_mock['waveform']['times'])
    assert waveform.details.units == channels_mock['waveform']['details'].units
    assert list(waveform.values) == list(channels_mock['waveform']['values'])
    assert waveform.details.sampling_frequency == \
           channels_mock['waveform']['details'].sampling_frequency


def test_channels_wavemark_init(channels_init, channels_mock):
    wavemark = channels.Wavemark(**channels_init['wavemark'])
    assert wavemark.details.name == channels_mock['wavemark']['details'].name
    assert list(wavemark.times) == list(channels_mock['wavemark']['times'])
    assert wavemark.details.units == channels_mock['wavemark']['details'].units
    assert wavemark.details.sampling_frequency == \
           channels_mock['wavemark']['details'].sampling_frequency
    assert wavemark.action_potentials == \
           channels_mock['wavemark']['action_potentials']
