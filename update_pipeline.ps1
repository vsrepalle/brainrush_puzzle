# ------------------------------
# PowerShell Script: Update Puzzle Pipeline with JSON Themes
# Save as update_pipeline_with_json_themes.ps1
# ------------------------------

$backupDir = "backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
New-Item -ItemType Directory -Path $backupDir
Copy-Item "src\renderer\video_renderer.py" "$backupDir\video_renderer.py.bak" -ErrorAction SilentlyContinue
Copy-Item "src\generator\puzzle_generator.py" "$backupDir\puzzle_generator.py.bak" -ErrorAction SilentlyContinue
Copy-Item "app.py" "$backupDir\app.py.bak" -ErrorAction SilentlyContinue
Copy-Item "config.py" "$backupDir\config.py.bak" -ErrorAction SilentlyContinue
Copy-Item "run_debug.bat" "$backupDir\run_debug.bat.bak" -ErrorAction SilentlyContinue
Write-Host "Backups created at $backupDir"

# ------------------------------
# config.py
# ------------------------------
Set-Content -Path "config.py" -Value @"
import os

# Path to ImageMagick magick.exe
IMAGEMAGICK_BINARY = r'C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe'
OUTPUT_DIR = os.path.join(os.getcwd(), 'output', 'videos')
"@

# ------------------------------
# themes.json
# ------------------------------
Set-Content -Path "themes.json" -Value @"
{
  "Arithmetic": "generate_arithmetic",
  "Geometric": "generate_geometric",
  "Logical": "generate_logical",
  "Fibonacci": "generate_fibonacci",
  "Squares": "generate_squares",
  "Random": "random"
}
"@

# ------------------------------
# video_renderer.py
# ------------------------------
Set-Content -Path "src\renderer\video_renderer.py" -Value @"
import config
from moviepy.config import change_settings

# Configure MoviePy to use ImageMagick
change_settings({'IMAGEMAGICK_BINARY': config.IMAGEMAGICK_BINARY})

from moviepy.editor import ImageClip, TextClip, CompositeVideoClip, AudioFileClip, concatenate_videoclips

def render_puzzle_video(question, answer, explanation, output_path):
    'Render puzzle video with background image + music, Q->Explanation->A sequence'

    duration = 3  # seconds per segment

    bg_clip = ImageClip('background_image.jpg').resize((720, 1280))

    # Question
    question_text = TextClip(question,
                             fontsize=50, color='white', size=(700, 1200),
                             method='caption', align='center')
    question_text = question_text.set_position('center').set_duration(duration)
    question_clip = CompositeVideoClip([bg_clip.set_duration(duration), question_text])

    # Explanation
    explanation_text = TextClip(f'Explanation:\n{explanation}',
                                fontsize=45, color='lightblue', size=(700, 1200),
                                method='caption', align='center')
    explanation_text = explanation_text.set_position('center').set_duration(duration)
    explanation_clip = CompositeVideoClip([bg_clip.set_duration(duration), explanation_text])

    # Answer
    answer_text = TextClip(f'Answer: {answer}',
                           fontsize=50, color='yellow', size=(700, 1200),
                           method='caption', align='center')
    answer_text = answer_text.set_position('center').set_duration(duration)
    answer_clip = CompositeVideoClip([bg_clip.set_duration(duration), answer_text])

    final_clip = concatenate_videoclips([question_clip, explanation_clip, answer_clip])

    # Background music
    try:
        audio_clip = AudioFileClip('background_music.mp3').subclip(0, 3*duration)
        final_clip = final_clip.set_audio(audio_clip)
    except Exception as e:
        print(f'No background music applied: {e}')

    final_clip.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')
"@

# ------------------------------
# puzzle_generator.py
# ------------------------------
Set-Content -Path "src\generator\puzzle_generator.py" -Value @"
import random
import json
import os

# -------------------------
# Standard puzzle functions
# -------------------------
def generate_arithmetic():
    n = random.randint(1, 10)
    q = f'{n} * ({n+1}) = ?'
    a = n*(n+1)
    e = f'Multiply {n} by {n+1} to get {a}.'
    return q, a, e

def generate_geometric():
    start = random.randint(1, 5)
    ratio = random.randint(2, 4)
    seq = [start, start*ratio, start*ratio**2]
    q = f'{", ".join(map(str, seq))}, ... ?'
    a = start*ratio**3
    e = f'Each term is multiplied by {ratio}. The next term is {a}.'
    return q, a, e

