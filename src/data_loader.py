import pandas as pd
from pathlib import Path
from typing import List
import numpy as np


def load_sensor_data(file_path: Path, column_names: List[str] | None = None, header_value: int = 0) -> pd.DataFrame:
    df = pd.read_csv(file_path, delimiter=',', header= header_value, names=column_names)
    return df

def load_xsens_file(filepath: Path) -> pd.DataFrame:

    df = pd.read_csv(
        filepath,
        comment="/",
        header=0
    )

    # Check PacketCounter continuity
    pc_diffs = df["PacketCounter"].diff().dropna()

    pc_diffs = pc_diffs.apply(
        lambda x: x + 65536 if x < 0 else x
    ).unique()

    if not (len(pc_diffs) == 1 and pc_diffs[0] == 1):
        print(
            f"[!] {filepath.name}: dropped frames detected! "
            f"Diff steps found: {pc_diffs}"
        )

    # Calculate acceleration magnitude
    df["Acc_mag"] = np.sqrt(
        df["Acc_X"]**2 +
        df["Acc_Y"]**2 +
        df["Acc_Z"]**2
    )

    return df
