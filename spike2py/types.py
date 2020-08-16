from pathlib import Path
from typing import List, Dict, Union

import numpy as np

# read.py
mat_data = Dict[str, np.ndarray]
parsed_mat_data = Dict[str, dict]
parsed_event = Dict[str, Union[np.ndarray, str, Path]]
parsed_keyboard = Dict[str, Union[List[str], np.ndarray, str, Path]]
parsed_waveform = Dict[str, Union[int, np.ndarray, str, Path]]
parsed_wavemark = Dict[str, Union[int, List[int], str, np.ndarray, Path]]
parsed_spike2py_data = Dict[
    str, Union[parsed_event, parsed_keyboard, parsed_waveform, parsed_wavemark]
]
