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

        # file to convert
        # please have a two column csv, with one coloum of Current, and one column of Time
        self.root = "HVBatteryCurrent_1Lap.xlsx"
        # name to save
        self.save_name = "WAVE_I_01"
        # number of points (fills up to 100 with empty lines), found issues when inputting 100 different lines
        self.points = 98

        # Scale Constant, reduces the peaks below a certain value
        self.scale_const = 0.85
        # Clamping Values, clamps outliers
        self.upper_clamp = 30

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
        ]
        # AC START, AC END,STAR FREQ, END FREQ , AC START ANGLE, DC START, DC END,SQUENCE POINT IN TIME

        self.saved = pd.DataFrame(0, columns=column_names, index=range(100))
        self.saved["H"] = 100

    def load(self):
        self.raw = pd.read_excel(self.root)
        print(self.raw.head())  # Display the first few rows of the DataFrame
        shape = self.raw.shape
        print("Number of rows:", shape[0])
        print("Number of columns:", shape[1])

    def convert(self, method="1"):
        signal_np = self.raw.to_numpy()
        decimation_factor = len(signal_np) // self.points

        # Decimation
        if method == "1":
            downsampled_signal = signal_np[::decimation_factor]

        # Max value
        elif method == "2":
            points_per_segment = len(signal_np) // self.points
            segments = signal_np[: points_per_segment * self.points].reshape(
                (self.points, points_per_segment, 2)
            )
            downsampled_current = np.max(segments[:, :, 1], axis=1)
            downsampled_time = segments[
                np.arange(self.points), np.argmax(segments[:, :, 1], axis=1), 0
            ]
            downsampled_signal = np.column_stack(
                (downsampled_time, downsampled_current)
            )

        # Scaling and clamping
        downsampled_signal[:, 1] *= self.scale_const
        downsampled_signal[:, 1] = np.clip(
            downsampled_signal[:, 1], 0, self.upper_clamp
        )

        self.sampled = pd.DataFrame(downsampled_signal, columns=["Time", "Current"])
        self.sampled = self.sampled.abs()
        original_integral = np.trapz(self.raw["Current"], x=self.raw["Time"])
        downsampled_integral = np.trapz(self.sampled["Current"], x=self.sampled["Time"])

        print(
            "error =",
            (downsampled_integral - original_integral) / original_integral,
            "%",
        )
        print(downsampled_integral, original_integral)

    def save(self):
        for index, row in self.sampled.iterrows():
            if index == self.points - 1:
                break
            current_f = round(float(row["Current"]), 2)
            current_g = round(float(self.sampled.at[index + 1, "Current"]), 2)
            self.saved.at[index, "F"] = current_f
            self.saved.at[index, "G"] = current_g

            time = round(
                (
                    round(float(self.sampled.at[index + 1, "Time"]), 2)
                    - round(float(row["Time"]), 2)
                )
                * 1000000,
                0,
            )
            self.saved.at[index, "H"] = time

        print(self.saved)
        self.saved.to_csv(
            f"HMI_FILES/{self.save_name}.csv",
            sep=";",
            decimal=",",
            index=False,
            header=False,
            lineterminator=";\n",
        )

        plt.plot(self.raw["Time"], self.raw["Current"])
        plt.plot(self.sampled["Time"], self.sampled["Current"])

        # plt.plot(self.saved["H"].cumsum() / 1000000, self.saved["F"])

        plt.xlabel("F")
        plt.ylabel("Cumulative Sum of H")
        plt.title("Plot of F against Cumulative Sum of H")
        plt.grid(True)
        plt.show()


if __name__ == "__main__":
    conv = BatteryConvert()
    conv.load()
    conv.convert()
    conv.save()
