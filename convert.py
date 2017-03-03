#!/usr/bin/env python
import os, sys
import boto3
import config
from deepzoom import ImageCreator
import shutil

s3 = boto3.client('s3')


def to_zoom(event, context):
    """
    Receives an S3 event record for a new object.
    Downloads the object to the local filesystem,
    uses Deepzoom to tile it, and then uploads the
    results DZI and tileset to a specified bucket.

    """
    bucket = event['Records'][0]['s3']['bucket']['name']  # Bucket where object was created
    key = event['Records'][0]['s3']['object']['key']  # Key (relpath) of object in bucket
    base_key = '.'.join(key.split('.')[:-1])  # Object filename without its extension
    extension = key.split('.')[-1].lower()  # File extension of object
    dzi_key = base_key + '.dzi'  # Key of DZI to be created

    if extension not in config.ALLOWED_EXTENSIONS:  # Abort early due to unsupported file extension
        print('extension {} not allowed'.format(extension))
        return False

    local_file = os.path.join(config.TEMP_DIR, key)  # Local file where object is stored
    dzi_file = os.path.join(config.TEMP_DIR, dzi_key)  # Local file where new DZI will be stored
    tile_dir = os.path.join(config.TEMP_DIR, base_key + '_files')  # Local directory where tiles will be stored
    dzi_key = os.path.relpath(dzi_file, config.TEMP_DIR)  # Relative path to DZI, used as key when uploaded

    print(bucket, key, local_file, dzi_key)

    s3.download_file(bucket, key, local_file)  # Download object to local filesystem for processing
    creator = ImageCreator(tile_size=config.DEEPZOOM_TILE_SIZE, 
                       tile_format=config.DEEPZOOM_TILE_FORMAT,
                       image_quality=config.DEEPZOOM_IMAGE_QUALITY,
                       resize_filter=config.DEEPZOOM_RESIZE_FILTER)
    creator.create(local_file, dzi_file)  # Convert object to tileset using Deepzoom library
    s3.upload_file(dzi_file, config.S3_ZOOM_BUCKET, dzi_key)  # Upload DZI file

    for directory, directories, files in os.walk(tile_dir, topdown=False):  # Loop through tile_dir and upload all tiles
        for name in files:
            file_path = os.path.join(directory, name)
            file_key = os.path.relpath(file_path, config.TEMP_DIR)

            # Upload tile, retrying if exception is thrown
            retry = True
            while retry:
                try:
                    s3.upload_file(file_path, config.S3_ZOOM_BUCKET, file_key)
                    retry = False
                except:
                    pass

    shutil.rmtree(tile_dir, ignore_errors=True)  # Delete tile_dir before quitting