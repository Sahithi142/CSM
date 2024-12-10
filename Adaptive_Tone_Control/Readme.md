# Adaptive Tone Control

## Task

ad_ton_con.py Python script implements an audio band equalizer using Fast Fourier Transform (FFT) and filtering techniques. The equalizer processes an audio signal by dividing it into three frequency bands (low, mid, and high), calculates the energy in each band, and adjusts them to balance the energy across bands.

## What I did

- Generated a synthetic test signal by combining two sine waves at 440 Hz and 1000 Hz for low and mid frequencies, respectively.
- Implemented FFT-based band energy calculation to measure energy in low, mid, and high frequency bands.
- Designed and applied filters (low-pass, band-pass, and high-pass) to isolate the frequency bands.
- Calculated gain factors for each band to balance the energy across the bands.
- Applied gain adjustments to the filtered bands and reconstructed the equalized signal.
- Visualized the results by plotting the original and equalized signals for comparison.

## Exploration

While experimenting with different FFT window sizes and settings in my script, I found that using a window length of 20–50 ms (like 2048 samples at 44.1 kHz) gave the best balance between clear frequency details and quick responsiveness. Shorter windows (512–1024 samples) responded faster to sudden changes, but they lost some of the finer frequency details. On the other hand, longer windows (4096 samples) provided better frequency resolution but felt slow to react.

For tone adjustments, I tried different smoothing rates and found that smoothing over 100–200 ms (0.1–0.5 seconds) created natural transitions without any choppy or awkward effects. Instead of relying on peak values, using the averaged energy of each frequency band made everything feel much more stable, avoiding overreacting to short momentary.
