import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


class ReadData:

    def __init__(self):
        self.logger_data = None
        self.putty_data = None

    def read_logger(self, path):
        self.logger_data = pd.read_csv(
            path,
            sep=";",
            decimal=",",
            lineterminator="\n",
        )
        print(self.logger_data)

    def read_putty(self, path):
        self.putty_data = pd.read_csv(
            path,
            header=None,
            delimiter=",",
            names=["float_value", "time"],
            on_bad_lines="skip",
        )
        print(self.putty_data)

    def performence_graphs(self):

        log_time = (
            np.linspace(0, 0.0005 * len(self.logger_data), len(self.logger_data)) * 1200
        )

        putty_time = (
            np.linspace(0, 0.001 * len(self.putty_data), len(self.putty_data)) * 960
        )

        for column_name, column_data in self.logger_data.items():
            if column_name not in ["Output/Input"]:
                try:
                    print(column_name)
                    plt.figure(figsize=(10, 4))
                    plt.plot(log_time, self.logger_data[column_name])
                    plt.xlabel("Time (s)")
                    plt.ylabel(column_name)
                    plt.title(f"{column_name} vs Time")
                    plt.grid(True)
                    plt.savefig(f"Graphs\{column_name}.png")
                    plt.close()
                except:
                    pass

        plt.figure(figsize=(10, 4))
        plt.plot(putty_time, self.putty_data["float_value"])
        plt.xlabel("Time (s)")
        plt.ylabel("Temp")
        plt.title(f"Temp vs Time")
        plt.grid(True)
        plt.savefig("Graphs\Temp.png")
        plt.close()


if __name__ == "__main__":
    read = ReadData()
    read.read_logger("Data\\usb_log_17.csv")
    read.read_putty("Data\\putty_stripped.log")
    read.performence_graphs()
