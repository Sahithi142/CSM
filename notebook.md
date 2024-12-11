# Fourier Transform and DFT Concepts

## 1. Sound Representation
- Every sound can be decomposed into a sum of sinusoids (Fourier’s Theorem).  

## 2. Frequency & Time Domain  
- A time-domain signal \(f(t)\) maps to a frequency-domain representation \( \hat{f}(\omega) \).  

## 3. Complex Representation  
- A frequency is expressed as a complex number:  
  \[ f(\omega) = a + bi \]  
  Amplitude: \( |f(\omega)| = \sqrt{a^2 + b^2} \)  
  Phase: \( \theta(f(\omega)) = \tan^{-1}(b / a) \)  

## 4. Euler’s Formula  
- Sinusoids in complex exponential form:  
  \[ e^{i(\omega t + \theta)} = \cos(\omega t + \theta) + i \sin(\omega t + \theta) \]  

## 5. Fourier Transform (FT)  
- Converts time-domain signal to frequency-domain:  
  \[ \hat{f}(\omega) = \int_{-\infty}^{\infty} f(t) e^{-i \omega t} \, dt \]  

## 6. Inverse Fourier Transform  
- Converts frequency-domain signal back to time-domain:  
  \[ f(t) = \frac{1}{2\pi} \int_{-\infty}^{\infty} \hat{f}(\omega) e^{i \omega t} \, d\omega \]  

## 7. Discrete Fourier Transform (DFT)  
- DFT for discrete signals:  
  \[ X[k] = \sum_{n=0}^{N-1} x[n] e^{-i 2\pi k n / N} \]  

## 8. Goertzel Filter  
- Optimized DFT for specific frequencies.  

## 9. Fast Fourier Transform (FFT)  
- FFT reduces DFT complexity to \(O(N \log N)\).  

## 10. Windowing  
- Smooths signal edges using a window function:  
  \[ \text{Sine window:} \quad x[n] \cdot \sin\left(\frac{\pi n}{N}\right) \]  

## 11. Harmonics in Waves  
- **Square wave:** Odd harmonics (e.g., \(3f, 5f\)).  
  \[ x(t) = \sin(\omega t) + \frac{1}{3} \sin(3 \omega t) + \frac{1}{5} \sin(5 \omega t) + \ldots \]  
- **Triangle wave:** Decreasing odd harmonics.  

## 12. Frequency Resolution  
- Depends on sampling rate and signal length.  

## 13. Applications  
- **Frequency Analysis:** Identifies spectral peaks.  
- **Filtering:** Adjusts frequency bins and performs inverse DFT.  
- **Lossy Compression:** Removes unneeded frequencies based on psychoacoustics.  

## 14. Overlapping Windows  
- Use overlapping DFT windows to track frequency changes over time.  

## 15. Discrete Cosine Transform (DCT)  
- Used in compression (e.g., MPEG) by discarding phase information.

# Sound Synthesis and Filters

## 1. Synthesis vs Analysis  
- **Synthesis:** Process of creating sounds (opposite of analysis).  
- **Filters:** Modify amplitude/phase of sound frequencies (e.g., tone control, equalizers).  

## 2. Popular Filter Types  
- **Low Pass:** Allows low frequencies, blocks high ones.  
- **High Pass:** Allows high frequencies, blocks low ones.  
- **Bandpass:** Allows a specific range of frequencies.  
- **Band Notch:** Blocks a specific range of frequencies.

## 3. Units and Normalization  
- Frequencies range from 0 to 1 (where 1 is Nyquist limit).  
- Amplitude:  
  - Time domain: \([-1, 1]\)  
  - Frequency domain: \([0, 1]\)  

## 4. Analog vs Digital Filters  
- **Analog Filters:** Use resistors, capacitors, etc., but are less flexible.  
- **Digital Filters:** Offer higher precision and flexibility using software.

## 5. FIR and IIR Filters  
- **FIR (Finite Impulse Response):**  
  - Impulse response eventually becomes zero.  
  - No feedback from previous outputs.  

- **IIR (Infinite Impulse Response):**  
  - Uses past outputs in feedback loop.  
  - More efficient but harder to design and stabilize.

