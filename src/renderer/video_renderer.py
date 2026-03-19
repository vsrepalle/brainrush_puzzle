from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import uuid, os

WIDTH, HEIGHT = 720, 1280

def get_font(size):
    try:
        return ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", size)
    except:
        return ImageFont.load_default()

def get_base_dir():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_background():
    base_dir = get_base_dir()
    bg_path = os.path.join(base_dir, "background_image.jpg")

    if os.path.exists(bg_path):
        img = Image.open(bg_path).resize((WIDTH, HEIGHT))
    else:
        img = Image.new("RGB", (WIDTH, HEIGHT), (20,20,60))
    return img

def create_image(text):
    img = get_background()
    draw = ImageDraw.Draw(img)

    font = get_font(70)
    lines = text.replace("->","→").split("\n")

    total_h = len(lines) * 90
    y = (HEIGHT - total_h)//2

    for line in lines:
        w = draw.textbbox((0,0), line, font=font)[2]
        x = (WIDTH - w)//2
        draw.text((x+2,y+2), line, fill=(0,0,0), font=font)
        draw.text((x,y), line, fill=(255,255,255), font=font)
        y += 90

    path = f"temp_{uuid.uuid4()}.png"
    img.save(path)
    return path

def create_countdown():
    clips = []
    for i in range(5,0,-1):
        img = create_image(str(i))
        clip = ImageClip(img).set_duration(0.7)
        clips.append(clip)
    return clips

def render_video(puzzles, output_path):
    temp_files = []
    clips = []

    # Hook
    hook = create_image("Only 1% can solve this!")
    temp_files.append(hook)
    clips.append(ImageClip(hook).set_duration(2))

    for p in puzzles:
        q = create_image(p["question"])
        a = create_image("Answer: " + p["answer"])
        e = create_image("Explanation:\n" + p["explanation"])

        temp_files.extend([q,a,e])

        clips.append(ImageClip(q).set_duration(3))

        # Countdown
        countdown = create_countdown()
        clips.extend(countdown)

        clips.append(ImageClip(a).set_duration(2))
        clips.append(ImageClip(e).set_duration(3))

    final = concatenate_videoclips(clips)

    base_dir = get_base_dir()

    # Background music
    music_path = os.path.join(base_dir, "background_music.mp3")
    if os.path.exists(music_path):
        audio = AudioFileClip(music_path).subclip(0, final.duration)
        final = final.set_audio(audio)

    final.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")

    # Cleanup temp files
    print("[DEBUG] Cleaning temp files...")
    for f in temp_files:
        try:
            os.remove(f)
        except:
            pass
    print("[DEBUG] Cleanup done")