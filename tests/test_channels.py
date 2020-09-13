from pytest import approx

from spike2py import channels


def test_channels_event_init(channels_init, channels_mock):
    event = channels.Event(**channels_init["event"])
    assert event.info.name == channels_mock["event"]["info"].name
    assert (
        event.info.path_save_figures
        == channels_mock["keyboard"]["info"].path_save_figures
    )
    assert event.info.trial_name == channels_mock["keyboard"]["info"].trial_name
    assert event.info.subject_id == channels_mock["keyboard"]["info"].subject_id
    assert list(event.times) == list(channels_mock["event"]["times"])
    assert repr(event) == "Event channel"


def test_channels_keyboard_init(channels_init, channels_mock):
    keyboard = channels.Keyboard(**channels_init["keyboard"])
    assert keyboard.info.name == channels_mock["keyboard"]["info"].name
    assert (
        keyboard.info.path_save_figures
        == channels_mock["keyboard"]["info"].path_save_figures
    )
    assert keyboard.info.trial_name == channels_mock["keyboard"]["info"].trial_name
    assert keyboard.info.subject_id == channels_mock["keyboard"]["info"].subject_id
    assert list(keyboard.times) == list(channels_mock["keyboard"]["times"])
    assert keyboard.codes == channels_mock["keyboard"]["codes"]
    assert repr(keyboard) == "Keyboard channel"


def test_channels_waveform_init(channels_init, channels_mock):
    waveform = channels.Waveform(**channels_init["waveform"])
    assert "raw_values" in waveform.__dir__()
    assert waveform.info.name == channels_mock["waveform"]["info"].name
    assert (
        waveform.info.path_save_figures
        == channels_mock["waveform"]["info"].path_save_figures
    )
    assert waveform.info.trial_name == channels_mock["waveform"]["info"].trial_name
    assert waveform.info.subject_id == channels_mock["waveform"]["info"].subject_id
    assert list(waveform.times) == list(channels_mock["waveform"]["times"])
    assert waveform.info.units == channels_mock["waveform"]["info"].units
    assert list(waveform.values) == list(channels_mock["waveform"]["values"])
    assert (
        waveform.info.sampling_frequency
        == channels_mock["waveform"]["info"].sampling_frequency
    )
    assert repr(waveform) == "Waveform channel"


def test_channels_wavemark_init(channels_init, channels_mock):
    wavemark = channels.Wavemark(**channels_init["wavemark"])
    assert wavemark.info.name == channels_mock["wavemark"]["info"].name
    assert (
        wavemark.info.path_save_figures
        == channels_mock["wavemark"]["info"].path_save_figures
    )
    assert wavemark.info.trial_name == channels_mock["wavemark"]["info"].trial_name
    assert wavemark.info.subject_id == channels_mock["wavemark"]["info"].subject_id
    assert list(wavemark.times) == list(channels_mock["wavemark"]["times"])
    assert wavemark.info.units == channels_mock["wavemark"]["info"].units
    assert (
        wavemark.info.sampling_frequency
        == channels_mock["wavemark"]["info"].sampling_frequency
    )
    assert wavemark.action_potentials == channels_mock["wavemark"]["action_potentials"]
    actual_inst_fq = wavemark.inst_firing_frequency
    assert actual_inst_fq == approx(
        channels_mock["wavemark"]["instantaneous_firing_frequency"]
    )
    assert repr(wavemark) == "Wavemark channel"
