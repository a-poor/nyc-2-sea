# NYC-2-SEA Road Trip

In order to process new videos in `s3://nyc-2-sea-road-trip/raw-video`
run the script `vid-to-frames.sh`.

* `vid-to-frames.sh`: (_Main script_) Processes new raw videos in S3
* `start-mongo.sh`: Starts the local MongoDB docker container (data
is stored in the `mongodata/` directory.
* `apply-ocr.py`: Applies image preprocessing and OCR to images in the
directory `tmp/images` and adds them to the MongoDB database. Run as a
command line script.
* `process_image.py`: Stores code for image preprocessing and performing
OCR via the `pytesseract` module.

