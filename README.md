# Battery Signal Conversion Utility

This Python utility script is designed to convert battery current signals stored in Excel format into a simplified format suitable for battery simulation purposes. The script performs downsampling and signal conversion techniques to achieve this.

## Dependencies

Make sure you have the following dependencies installed:

- pandas
- matplotlib
- numpy
- scipy

You can install these dependencies using pip:

pip install pandas matplotlib numpy scipy


## Usage

1. Clone this repository to your local machine.
2. Place the Excel file containing the battery current signals (e.g., `HVBatteryCurrent_1Lap.xlsx`) in the same directory as the script.
3. Run the script using Python:


## Description

- `BatteryConvert` class: This class encapsulates the functionality for loading, converting, and saving battery current signals.

- `load()`: Loads the battery current signals from the Excel file specified in the `root` attribute.

- `convert()`: Performs signal conversion techniques such as decimation and interpolation to simplify the signals. The method parameter specifies the conversion method (default is method "1").

- `save()`: Saves the converted signals to a CSV file in the `HMI_FILES` directory. The file format follows specific guidelines for compatibility with battery simulation devices.

## Output
The converted signals are saved in a CSV file named Wave_1.csv in the HMI_FILES directory.

##License
This project is licensed under the MIT License - see the LICENSE file for details.

