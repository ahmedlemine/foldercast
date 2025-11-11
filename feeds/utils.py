import logging
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

from django.conf import settings


logger = logging.getLogger(__name__)




def generate_artwork_img(title_text, output_file_path):
    default_artwork_path = Path(settings.BASE_DIR, "static/img/default_artwork.png")
    if not default_artwork_path:
        logger.error(f"Default artwork image not found at {default_artwork_path}")
        return None

    try:
        img = Image.open(default_artwork_path)
    except Exception as e:
        logger.error(f"Failed to open default artwork file: {e}")
        return None

    draw = ImageDraw.Draw(img)

    text = title_text
    position = (100, 720)
    font_size = 100
    text_color = (255, 255, 255)

    try:
        font = ImageFont.truetype(
            str(Path(settings.BASE_DIR, "static/fonts/ARI.ttf")), font_size
        )
    except FileNotFoundError:
        logger.warning("Warning: selected font not found. Using default font.")
        font = ImageFont.load_default()

    draw.text(position, text, font=font, fill=text_color)

    img.save(output_file_path)

    logger.info(f"Artwork generated and saved to: {output_file_path}")

    return output_file_path
