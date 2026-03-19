import os
from datetime import datetime
from src.generator.puzzle_generator import generate_puzzle
from src.renderer.video_renderer import render_video
from src.uploader.upload_youtube import upload_video

OUTPUT_DIR = "output/videos"

def main():
    print("[DEBUG] Starting VIRAL pipeline...")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 🔥 Generate multiple videos
    for i in range(3):  # change to 10+ later
        print(f"[DEBUG] Creating video {i+1}")

        puzzles = generate_puzzle()

        filename = f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}.mp4"
        output_path = os.path.join(OUTPUT_DIR, filename)

        render_video(puzzles, output_path)

        upload_video(output_path)

    print("[DEBUG] All videos created!")

if __name__ == "__main__":
    main()
