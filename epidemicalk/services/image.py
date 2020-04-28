from abc import ABC
from mimetypes import guess_extension, guess_type
import base64
import os
import uuid


def get_extension_base64(image_base64: str):
    extension = guess_extension(guess_type(image_base64)[0])
    return extension


def clean_base64(image_base64: str):
    image_base64 = image_base64.replace("data:image/png;base64,", "")
    image_base64 = image_base64.replace("data:image/jpeg;base64,", "")
    return image_base64


def save_image(image_base64: str, name_file:str):
    img_data = image_base64.encode()
    with open(name_file, "wb") as fh:
        fh.write(base64.decodebytes(img_data))


def remove(name_file: str):
    os.remove(name_file)


def generate_name_random(image_base64: str):
    extension = get_extension_base64(image_base64)
    name_file = str(uuid.uuid4()) + extension
    return name_file

