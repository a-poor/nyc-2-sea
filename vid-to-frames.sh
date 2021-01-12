echo "Starting..."
mkdir -p tmp/video tmp/images mongodata

echo ""
echo "Checking for mongodb..."
if [ 0 -eq $(docker ps | grep nyc2sea_mongo | wc -l) ]
then 
    echo "Mongo not running. Starting it up..."
    MONGO_ID=$(./start-mongo.sh)
    echo "Mongo id: $MONGO_ID"
fi

echo ""
echo "Creating a local copy of the unprocessed S3 videos..."
aws s3 cp s3://nyc-2-sea-road-trip/raw-video/ tmp/video --recursive

echo ""
echo ""

echo "Found $(ls tmp/video | wc -l) videos to process."
echo "Converting videos to images..."
for VID_FILE in $(ls tmp/video)
do
    NEW_NAME="${VID_FILE%.*}-%04d.jpg"
    ffmpeg -i $VID_FILE $NEW_NAME
done


echo ""
echo "Performing OCR on full-size images..."
python apply-ocr.py --path tmp/images

echo ""
echo "Removing large images..."
rm tmp/images/*

echo ""
echo "Converting videos to half-size images..."
for VID_FILE in $(ls tmp/video)
do
    NEW_NAME="${VID_FILE%.*}-%04d.jpg"
    ffmpeg -i $VID_FILE -s 960x540 $NEW_NAME
done

echo ""
echo ""

echo "Uploading $(ls tmp/images/ | wc -l) images..."
aws s3 mv tmp/images/ s3://nyc-2-sea-road-trip/raw-images/ --recursive 

echo ""
echo ""

echo "Moving processed videos to new bucket..."
for VID_FILE in $(ls tmp/video)
do
    aws s3 mv s3://nyc-2-sea-road-trip/raw-video/$VID_FILE s3://nyc-2-sea-road-trip/processed-video/$VID_FILE 
done

echo ""
echo ""

echo "Cleaning up..."
rm -r tmp/
[ -d __pycache__ ] && rm -r __pycache__
docker stop $MONGO_ID

echo "Done."

