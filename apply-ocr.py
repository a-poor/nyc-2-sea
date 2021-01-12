"""
apply-ocr.py
_created by Austin Poor_

Take images from `--path` directory (assuming
they're 1920x1080), crop them to the bounding
box specified by `--crop`, convert them to
black and white, and then user tesseract
to perform OCR on the image.

The data is stored in a mongodb database
located at `http://localhost:27017` in the
database `nyc_to_sea`, in the collection
`image_ocr`.
"""

import argparse
from pathlib import Path
from pymongo import MongoClient
from tqdm import tqdm
from process_image import process_image


parser = argparse.ArgumentParser(
    description=__doc__
)
parser.add_argument(
    "-p", "--path",
    dest="path",
    default="tmp/images",
    type=str,
    help="Path to images to be OCRed"
)
parser.add_argument(
    "--crop",
    type=int,
    nargs=4,
    default=(195,1020,1500,1080),
    help="Crop image to (left,up,right,bottom)"
)
parser.add_argument(
    "--cuttoff",
    type=int,
    default=200,
    help=("Filters images to be black if their pixel " 
        "value is less than `cuttoff and white if it "
        "is greater than `cuttoff`.")
)

if __name__ == "__main__":
    args = parser.parse_args()
    
    client = MongoClient()
    db = client.nyc_to_sea
    coll = db.image_ocr
    
    image_paths = list(Path(args.path).glob("*.jpg"))

    for img in tqdm(image_paths,desc="Images Processed"):
        txt = process_image(
            img,
            crop=tuple(args.crop),
            cuttoff=args.cuttoff
        )
        coll.insert_one({
            "s3-path": f"s3://nyc-2-sea-road-trip/raw-images/{img.name}",
            "ocr-text": txt
        })

