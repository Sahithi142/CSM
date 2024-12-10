import numpy as np
import scipy.fft as sfft
import scipy.signal as sig
import matplotlib.pyplot as plt

SAMPLING_RATE = 44100 

def calculate_band_energy(freq_data, freq_range, sampling_rate, fft_size):
    start_idx = int(freq_range[0] * fft_size / sampling_rate)
    end_idx = int(freq_range[1] * fft_size / sampling_rate)
    return np.sum(np.abs(freq_data[start_idx:end_idx]) ** 2)

def apply_audio_filter(audio_data, freq_band, filter_kind="low", sampling_rate=SAMPLING_RATE):
    nyquist_limit = sampling_rate / 2
    if filter_kind == "low":
        b, a = sig.butter(4, freq_band[1] / nyquist_limit, 'low')
    elif filter_kind == "high":
        b, a = sig.butter(4, freq_band[0] / nyquist_limit, 'high')
    elif filter_kind == "band":
        b, a = sig.butter(4, [freq_band[0] / nyquist_limit, freq_band[1] / nyquist_limit], 'bandpass')
    return sig.lfilter(b, a, audio_data)

def compute_fft(audio_data, fft_size):
    fft_output = sfft.fft(audio_data[:fft_size])
    fft_magnitude = np.abs(fft_output)
    return fft_magnitude, fft_output

def band_equalizer(audio_data, fft_size, sampling_rate):
    fft_magnitude, freq_data = compute_fft(audio_data, fft_size)
    
    low_band_energy = calculate_band_energy(freq_data, LOW_FREQ_BAND, sampling_rate, fft_size)
    mid_band_energy = calculate_band_energy(freq_data, MID_FREQ_BAND, sampling_rate, fft_size)
    high_band_energy = calculate_band_energy(freq_data, HIGH_FREQ_BAND, sampling_rate, fft_size)
    
    total_band_energy = low_band_energy + mid_band_energy + high_band_energy
    target_energy_per_band = total_band_energy / 3
    
    low_gain = np.sqrt(target_energy_per_band / low_band_energy)
    mid_gain = np.sqrt(target_energy_per_band / mid_band_energy)
    high_gain = np.sqrt(target_energy_per_band / high_band_energy)
    
    low_band_adjusted = apply_audio_filter(audio_data, LOW_FREQ_BAND, "low", sampling_rate) * low_gain
    mid_band_adjusted = apply_audio_filter(audio_data, MID_FREQ_BAND, "band", sampling_rate) * mid_gain
    high_band_adjusted = apply_audio_filter(audio_data, HIGH_FREQ_BAND, "high", sampling_rate) * high_gain
    
    return low_band_adjusted + mid_band_adjusted + high_band_adjusted


LOW_FREQ_BAND = (0, 300)
MID_FREQ_BAND = (300, 2000)
HIGH_FREQ_BAND = (2000, SAMPLING_RATE // 2)

TARGET_NORMALIZED_ENERGY = 1
FFT_WINDOW_SIZE = 2048  

time_axis = np.linspace(0, 1, SAMPLING_RATE) 
test_signal = 0.5 * np.sin(2 * np.pi * 440 * time_axis) + 0.5 * np.sin(2 * np.pi * 1000 * time_axis)

processed_signal = band_equalizer(test_signal, FFT_WINDOW_SIZE, SAMPLING_RATE)

plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(time_axis[:500], test_signal[:500])
plt.title("Original Signal")
plt.subplot(2, 1, 2)
plt.plot(time_axis[:500], processed_signal[:500])
plt.title("Equalized Signal")
plt.tight_layout()
plt.show()
