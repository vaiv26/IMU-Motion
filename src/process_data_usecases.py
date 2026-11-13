import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, sosfiltfilt, find_peaks

def detect_steps(acc_df: pd.DataFrame, signal_cols: list, fs: int = 100):

    t_raw = acc_df["time"].values
    t0_nano = t_raw[0]
    tend_nano = t_raw[-1]

    # Create a uniform 100Hz timeline from start to finish
    dt_100Hz = int(1e9/fs)
    uniform_100z_time = np.arange(t0_nano,tend_nano,dt_100Hz)

    # Interpolate signal columns onto this clean uniform grid
    uniform_data = {}
    for col in signal_cols:
        uniform_data[col] = np.interp(uniform_100z_time, t_raw, acc_df[col].values)

    num_samples = len(uniform_100z_time)
    
    ns_per_sample = 1e9 / fs

    # Create uniform nanosecond array starting at exact original baseline
    new_nanos = (t0_nano + np.arange(num_samples) * ns_per_sample).astype(np.int64)

    # 4. Construct downsampled DataFrame
    out_df = pd.DataFrame(uniform_data)
    out_df["time"] = new_nanos

    out_df["time_s_normalized"] = ((out_df["time"] - t0_nano) / 1e9).round(6)

    acc_mag = np.sqrt(out_df["x"]**2 + out_df["y"]**2 + out_df["z"]**2)

    # Band-pass filter: initial walking-frequency range
    sos = butter(4, [0.5, 3.0], btype="bandpass", fs=fs, output="sos")

    filtered = sosfiltfilt(sos, acc_mag.to_numpy())

    # Initial peak-detection parameters
    peaks, properties = find_peaks(filtered, distance=int(0.35 * fs), prominence=0.5)

    return peaks, filtered, out_df