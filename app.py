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
