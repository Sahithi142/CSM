# "Pop Music Generator"
# Updated and Enhanced for Better Functionality

import argparse, random, re, wave
import numpy as np
import sounddevice as sd

def generate_rhythm():
    kick_wave = np.sin(2 * np.pi * 60 * np.linspace(0, 1, beat_samples // 2))
    kick_wave *= np.exp(-np.linspace(0, 1, len(kick_wave)) * 10)  

    snare_wave = np.random.normal(0, 1, beat_samples // 2) * np.exp(-np.linspace(0, 1, beat_samples // 2) * 20)

    hi_hat_wave = np.random.normal(0, 1, beat_samples // 4) * np.exp(-np.linspace(0, 1, beat_samples // 4) * 40)
    hi_hat_wave = np.tile(hi_hat_wave, 4)  

    rhythm_pattern = np.zeros(beat_samples * 4)

    rhythm_pattern[:len(kick_wave)] += kick_wave  
    rhythm_pattern[beat_samples:beat_samples + len(snare_wave)] += snare_wave  
    rhythm_pattern[2 * beat_samples:2 * beat_samples + len(hi_hat_wave)] += hi_hat_wave[:beat_samples] 

    return rhythm_pattern

def generate_waveform(note_key, duration=1, waveform_type="sine"):
    frequency = 440 * 2 ** ((note_key - 69) / 12)
    num_samples = beat_samples * duration
    time_axis = np.linspace(0, 2 * np.pi * frequency * num_samples / samplerate, num_samples)

    if waveform_type == "sine":
        return np.sin(time_axis)
    elif waveform_type == "sawtooth":
        return 2 * (time_axis / np.pi - np.floor(0.5 + time_axis / np.pi))
    elif waveform_type == "triangle":
        return 2 * np.abs(2 * (time_axis / np.pi - np.floor(0.5 + time_axis / np.pi))) - 1
    elif waveform_type == "square":
        return np.sign(np.sin(time_axis))
    

# 11 canonical note names.
names = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
note_names = {s: i for i, s in enumerate(names)}
def play(sound):
    sd.play(sound, samplerate=samplerate, blocking=True)
# Turn a note name into a corresponding MIDI key number.
note_name_re = re.compile(r"([A-G]b?)(\[([0-8])\])?")
def parse_note(s):
    m = note_name_re.fullmatch(s)
    if m is None:
        raise ValueError
    s = m[1]
    s = s[0].upper() + s[1:]
    q = 4
    if m[3] is not None:
        q = int(m[3])
    return note_names[s] + 12 * q

# Gain parsers
def parse_log_knob(k, db_at_zero=-40):
    v = float(k)
    if v < 0 or v > 10:
        raise ValueError
    return 10**(-db_at_zero * (v - 10) / 200)

def parse_linear_knob(k):
    v = float(k)
    if v < 0 or v > 10:
        raise ValueError
    return v / 10

def parse_db(d):
    v = float(d)
    if v > 0:
        raise ValueError
    return 10**(v / 20)

# Argument parsing
ap = argparse.ArgumentParser()
ap.add_argument('--bpm', type=int, default=90)
ap.add_argument('--samplerate', type=int, default=48_000)
ap.add_argument('--root', type=parse_note, default="C[5]")
ap.add_argument('--bass-octave', type=int, default=2)
ap.add_argument('--balance', type=parse_linear_knob, default="5")
ap.add_argument('--gain', type=parse_db, default="-3")
ap.add_argument('--waveform', choices=["sine", "square", "sawtooth", "triangle"], default="sine")
ap.add_argument('--output')
args = ap.parse_args()

# Tempo and samplerate
bpm = args.bpm
samplerate = args.samplerate
beat_samples = int(np.round(samplerate / (bpm / 60)))

# Scales and chords
major_scale = [0, 2, 4, 5, 7, 9, 11]
major_chord = [1, 3, 5]

def note_to_key_offset(note):
    scale_degree = note % 7
    return note // 7 * 12 + major_scale[scale_degree]

def chord_to_note_offset(posn):
    chord_posn = posn % 3
    return posn // 3 * 7 + major_chord[chord_posn] - 1

melody_root = args.root
bass_root = melody_root - 12 * args.bass_octave
chord_loop = [8, 5, 6, 4]

position = 0
def pick_notes(chord_root, n=4):
    global position
    p = position
    notes = []
    for _ in range(n):
        chord_note_offset = chord_to_note_offset(p)
        chord_note = note_to_key_offset(chord_root + chord_note_offset)
        notes.append(chord_note)
        if random.random() > 0.5:
            p = p + 1
        else:
            p = p - 1
    position = p
    return notes

def make_waveform(key, n=1, waveform="sine"):
    f = 440 * 2 ** ((key - 69) / 12)
    b = beat_samples * n
    cycles = 2 * np.pi * f * b / samplerate
    t = np.linspace(0, cycles, b)
    if waveform == "sine":
        return np.sin(t)
    elif waveform == "square":
        return np.sign(np.sin(t))
    elif waveform == "sawtooth":
        return 2 * (t / np.pi - np.floor(0.5 + t / np.pi))
    elif waveform == "triangle":
        return 2 * np.abs(2 * (t / np.pi - np.floor(0.5 + t / np.pi))) - 1

def make_rhythm():
    # Generate kick, snare, and hi-hat patterns
    kick = np.sin(2 * np.pi * 60 * np.linspace(0, 1, beat_samples // 2))
    kick = kick * np.exp(-np.linspace(0, 1, len(kick)) * 10)  # Decay envelope

    snare = np.random.normal(0, 1, beat_samples // 2) * np.exp(-np.linspace(0, 1, beat_samples // 2) * 20)

    hi_hat = np.random.normal(0, 1, beat_samples // 4) * np.exp(-np.linspace(0, 1, beat_samples // 4) * 40)
    hi_hat = np.tile(hi_hat, 4)  # Repeat for a full measure

    # Initialize the rhythm array
    rhythm = np.zeros(beat_samples * 4)

    # Place the kick, snare, and hi-hat at appropriate intervals
    rhythm[:len(kick)] += kick  # Kick on beat 1
    rhythm[beat_samples:beat_samples + len(snare)] += snare  # Snare on beat 2
    rhythm[2 * beat_samples:2 * beat_samples + len(hi_hat)] += hi_hat[:beat_samples]  # Hi-hat on beat 3

    return rhythm

sound = np.array([], dtype=np.float64)
for c in chord_loop:
    notes = pick_notes(c - 1)
    melody = np.concatenate([make_waveform(i + melody_root, waveform=args.waveform) for i in notes])
    bass_note = note_to_key_offset(c - 1)
    bass = generate_waveform(bass_note + bass_root, duration=4, waveform_type="sine")
    rhythm = generate_rhythm()
    melody_gain = args.balance
    bass_gain = 1 - melody_gain
    sound = np.append(sound, melody_gain * melody + bass_gain * bass + 0.1 * rhythm)

if args.output:
    output = wave.open(args.output, "wb")
    output.setnchannels(1)
    output.setsampwidth(2)
    output.setframerate(samplerate)
    output.setnframes(len(sound))
    data = args.gain * 32767 * sound.clip(-1, 1)
    output.writeframesraw(data.astype(np.int16))
    output.close()
else:
    play(args.gain * sound)
if args.output:
    print(f"Saving to {args.output}")
    ...
else:
    print("Playing sound...")
    play(args.gain * sound)