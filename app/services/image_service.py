import os
import base64
from PIL import Image
from werkzeug.utils import secure_filename
from flask import flash
from flask_babel import gettext
from app.extensions import db


class ImageService:
    @staticmethod
    def get_base64(image, max_image_resolution=(0, 0)):

        if image is None:
            flash('No image provided.', 'error')
            return

        filename = secure_filename(image.filename)
        image_path = os.path.join('app/static/temp', filename)
        image.save(image_path)
        image = Image.open(image_path)
        if max_image_resolution != (0, 0):
            image.thumbnail(max_image_resolution)
        image.save(image_path)

        flash('test2', 'success')

        with open(image_path, 'rb') as f:
            base64_image = base64.b64encode(f.read()).decode('utf-8')

        os.remove(image_path)

        return base64_image
