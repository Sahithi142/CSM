import os
import numpy as np
import soundfile as sf
from django.shortcuts import render, redirect
from django.conf import settings
from pydub import AudioSegment
from .forms import AudioUploadForm

# Helper functions for audio processing
def simple_resample(sig, speed_factor):
    old_indices = np.arange(len(sig))
    new_len = int(len(sig) / speed_factor)
    new_indices = np.linspace(0, len(sig)-1, new_len)
    return np.interp(new_indices, old_indices, sig)

def shift_pitch(sig, semitones, fs):
    factor = 2 ** (semitones / 12.0)
    intermediate = simple_resample(sig, factor)
    return np.interp(np.linspace(0, len(intermediate)-1, len(sig)), np.arange(len(intermediate)), intermediate)

def stretch_time(sig, stretch_factor):
    old_idx = np.arange(len(sig))
    new_length = int(len(sig) * stretch_factor)
    new_idx = np.linspace(0, len(sig)-1, new_length)
    return np.interp(new_idx, old_idx, sig)

def add_simple_echo(sig, fs, delay_sec=0.3, decay=0.4):
    delay_samps = int(delay_sec * fs)
    out = np.zeros(len(sig) + delay_samps)
    out[:len(sig)] = sig
    out[delay_samps:delay_samps+len(sig)] += sig * decay
    return out

def apply_vibrato(sig, fs, rate=5.0, depth=0.5):
    t = np.linspace(0, len(sig)/fs, len(sig))
    semitone_mod = depth * np.sin(2 * np.pi * rate * t)
    pitch_factors = 2 ** (semitone_mod / 12.0)
    cumulative = np.cumsum(pitch_factors)
    cumulative = cumulative * (len(sig) / cumulative[-1])
    return np.interp(np.arange(len(sig)), cumulative, sig)

def pitch_glide(sig, fs, start_st=-5, end_st=5):
    num_samps = len(sig)
    st_curve = np.linspace(start_st, end_st, num_samps)
    pf = 2 ** (st_curve / 12.0)
    cum_dist = np.cumsum(pf)
    cum_dist = cum_dist * (num_samps / cum_dist[-1])
    return np.interp(np.arange(num_samps), cum_dist, sig)

def random_seg_pitch(sig, fs, segments=8, max_st=5):
    seg_len = len(sig) // segments
    pieces = []
    for i in range(segments):
        seg_start = i*seg_len
        if i == segments-1:
            seg_end = len(sig)
        else:
            seg_end = seg_start + seg_len
        chunk = sig[seg_start:seg_end]
        shift_amt = np.random.randint(-max_st, max_st+1)
        pieces.append(shift_pitch(chunk, shift_amt, fs))
    return np.concatenate(pieces)

def apply_distortion(sig, gain=2.0):
    dist = sig * gain
    dist = np.clip(dist, -1.0, 1.0)
    return dist

def apply_lowpass(sig, filt_len=101):
    filt_kernel = np.ones(filt_len) / filt_len
    return np.convolve(sig, filt_kernel, mode='same')

def reverse_audio(sig):
    return sig[::-1]

def fade_in_out(sig, fs, fade_in_sec=0.5, fade_out_sec=0.5):
    fade_in_samps = int(fs * fade_in_sec)
    fade_out_samps = int(fs * fade_out_sec)
    out = sig.copy()
    out[:fade_in_samps] *= np.linspace(0, 1, fade_in_samps)
    out[-fade_out_samps:] *= np.linspace(1, 0, fade_out_samps)
    return out

def tremolo(sig, fs, rate=5.0):
    t_vals = np.linspace(0, len(sig)/fs, len(sig))
    trem_curve = 0.5 * (1.0 + np.sin(2 * np.pi * rate * t_vals))
    return sig * trem_curve.astype(np.float32)

def ring_mod(sig, fs, carrier_freq=100.0):
    t_vals = np.linspace(0, len(sig)/fs, len(sig))
    carrier = np.sin(2 * np.pi * carrier_freq * t_vals).astype(np.float32)
    return sig * carrier

def apply_effect(samples, fs, effect):
    if effect == 'none':
        return samples
    elif effect == 'pitch_up':
        return shift_pitch(samples, 3, fs)
    elif effect == 'pitch_down':
        return shift_pitch(samples, -3, fs)
    elif effect == 'slow':
        return stretch_time(samples, 1.5)
    elif effect == 'fast':
        return stretch_time(samples, 0.7)
    elif effect == 'vibrato':
        return apply_vibrato(samples, fs, rate=5.0, depth=2.0)
    elif effect == 'glide':
        return pitch_glide(samples, fs, start_st=-5, end_st=5)
    elif effect == 'random_jump':
        return random_seg_pitch(samples, fs, segments=8, max_st=4)
    elif effect == 'echo':
        return add_simple_echo(samples, fs, delay_sec=0.3, decay=0.4)
    elif effect == 'distortion':
        return apply_distortion(samples, gain=2.0)
    elif effect == 'lowpass':
        return apply_lowpass(samples, filt_len=101)
    elif effect == 'reverse':
        return reverse_audio(samples)
    elif effect == 'fade':
        return fade_in_out(samples, fs, fade_in_sec=0.5, fade_out_sec=0.5)
    elif effect == 'tremolo':
        return tremolo(samples, fs, rate=5.0)
    elif effect == 'ring_mod':
        return ring_mod(samples, fs, carrier_freq=100.0)
    else:
        return samples

def index_view(request):
    if request.method == 'POST':
        form = AudioUploadForm(request.POST, request.FILES)
        if form.is_valid():
            audio_file = request.FILES['audio_file']
            effect = form.cleaned_data['effect']

            # Save the uploaded file temporarily
            input_path = os.path.join(settings.MEDIA_ROOT, 'input.mp3')
            with open(input_path, 'wb+') as dest:
                for chunk in audio_file.chunks():
                    dest.write(chunk)

            # Load audio
            audio = AudioSegment.from_file(input_path, format="mp3")
            fs = audio.frame_rate
            raw_samples = np.array(audio.get_array_of_samples(), dtype=np.float32)

            # Convert to mono if stereo
            if audio.channels > 1:
                raw_samples = raw_samples.reshape(-1, audio.channels).mean(axis=1)

            # Normalize amplitude
            peak_val = np.abs(raw_samples).max()
            samples = raw_samples / peak_val if peak_val > 0 else raw_samples

            # Apply selected effect
            processed = apply_effect(samples, fs, effect)

            # Save the processed output
            output_path = os.path.join(settings.MEDIA_ROOT, 'processed', 'output.wav')
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            sf.write(output_path, processed, fs)

            # Redirect to result page
            return redirect('result_view')
    else:
        form = AudioUploadForm()
    return render(request, 'myapp/index.html', {'form': form})

def result_view(request):
    # The processed file is available at /media/processed/output.wav
    audio_url = settings.MEDIA_URL + 'processed/output.wav'
    return render(request, 'myapp/result.html', {'audio_url': audio_url})
