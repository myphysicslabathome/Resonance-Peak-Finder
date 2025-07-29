import numpy as np
import pandas as pd
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Read x, y data
df = pd.read_csv("Res2.csv")
x = df.iloc[:, 0].to_numpy()
y = df.iloc[:, 1].to_numpy()

# Define Gaussian function
def gaussian(x, a, x0, sigma, offset):
    return a * np.exp(-(x - x0)**2 / (2 * sigma**2)) + offset

# Detect peaks
peaks_indices, _ = find_peaks(y, prominence=0.1, distance=10)
peak_x = x[peaks_indices]
peak_y = y[peaks_indices]

# Plot original data
plt.figure(figsize=(12, 6))
plt.plot(x, y, label='Original Data')
plt.plot(peak_x, peak_y, 'o', color='red', markersize=6, label='Detected Peaks')

# Fit Gaussian to each peak with bounds
for i, idx in enumerate(peaks_indices):
    window_size = 50  # number of points on each side of the peak
    left = max(0, idx - window_size)
    right = min(len(x), idx + window_size)

    x_fit = x[left:right]
    y_fit = y[left:right]

    # Initial parameter guesses
    a_init = y[idx] - np.min(y_fit)
    x0_init = x[idx]
    sigma_init = (x[right-1] - x[left]) / 6
    offset_init = np.min(y_fit)
    p0 = [a_init, x0_init, sigma_init, offset_init]

    # Bounds: amplitude > 0, sigma > 0, offset ≥ 0
    lower_bounds = [0, x[left], 1e-3, 0]
    upper_bounds = [np.max(y_fit)*2, x[right-1], (x[right-1] - x[left]), np.max(y_fit)]

    try:
        popt, _ = curve_fit(gaussian, x_fit, y_fit, p0=p0, bounds=(lower_bounds, upper_bounds))
        a_fit, x0_fit, sigma_fit, offset_fit = popt

        # Plot the fitted curve
        x_fine = np.linspace(x_fit[0], x_fit[-1], 500)
        y_fine = gaussian(x_fine, *popt)
        plt.plot(x_fine, y_fine, '--', label=f'Gaussian Fit {i+1}')

        # Annotate peak center
        plt.annotate(f'{x0_fit:.1f} Hz', (x0_fit, gaussian(x0_fit, *popt)),
                     textcoords="offset points", xytext=(0, 10), ha='center', fontsize=9, color='blue')

        print(f"Peak {i+1}: Center = {x0_fit:.2f} Hz | Amplitude = {a_fit:.2f} | Sigma = {sigma_fit:.2f}")

    except RuntimeError:
        print(f"Peak {i+1}: Fit failed.")

plt.title('Frequency Response Spectrum with Constrained Gaussian Fits', fontweight='bold')
plt.xlabel('Frequency (Hz)', fontweight='bold')
plt.ylabel('Amplitude (Volt)', fontweight='bold')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
