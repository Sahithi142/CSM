# Django Audio Processing Web App

This Django-based web application allows you to upload an MP3 file, apply various audio effects, and then play the processed result directly in your browser. Effects include pitch shifting, time-stretching, echo, vibrato, distortion, and more.

## Requirements

- Python
- Django
- Numpy
- Soundfile (It is included in folder for testing)
- Pydub
- Matplotlib
- FFmpeg

## Installation

### Using pip

```bash
pip install django numpy soundfile pydub matplotlib
```

Ensure you have FFmpeg installed

## Starting the Server

From the project root (where manage.py is located):

```bash
python manage.py runserver
```

Then open http://127.0.0.1:8000/ in your web browser.

## Where the idea came from

When I was a kid, I loved playing my favorite songs in Windows Media Player and tweaking the few sound options it offered. Even though it was just a basic equalizer and simple effects, it amazed me how those small changes could alter the sound. That early fascination led me to create something, where I can experiment with a wider range of audio effects and share that experience with others.

## How it works

- Go to the home page.
- Upload an MP3 file.
- Select the desired effect from the dropdown.
- Click "Process Audio".
- After processing, you'll be directed to a result page with a player and control buttons.
- Click Play to hear the transformed audio.

Note: The sample music file used for testing is sourced from Pexels Music which provides royalty-free music.

## What I did

- Created a new Django project and app.
- Installed required packages with pip.
- Configured settings.py for media file handling.
- Set up file upload and audio effects application logic in views.py.
- Added a form in forms.py to select effects.
- Created templates (index.html and result.html) to upload, process, and play audio.
- Tested the app locally with the Django development server.

## Effects

- Pitch Shift: Changes pitch by resampling the audio at a different speed, then adjusting back to original length.
- Time-Stretch: Slows down or speeds up the audio by re-interpolating sample positions.
- Vibrato: Slightly alters pitch over time using a sine wave pattern.
- Pitch Glide: Gradually shifts pitch from a starting value to an ending value.
- Random Pitch Jumps: Splits audio into segments and shifts pitch of each segment differently.
- Echo: Adds a delayed and quieter version of the sound to the original.
- Distortion: Increases volume and clips peaks for a harsher sound.
- Low-Pass Filter: Smooths the audio by averaging samples, reducing high frequencies.
- Reverse: Plays the audio backwards.
- Fade In/Out: Gradually changes volume at the start or end of the audio.
- Tremolo: Modulates volume over time with a slow sine wave.
- Ring Modulation: Multiplies the audio by a sine wave for a metallic, ringing effect.
