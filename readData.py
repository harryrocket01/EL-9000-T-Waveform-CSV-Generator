import pandas as pd
import matplotlib.pyplot as plt


class ReadData:

    def __init__(self):
        pass

    def read_logger(self, path):
        logger_data = pd.read_csv(
            path,
            sep=";",
            decimal=",",
            lineterminator="\n",
        )
        print(logger_data)

        logger_data.plot()
        plt.show()

    def read_putty(self, path):
        putty_data = pd.read_csv(
            path,
            header=None,
            delimiter=",",
            names=["float_value", "int_value"],
            on_bad_lines="skip",
        )
        print(putty_data)
        putty_data.plot()
        plt.show()


if __name__ == "__main__":
    read = ReadData()
    read.read_logger("Data\\usb_log_15.csv")
    read.read_putty("Data\\putty.log")