def generate_logical():
    n = random.randint(1, 20)
    seq = [i for i in range(n, n+4)]
    missing = random.choice(seq)
    display_seq = [str(x) if x != missing else "_" for x in seq]
    q = f'Find the missing number: {", ".join(display_seq)}'
    a = missing
    e = f'The sequence is consecutive numbers starting from {n}.'
    return q, a, e

def generate_fibonacci():
    seq = [0, 1]
    for _ in range(2, 5):
        seq.append(seq[-1]+seq[-2])
    missing = random.choice(seq)
    display_seq = [str(x) if x != missing else "_" for x in seq]
    q = f'Fibonacci sequence: {", ".join(display_seq)}'
    a = missing
    e = f'The next Fibonacci number is {a}.'
    return q, a, e

def generate_squares():
    n = random.randint(1, 10)
    seq = [i*i for i in range(n, n+4)]
    missing = random.choice(seq)
    display_seq = [str(x) if x != missing else "_" for x in seq]
    q = f'Square numbers sequence: {", ".join(display_seq)}'
    a = missing
    e = f'The sequence is consecutive squares. Missing is {a}.'
    return q, a, e

# -------------------------
# Load themes JSON
# -------------------------
THEMES_FILE = os.path.join(os.getcwd(), 'themes.json')
with open(THEMES_FILE, 'r') as f:
    THEMES = json.load(f)

# Map string names to functions
THEME_FUNCTIONS = {
    "generate_arithmetic": generate_arithmetic,
    "generate_geometric": generate_geometric,
    "generate_logical": generate_logical,
    "generate_fibonacci": generate_fibonacci,
    "generate_squares": generate_squares
}

# -------------------------
# Generate puzzles by theme
# -------------------------
def generate_puzzle_by_theme(theme_name):
    if theme_name == "Random":
        func = random.choice(list(THEME_FUNCTIONS.values()))
    else:
        func_name = THEMES.get(theme_name)
        func = THEME_FUNCTIONS.get(func_name, random.choice(list(THEME_FUNCTIONS.values())))
    return func()

def generate_puzzle_batch(count=5, theme_name="Random"):
    batch = []
    for _ in range(count):
        q, a, e = generate_puzzle_by_theme(theme_name)
        batch.append({'question': q, 'answer': a, 'explanation': e})
    return batch
"@

# ------------------------------
# app.py
# ------------------------------
Set-Content -Path "app.py" -Value @"
import os
import json
from src.generator.puzzle_generator import generate_puzzle_batch
from src.renderer.video_renderer import render_puzzle_video
from config import OUTPUT_DIR

# Optional YouTube uploader
try:
    from src.uploader.upload_youtube import upload_video
    uploader_available = True
except ImportError:
    uploader_available = False

# Load theme list
with open('themes.json', 'r') as f:
    themes = list(json.load(f).keys())

def main():
    print('[DEBUG] Starting pipeline...')
    print('Available puzzle themes:')
    for idx, t in enumerate(themes, 1):
        print(f'{idx} - {t}')

    choice = input('Enter theme number (default Random): ').strip()
    try:
        choice_idx = int(choice)-1
        theme_name = themes[choice_idx]
    except:
        theme_name = 'Random'

    print(f'[DEBUG] Selected theme: {theme_name}')

    puzzles = generate_puzzle_batch(5, theme_name)
    print(f'[DEBUG] Generated {len(puzzles)} puzzles')

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    video_paths = []

    for idx, p in enumerate(puzzles):
        video_path = os.path.join(OUTPUT_DIR, f'video_{idx}.mp4')
        render_puzzle_video(p['question'], p['answer'], p['explanation'], video_path)
        video_paths.append(video_path)
        print(f'[DEBUG] Video created: {video_path}')

    print('\n[DEBUG] All videos rendered.')

    if uploader_available and video_paths:
        upload = input('Do you want to upload these videos to YouTube? (y/n): ').strip().lower()
        if upload == 'y':
            for vp in video_paths:
                print(f'[DEBUG] Uploading {vp}...')
                upload_video(vp)
            print('[DEBUG] All videos uploaded.')
        else:
            print('[DEBUG] Upload skipped.')
    elif not uploader_available:
        print('[DEBUG] YouTube uploader not available. Skipping upload.')

if __name__ == '__main__':
    main()
"@

# ------------------------------
# run_debug.bat
# ------------------------------
Set-Content -Path "run_debug.bat" -Value @"
@echo off
echo Running DEBUG puzzle batch pipeline...
python app.py
pause
"@

Write-Host "All files updated successfully with JSON theme selection and ImageMagick configuration."