## 6. DFT Filters  
- Converts signal to frequency domain, scales unwanted frequencies, and converts back.  
- FFT is used to optimize DFT to \(O(N \log N)\).

## 7. Key Concepts in Music Notes  
- **Octave:** Doubling of frequency from one note to the next.  
- **12-tone scale:** Divides each octave into 12 parts.  
  - \( \text{note}_i(f) = f \cdot 2^{i / 12} \)

## 8. MIDI Key Numbers  
- MIDI key 69 = A4 (440 Hz).  
- Notes are named with sharps (♯) or flats (♭), e.g., A♯/B♭.

## 9. Sample MIDI Key Frequencies  
- **A4 (69):** 440 Hz  
- **C5 (72):** 523.25 Hz  
- **G5 (79):** 783.99 Hz  
- **A5 (81):** 880 Hz  

## 10. Polyphony and Monophony  
- **Polyphonic:** Multiple notes played simultaneously.  
- **Monophonic:** One note played at a time.

## 11. Note Timing  
- Notes have **on** and **off times** (start and duration).  
- Typical duration: 4 ms or more.  

## 12. Anti-Aliasing Filters  
- Used to prevent aliasing during resampling (DAC/ADC).

## 13. Linear Time-Invariant (LTI) Systems  
- LTI filters produce linear output with no distortion.  
- Output depends only on the input, not on the input time.

## 14. Frequency Modulation (FM)  
- Modifies frequency over time, used in advanced synthesis.

## 15. Applications of Filters  
- Tone shaping, resampling, and anti-aliasing.  
- Used in equalizers, effects (like "wah-wah"), and compression.



## Portfolio Notebook Entry: Introduction on Zulip

## Task: Posted an introduction in the #introductions stream on Zulip.

## Content of the Introduction:
"Hi everyone! I'm Sahithi Mothe. I have a passion for exploring technology, and I'm excited to learn more about computers and sound through this course. My background involves experimenting with software and digital tools, and I'm curious to see how sound and music come together with technology. Looking forward to learning and collaborating with all of you!"

## Reflection:

- I felt good sharing my background and interests with my peers.
- It was an opportunity to connect with others and learn about their journeys.
- I’m excited to contribute to discussions and make the most of this course

## What I learned from the course

I learned how digital sound is created and processed. I now understand how audio is captured using sampling and quantization, turning sound waves into digital data. Concepts like frequency and amplitude started to make more sense, especially in how they shape the sounds we hear.

Learned practical ways to work with audio, like using filters and algorithms to change or create sounds. All this showed me how programming can bring these concepts to life and gave me a clearer picture of how sound is represented and manipulated digitally. It was great learning audio processing and experimenting with sound.

## Portfolio Notebook Entry: Adaptive Tone Control

## Task: Implemented an audio equalizer to balance sound energy across frequency bands using FFT and filtering techniques.

## What I Did:

- Generated a test signal combining sine waves at 440 Hz and 1000 Hz to represent low and mid frequencies.
- Used FFT to calculate energy in low (0–300 Hz), mid (300–2000 Hz), and high (2000+ Hz) frequency bands.
- Designed and applied filters (low-pass, band-pass, and high-pass) to isolate these bands.
- Adjusted band energies by calculating gain factors to balance them evenly.
- Reconstructed the signal and visualized comparing the original and equalized versions.

## Reflection:

This task deepened my understanding of audio processing and its connection to concepts like compression and equalization. I also gained insights into how parameter tuning affects performance and output quality.

## Portfolio Notebook Entry: Pop Music Generator

## Task: Enhanced a Python-based pop music generator to create rhythmic and melodic patterns.

## What I did:

- Implemented waveform generation for multiple types (sine, square, sawtooth, triangle).
- Added rhythm patterns with kick, snare, and hi-hat sounds for a more dynamic beat.
- Synthesized melodic loops and basslines with customizable parameters for variety.
- Enabled playback of generated music using the sounddevice library.

## Reflection:

- Experimenting with different waveforms and rhythms helped me understand how small changes affect the feel of the music.
Adding rhythm patterns gave the music a more engaging and realistic sound. I enjoyed the challenge of balancing the melody, bass, and rhythm to create cohesive output.
- This assignment inspired me to explore more features like chord variations and melody randomization in the future.
Overall, it was fun.

