import numpy as np
import scipy.io.wavfile as wavfile
import sounddevice as sd

def generate_sine_wave(frequency, duration, amplitude, sample_rate):
    """Generate a sine wave with the given frequency, duration, amplitude, and sample rate."""
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = amplitude * np.sin(2 * np.pi * frequency * t)
    return wave.astype(np.int16)

def generate_clipped_sine_wave(frequency, duration, amplitude, sample_rate):
    """Generate a clipped sine wave."""
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = amplitude * np.sin(2 * np.pi * frequency * t)
    
    # Clip to ¼ max amplitude (-8192 to 8192)
    clipped_wave = np.clip(wave, -8192, 8192)
    return clipped_wave.astype(np.int16)

def save_wave(filename, wave, sample_rate):
    """Save the generated wave to a WAV file."""
    wavfile.write(filename, sample_rate, wave)
    print(f"Saved {filename}")

def play_wave(wave, sample_rate, wave_name):
    """Play the given wave directly through the audio output."""
    print(f"Playing {wave_name}...")
    sd.play(wave, sample_rate)
    sd.wait()

def main():
    # Wave specifications
    frequency = 440          # Hz
    duration = 1              # second
    sample_rate = 48000       # samples per second
    amplitude = 8192          # ¼ max 16-bit amplitude

    # Generate and save the sine wave
    sine_wave = generate_sine_wave(frequency, duration, amplitude, sample_rate)
    save_wave("sine.wav", sine_wave, sample_rate)

    # Generate and save the clipped sine wave
    clipped_wave = generate_clipped_sine_wave(frequency, duration, amplitude * 2, sample_rate)
    save_wave("clipped.wav", clipped_wave, sample_rate)

    # Play both waves sequentially
    play_wave(sine_wave, sample_rate, "Sine Wave")
    play_wave(clipped_wave, sample_rate, "Clipped Sine Wave")

if __name__ == "__main__":
    main()
