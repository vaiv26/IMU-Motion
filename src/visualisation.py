import matplotlib.pyplot as plt
import pandas as pd
from numpy.typing import NDArray
from pandas import Series
from typing import Any

def plot_acceleration_magnitude_with_lines(df:pd.DataFrame, time_start, time_end, acc_mag: NDArray[Any], name: str, time_col_name: str):

    plt.figure(figsize=(12, 4))
    plt.ticklabel_format(useOffset=False, style="plain")
    plt.axvline(time_start, color="green", linestyle="--", linewidth=0.5, label=f"trim start ({time_start:.2f}s)")
    plt.axvline(time_end, color="red", linestyle="--", linewidth=0.5, label=f"trim end ({time_end:.2f}s)")
    plt.plot(df[time_col_name], acc_mag, label="Acc magnitude")
    plt.xlabel("Time (s)")
    plt.ylabel("Accelerometer reading magnitude")
    plt.title(f"Sensor accelerometer - {name}")
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_acceleration_magnitude(df:pd.DataFrame, acc_mag: NDArray[Any], name: str, time_col_name: str):

    plt.figure(figsize=(12, 4))
    plt.plot(df[time_col_name], acc_mag, label="Acc magnitude right wrist")
    plt.xlabel("Time (s)")
    plt.ylabel("Accelerometer reading magnitude")
    plt.title(f"XSens Sensor accelerometer for right wrist of {name}")
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_acceleration_magnitude_with_checkpoints(step_logger_df:pd.DataFrame, time_col: pd.Series, mag_signal: NDArray[Any], title: str):

    plt.figure(figsize=(12, 4))
    plt.ticklabel_format(useOffset=False, style="plain")

    # Plot Accelerometer Signal
    plt.plot(time_col, mag_signal, label="Acc Magnitude", color="C0")

    # Loop over each checkpoint in the step logger DataFrame
    for idx, row in step_logger_df.iterrows():
        event_time =  round((row['time']/ 1e3),4)
        checkpoint_label = str(row["Checkpoint"]).strip()

        # 1. Draw vertical event line
        line_label = "Sensor Logger Event" if idx == 0 else ""
        plt.axvline(
            x=event_time,
            color="red",
            linestyle="--",
            alpha=0.6,
            linewidth=1.2,
            label=line_label,
        )

    plt.xlabel("Time (ms)")
    plt.ylabel("Acceleration ($m/s^2$)")
    plt.title(f"{title}")
    plt.legend(loc="upper right")
    plt.tight_layout()
    plt.show()