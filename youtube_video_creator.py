from PIL import Image, ImageFont, ImageDraw
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
import boto3
#create logger
import logging
logger = logging.getLogger('youtube_video_creator')
logger.setLevel(logging.DEBUG)
logging_handler = logging.StreamHandler()
logging_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging_handler.setFormatter(formatter)
logger.addHandler(logging_handler)

def rewrite_on_image(image_to_write):
    try:
        my_image = Image.open(image_to_write)
        title_font = ImageFont.truetype('playfair/playfairDisplay-Regular.ttf', 60)
        title_text = "Hello From Tech Life Automator"
        image_edit = ImageDraw.Draw(my_image)
        image_edit.text((15,15), title_text, (237, 230, 211), font=title_font)
        my_image.save("result.png")
    except Exception as exc:
        logger.info(exc)
        return False
    return True
def start_speech_synthesis_for_youtube():
    poly_client = boto3.client('polly')
    try:
        polly_response = poly_client.synthesize_speech(
            Engine = 'neural',
            LanguageCode = 'en-GB',
            OutputFormat = 'mp3',
            Text = 'Hello From Tech Life Automator',
            TextType = 'text',
            VoiceId = 'Emma'
        )
        file = open('speech.mp3', 'wb')
        file.write(polly_response['AudioStream'].read())
        file.close()
        logger.info(polly_response)
    except Exception as exc:
        logger.error(exc)
        return False
    return True
def make_video_from_image():
    try:
        image = ImageClip("result.png")
        audio  = AudioFileClip("speech.mp3")
        image = image.set_duration(audio.duration)
        image = image.set_audio(audio)
        video = concatenate_videoclips([image])
        video.write_videofile("output.mp4", codec="libx264", fps=24)
    except Exception as exc:
        logger.error(exc)
        return False
    return True


if __name__ == "__main__":
    if rewrite_on_image("test.png"):
        logger.info("Image rewrite completed!")
    else:
        logger.error("Issue with Image rewrite")

    if start_speech_synthesis_for_youtube():
        logger.info("Speech synthesis succesfull")
    else: 
        logger.error("Issue with speech synthesis")
    
    if make_video_from_image():
        logger.info("Video succefully created")
    else:
        logger.error("Issue with video creation")