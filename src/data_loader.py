import pandas as pd
from pathlib import Path
from typing import List
import numpy as np


def load_sensor_data(file_path: Path, session_name: str, is_stats: bool, column_names: List[str] | None = None, header_value: int = 0) -> pd.DataFrame:
    df = pd.read_csv(file_path, delimiter=',', header= header_value, names=column_names)

    # Check for Jitter
    t_raw = df["time"].values # nanoseconds time stamps

    # Calculate difference between consecutive time steps
    dt_nanos = np.diff(t_raw)
    dt_ms = dt_nanos / 1e6 # Convert nanoseconds to miliseconds

    # Compute statistics
    ideal_dt_ms = 10.0  # Expected 10ms for 100Hz
    mean_dt = np.mean(dt_ms)
    std_dt = np.std(dt_ms)
    min_dt = np.min(dt_ms)
    max_dt = np.max(dt_ms)

    if is_stats:
        print(f" Timestamp Jitter Analysis  of {session_name}")
        print(f"Total Samples: {len(t_raw)}")
        print(f"Ideal Interval: {ideal_dt_ms:.2f} ms")
        print(f"Mean Interval:  {mean_dt:.2f} ms")
        print(f"Std Deviation:  {std_dt:.2f} ms")
        print(f"Min Interval:   {min_dt:.2f} ms")
        print(f"Max Interval:   {max_dt:.2f} ms")

        #  Check if duplicate or backward timestamps exist (common OS glitches)
        backwards = np.sum(dt_nanos <= 0)
        if backwards > 0:
            print(f"WARNING: Found {backwards} zero or negative time intervals (timestamps out of order)!")
        else:
            print("Timestamps are strictly monotonic (no backward jumps).")

        # Calculate acceleration magnitude
        df["Acc_mag"] = np.sqrt(df["x"]**2 + df["y"]**2 + df["z"]**2)

    # Normalized time in seconds
    df["time_s"] = df["time"] / 1e9
    df["time_s_normalized"] = (df["time_s"] - df["time_s"].iloc[0]).round(4)
    return df

def load_xsens_file(filepath: Path) -> pd.DataFrame:

    df = pd.read_csv(filepath, comment="/", header=0)

    # Check PacketCounter continuity
    pc_diffs = df["PacketCounter"].diff().dropna()

    pc_diffs = pc_diffs.apply(
        lambda x: x + 65536 if x < 0 else x
    ).unique()

    if not (len(pc_diffs) == 1 and pc_diffs[0] == 1):
        print(
            f"[!] dropped frames detected! "
            f"Diff steps found: {pc_diffs}"
        )

    # Calculate acceleration magnitude
    df["Acc_mag"] = np.sqrt(df["Acc_X"]**2 + df["Acc_Y"]**2 + df["Acc_Z"]**2)

    # Normalized time in seconds
    counter = df["PacketCounter"].to_numpy(dtype=np.uint64)
    diff_counter = np.diff(counter).astype(np.int64)
    rollover = np.cumsum(diff_counter < -32768)
    counter_corrected = counter.copy()
    counter_corrected[1:] += rollover.astype(np.uint64) * 65536
    df["time_s_normalized"] = (counter_corrected - counter_corrected[0])/60

    return df
