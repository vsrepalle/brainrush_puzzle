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
