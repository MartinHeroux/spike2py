from spike2py import channels


def test_channels_event_init(channels_init, channels_mock):
    event = channels.Event(**channels_init["event"])
    assert event.details.name == channels_mock["event"]["details"].name
    assert event.details.path_figures == channels_mock["keyboard"]["details"].path_figures
    assert event.details.trial_name == channels_mock["keyboard"]["details"].trial_name
    assert event.details.subject_id == channels_mock["keyboard"]["details"].subject_id
    assert list(event.times) == list(channels_mock["event"]["times"])
    assert repr(event) == "Event channel"


def test_channels_keyboard_init(channels_init, channels_mock):
    keyboard = channels.Keyboard(**channels_init["keyboard"])
    assert keyboard.details.name == channels_mock["keyboard"]["details"].name
    assert keyboard.details.path_figures == channels_mock["keyboard"]["details"].path_figures
    assert (
        keyboard.details.trial_name == channels_mock["keyboard"]["details"].trial_name
    )
    assert (
        keyboard.details.subject_id == channels_mock["keyboard"]["details"].subject_id
    )
    assert list(keyboard.times) == list(channels_mock["keyboard"]["times"])
    assert keyboard.codes == channels_mock["keyboard"]["codes"]
    assert repr(keyboard) == "Keyboard channel"


def test_channels_waveform_init(channels_init, channels_mock):
    waveform = channels.Waveform(**channels_init["waveform"])
    assert "raw_values" in waveform.__dir__()
    assert waveform.details.name == channels_mock["waveform"]["details"].name
    assert waveform.details.path_figures == channels_mock["waveform"]["details"].path_figures
    assert (
        waveform.details.trial_name == channels_mock["waveform"]["details"].trial_name
    )
    assert (
        waveform.details.subject_id == channels_mock["waveform"]["details"].subject_id
    )
    assert list(waveform.times) == list(channels_mock["waveform"]["times"])
    assert waveform.details.units == channels_mock["waveform"]["details"].units
    assert list(waveform.values) == list(channels_mock["waveform"]["values"])
    assert (
        waveform.details.sampling_frequency
        == channels_mock["waveform"]["details"].sampling_frequency
    )
    assert repr(waveform) == "Waveform channel"


def test_channels_wavemark_init(channels_init, channels_mock):
    wavemark = channels.Wavemark(**channels_init["wavemark"])
    assert wavemark.details.name == channels_mock["wavemark"]["details"].name
    assert wavemark.details.path_figures == channels_mock["wavemark"]["details"].path_figures
    assert (
        wavemark.details.trial_name == channels_mock["wavemark"]["details"].trial_name
    )
    assert (
        wavemark.details.subject_id == channels_mock["wavemark"]["details"].subject_id
    )
    assert list(wavemark.times) == list(channels_mock["wavemark"]["times"])
    assert wavemark.details.units == channels_mock["wavemark"]["details"].units
    assert (
        wavemark.details.sampling_frequency
        == channels_mock["wavemark"]["details"].sampling_frequency
    )
    assert wavemark.action_potentials == channels_mock["wavemark"]["action_potentials"]
    actual_inst_fq = [int(value) for value in wavemark.inst_firing_frequency * 100000]
    expected_inst_fq = [int(value) for value in wavemark.inst_firing_frequency * 100000]
    assert actual_inst_fq == expected_inst_fq
    assert repr(wavemark) == "Wavemark channel"
