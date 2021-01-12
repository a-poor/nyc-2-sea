
import numpy as np
from PIL import Image
from pytesseract import image_to_string

def read_image(path):
    return Image.open(path)

def crop_convert(img,crop=(195,1020,1500,1080)):
    return np.array(img.crop(crop).convert("L"))

def filter_image(img,cuttoff=200):
    return Image.fromarray(np.where(
        img > cuttoff,
        np.zeros_like(img),
        np.ones_like(img)
    ))

def extract_text(img):
    return image_to_string(img).strip()

def process_image(path,crop=(195,1020,1500,1080),cuttoff=200):
    img = read_image(path)
    img = crop_convert(img,crop=crop)
    img = filter_image(img,cuttoff=cuttoff)
    return extract_text(img)

