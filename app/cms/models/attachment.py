import logging

from io import BytesIO
from os.path import dirname, abspath
from pathlib import Path

from django.db import models
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import requests
from requests.exceptions import MissingSchema
from PIL import Image, ImageFont, ImageDraw, ImageFilter
from s3direct.fields import S3DirectField

ASSETS_DIR = Path(dirname(dirname(abspath(__file__)))) / 'assets'


class Attachment(models.Model):
    """
    Zu einem Fragment kann ein Medien-Anhang hinzugefügt werden.
    """

    class Meta:
        abstract = True

    media_original = S3DirectField('Medien-Anhang', null=True, blank=True, dest='default')
    media_note = models.CharField(
        'Credit',
        help_text="Bei Foto-Anhang hier die Quelle eintragen. Wird auf dem Foto angezeigt.",
        max_length=100,
        null=True,
        blank=True)

    media = models.FileField('Verarbeitet', null=True, blank=True)

    def update_attachment(self):
        if not self.media_original:
            self.media = None
            return

        original_url = str(self.media_original)

        filename = original_url.split('/')[-1]

        if not (filename.lower().endswith('.png')
                or filename.lower().endswith('.jpg')
                or filename.lower().endswith('.jpeg')):
            self.media = filename
            return

        file_content = requests.get(original_url).content

        try:
            img = Image.open(BytesIO(file_content))
        except:
            self.media = filename
            logging.exception('Loading attachment for processing failed')
            return

        image_changed = False
        orig_mode = img.mode
        max_size = (1920, 1080)

        # Resize image
        if any(actual > max_ for actual, max_ in zip(img.size, max_size)):
            scale = min(max_ / actual for max_, actual in zip(max_size, img.size))

            new_size = tuple(int(dim * scale) for dim in img.size)
            img = img.resize(new_size, resample=Image.LANCZOS)
            image_changed = True

        # Draw credit onto image
        if self.media_note:
            # Create initial image objects for text drawing
            img = img.convert('RGBA')
            alpha = Image.new('RGBA', img.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(alpha)

            # Configuration for text drawing
            the_text = 'FOTO: ' + self.media_note.upper()
            fontsize = max((img.size[0] + img.size[1]) / 2 / 50, 10)
            shadow_radius = fontsize / 3
            shadow_mult = 0.75
            text_alpha = 0.7
            padding = tuple((int(shadow_radius * 2.5), int(shadow_radius * 3)))
            position = tuple(int(shadow_radius + p) for p in padding)

            fnt = ImageFont.truetype(
                str(ASSETS_DIR / 'Open_Sans' / 'OpenSans-SemiBold.ttf'), int(fontsize))

            # Calculate size of text
            text_size = draw.textsize(the_text, font=fnt)

            # Create new, smaller image to draw the text on
            txt = Image.new(
                'RGBA',
                tuple(ts + pad + pos for ts, pad, pos in zip(text_size, padding, position)),
                (0, 0, 0, 0))

            # Do the drawing
            draw = ImageDraw.Draw(txt)
            draw.text(position, the_text, font=fnt, fill=(0, 0, 0, 255))

            shadow = txt.filter(ImageFilter.GaussianBlur(radius=shadow_radius))
            txt = shadow.point(lambda px: min(int(px * shadow_mult), 255))

            draw = ImageDraw.Draw(txt)
            draw.text(position, the_text, font=fnt, fill=(255, 255, 255, int(255 * text_alpha)))

            # Rotate and paste onto original image
            txt = txt.rotate(90, expand=1, resample=Image.LANCZOS)
            alpha.paste(txt, box=tuple(a - b for a, b in zip(alpha.size, txt.size)))
            img = Image.alpha_composite(img, alpha)
            image_changed = True

        if not image_changed:
            self.media = filename
            return

        # Save result
        bio = BytesIO()
        bio.name = filename
        out = img.convert(orig_mode)
        out.save(bio)
        bio.seek(0)

        new_filename = default_storage.generate_filename(filename)
        print('New filename:', new_filename)
        path = default_storage.save(new_filename, ContentFile(bio.read(), name=new_filename))
        self.media = path

