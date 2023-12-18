import secrets
import os
from PIL import Image
from app import app


def save_picture_data(form_picture):
    # generate hashed name to avoid collision
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    filename = random_hex + f_ext

    # generate absolute path for profile pic
    filepath = os.path.join(app.root_path, "static/profile_pics", filename)

    # resize pic to icon size before saving
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(filepath)

    return filename
