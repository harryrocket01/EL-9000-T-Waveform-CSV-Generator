import pandas as pd
import matplotlib.pyplot as plt
import subprocess
import sys
import numpy as np
from scipy import signal
import scipy.interpolate as interpolate

# subprocess.check_call([sys.executable, "-m", "pip", "install", "openpyxl"])


class BatteryConvert:

    def __init__(self):
        self.root = "HVBatteryCurrent_1Lap.xlsx"
        self.raw = None
        self.sampled = None
        column_names = [
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
        ]  # AC START, AC END,STAR FREQ, END FREQ , AC START ANGLE, DC START, DC END,SQUENCE POINT IN TIME

        self.saved = pd.DataFrame(0, columns=column_names, index=range(99))

    def load(self):

        self.raw = pd.read_excel(self.root)
        print(self.raw.head())  # Display the first few rows of the DataFrame
        shape = self.raw.shape
        print("Number of rows:", shape[0])
        print("Number of columns:", shape[1])

        self.raw.plot()

    def convert(self, method="1"):
        signal_np = self.raw.to_numpy()
        decimation_factor = len(signal_np) // 100

        # Decimation
        if method == "1":
            downsampled_signal = signal_np[::decimation_factor]
            downsampled_signal[:, 1] *= 0.85  # Multiply the second column by 0.85

        # Interpolation
        elif method == "2":
            points_per_segment = len(signal_np) // 100
            segments = signal_np[: points_per_segment * 100].reshape(
                (100, points_per_segment, 2)
            )
            downsampled_current = np.max(segments[:, :, 1], axis=1)
            downsampled_time = segments[
                np.arange(100), np.argmax(segments[:, :, 1], axis=1), 0
            ]
            downsampled_signal = np.column_stack(
                (downsampled_time, downsampled_current)
            )

        else:  # For method "3"
            points_per_segment = len(signal_np) // 100
            segments = signal_np[: points_per_segment * 100].reshape(
                (100, points_per_segment, 2)
            )
            downsampled_current = np.mean(segments[:, :, 1], axis=1)
            downsampled_time = segments[
                np.arange(100), np.argmax(segments[:, :, 1], axis=1), 0
            ]
            downsampled_signal = np.column_stack(
                (downsampled_time, downsampled_current)
            )

        self.sampled = pd.DataFrame(downsampled_signal, columns=["Time", "Current"])
        self.sampled.plot()

        original_integral = np.trapz(self.raw["Current"], x=self.raw["Time"])
        downsampled_integral = np.trapz(self.sampled["Current"], x=self.sampled["Time"])

        print("error =", downsampled_integral - original_integral)

    def save(self):
        for index, row in self.sampled.iterrows():
            if index == 100:
                break
            current_f = round(float(row["Current"]), 4)
            current_g = round(float(self.sampled.at[index + 1, "Current"]), 4)
            self.saved.at[index, "F"] = current_f
            self.saved.at[index, "G"] = current_g
            self.saved.at[index, "H"] = round(float(row["Current"]), 5) * 1_000_000

        print(self.saved)
        self.saved.to_csv(
            "HMI_FILES/Generate_Wave.csv", sep=";", decimal=".", index=False
        )
        self.saved[["F", "G"]].plot()
        plt.show()


if __name__ == "__main__":
    conv = BatteryConvert()
    conv.load()
    conv.convert()
    conv.save()
