import pandas as pd
import numpy as np
from scipy.signal import resample_poly


def get_start_end_time(df: pd.DataFrame, samples: np.int64) -> tuple[float, float]:
    # find two values in which acc_mag is higest [1st and second peak ]
    # Since we want to find from start and finish of the signal, we can look only in 150 seconds from start and end time
    required_columns = ["time_s_normalized", "Acc_mag"]
    missing_columns = [column for column in required_columns
                       if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    time_start = df["time_s_normalized"].iloc[0]
    time_end = df["time_s_normalized"].iloc[-1]
    highest_acc_mag = 0
    for i in range(samples):  
        acc_mag = df["Acc_mag"].iloc[i]
        if acc_mag > highest_acc_mag:
            highest_acc_mag = acc_mag
            time_start = df["time_s_normalized"].iloc[i]

    highest_acc_mag = 0
    for i in range(len(df) - samples, len(df)):
        acc_mag = df["Acc_mag"].iloc[i]
        if acc_mag > highest_acc_mag:
            highest_acc_mag = acc_mag
            time_end = df["time_s_normalized"].iloc[i]
    return time_start, time_end


def trim_signal_with_time(df: pd.DataFrame, t_start: float, t_end: float) -> pd.DataFrame:
        
    required_columns = ["time_s_normalized"]
    missing_columns = [column for column in required_columns
                       if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    mask = (df["time_s_normalized"] >= t_start) & (df["time_s_normalized"] <= t_end)
    return df.loc[mask].reset_index(drop=True)


def downsample_with_nanos(df: pd.DataFrame, time_col: str, signal_cols: list, target_fs=60) -> pd.DataFrame:

    # Reviewer Comment: Sensor Logger on Android does not always sample at a uniform rate, 
    # while resample_poly assumes uniform samples. Please check timestamp jitter and interpolate first if needed.

    t_raw = df[time_col].values
    t0_nano = t_raw[0]
    tend_nano = t_raw[-1]

    # Create a uniform 100Hz timeline from start to finish
    dt_100Hz = int(1e9/100)
    uniform_100z_time = np.arange(t0_nano,tend_nano,dt_100Hz)

    # Interpolate signal columns onto this clean uniform grid
    uniform_data = {}
    for col in signal_cols:
        uniform_data[col] = np.interp(uniform_100z_time, t_raw, df[col].values)

    # 1. Compute anti-aliased polyphase resampling ratio (3/5 for 100Hz -> 60Hz)
    up = 3
    down = 5

    # 2. Resample signal columns
    resampled_data = {}
    for col in signal_cols:
        resampled_data[col] = resample_poly(uniform_data[col], up, down)

    num_samples = len(next(iter(resampled_data.values())))

    # Calculate step size in nanoseconds (1e9 ns / 60 Hz = 16_666_666.67 ns)
    ns_per_sample = 1e9 / target_fs

    # Create uniform nanosecond array starting at exact original baseline
    new_nanos = (
        t0_nano + np.arange(num_samples) * ns_per_sample).astype(np.int64)

    # 4. Construct downsampled DataFrame
    out_df = pd.DataFrame(resampled_data)
    out_df[time_col] = new_nanos

    out_df["Normalized_time_secs"] = ((out_df[time_col] - t0_nano) / 1e9).round(6)

    return out_df

def add_timestamp(XSens_df: pd.DataFrame, sensor_logger_timestamp: np.int64) -> pd.DataFrame:
    # 1. Target time step (1/60th of a second for 60 Hz)
    dt_sec = 1.0 / 60.0
    ns_per_packet = np.int64(1e9 // 60)

    # 2. Ensure packet counter starts cleanly at 0
    # Handle packet counter rollover if present
    pc_raw = XSens_df["PacketCounter"].values
    pc_diffs = np.diff(pc_raw, prepend=pc_raw[0])
    pc_diffs[pc_diffs < 0] += 65536  # Unwrap 16-bit rollover
    normalized_pc = np.cumsum(pc_diffs) - pc_diffs[0]

    # 3. Calculate absolute 19-digit nanoseconds cleanly
    XSens_df["timestamp_ns"] = sensor_logger_timestamp + (normalized_pc * ns_per_packet)

    # 4. Calculate relative seconds directly from the normalized counter step
    XSens_df["Normalized_time_secs"] = (normalized_pc * dt_sec).round(6)

    return XSens_df

