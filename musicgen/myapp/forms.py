from django import forms

EFFECT_CHOICES = [
    ('none', 'No Effect'),
    ('pitch_up', 'Pitch Up'),
    ('pitch_down', 'Pitch Down'),
    ('slow', 'Slow Down (1.5x)'),
    ('fast', 'Speed Up (0.7x)'),
    ('vibrato', 'Vibrato'),
    ('glide', 'Pitch Glide'),
    ('random_jump', 'Random Segment Pitch Jumps'),
    ('echo', 'Echo'),
    ('distortion', 'Distortion'),
    ('lowpass', 'Low-Pass Filter'),
    ('reverse', 'Reverse'),
    ('fade', 'Fade In/Out'),
    ('tremolo', 'Tremolo'),
    ('ring_mod', 'Ring Modulation')
]

class AudioUploadForm(forms.Form):
    audio_file = forms.FileField(label='Upload any MP3 file')
    effect = forms.ChoiceField(choices=EFFECT_CHOICES, label='Choose any one effect')
