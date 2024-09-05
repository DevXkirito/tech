from moviepy.editor import *
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler
import requests

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = '6449794069:AAGqUp-VO0GV8Jm9lOCSB6fb0fKJELiL-F0'  # Replace with your bot token

def start(update, context):
    update.message.reply_text('Hi! I can hard burn subtitles into a video. Send me a video and a subtitle file.')

def help(update, context):
    update.message.reply_text('Send me a video and a subtitle file, and I\'ll hard burn the subtitles into the video.')

def burn_subtitles(update, context):
    if len(context.args) != 2:
        update.message.reply_text('Usage: /burn <video_file> <subtitle_file>')
        return

    video_file = context.args[0]
    subtitle_file = context.args[1]

    # Download the video and subtitle files
    video = context.bot.get_file(update.message.video).download()
    subtitle = context.bot.get_file(update.message.document).download()

    # Create a MoviePy video object
    clip = VideoFileClip(video)

    # Set the font style and logo from GitHub repository
    font_url = 'https://github.com/username/repository-name/raw/main/font.ttf'
    font_path = 'font.ttf'
    response = requests.get(font_url)
    with open(font_path, 'wb') as f:
        f.write(response.content)
    font = font_path

    logo_url = 'https://github.com/username/repository-name/raw/main/logo.png'
    logo_path = 'logo.png'
    response = requests.get(logo_url)
    with open(logo_path, 'wb') as f:
        f.write(response.content)
    logo = logo_path

    # Set the resolution and frame rate
    resolution = (265, 265)
    fps = 30

    # Hard burn the subtitles into the video
    clip = clip.resize(resolution)
    clip = clip.set_fps(fps)
    clip = clip.fl_image(lambda frame: frame, apply_to=['mask', 'audio'])

    # Add the subtitles to the video
    clip = clip.subclip(0, clip.duration).set_start(0)
    subtitle_clip = TextClip(subtitle, fontsize=20, font=font, color='white')
    subtitle_clip = subtitle_clip.set_position(('center', 'bottom'))  # Set subtitle position to center bottom
    subtitle_clip = subtitle_clip.set_duration(clip.duration)
    clip = CompositeVideoClip([clip, subtitle_clip])

    # Add the logo to the video
    logo_clip = ImageClip(logo).set_position('top-left').set_duration(clip.duration)
    clip = CompositeVideoClip([clip, logo_clip])

    # Write the final video to a file
    output_file = 'output.mp4'
    clip.write_videofile(output_file)

    # Send the final video to the user
    context.bot.send_video(chat_id=update.effective_chat.id, video=open(output_file, 'rb'))

def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('burn', burn_subtitles))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
