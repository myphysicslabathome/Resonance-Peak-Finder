import numpy as np
import pandas as pd
from scipy.signal import find_peaks
from scipy import interpolate
import matplotlib.pyplot as plt

# Read x,y data
df = pd. read_csv ("Res2.csv")
x = df.iloc [:, 0]
y = df.iloc [:, 1]

# Find peaks in the y-data
# 'prominence' can be adjusted to filter out less significant peaks
# 'distance' can be used to ensure a minimum separation between peaks
peaks_indices, _ = find_peaks(y, prominence=0.1, distance=10)

# Extract x and y values of the detected peaks
peak_x = x[peaks_indices]
peak_y = y[peaks_indices]


#f = interpolate.interp1d(x, y, kind='cubic')

# Plot the data and detected peaks
plt.figure(figsize=(10, 6))
plt.plot(x, y, label='Original Data')
plt.plot(peak_x, peak_y, 'o', color='red', markersize=8, label='Detected Peaks')
plt.title('Frequency Response Spectrum', fontweight='bold')
plt.xlabel('Frequency(Hz)', fontweight='bold')
plt.ylabel('Amplitude(Volt)', fontweight='bold')
for i in peaks_indices:
    plt.annotate(f'{peak_x[i]:.0f}', (peak_x[i], peak_y[i]), textcoords="offset points", xytext=(0,10), ha='center')
plt.legend()
plt.grid(False)
plt.show()

