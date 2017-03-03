#!/usr/bin/env python
import os, sys
import boto3
import config
from deepzoom import ImageCreator

s3 = boto3.client('s3')


def to_zoom(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    base_key = '.'.join(key.split('.')[:-1])
    dzi_key = base_key + '.dzi'
    tiles_base = base_key + '_files'

    local_file = os.path.join(config.TEMP_DIR, key)
    dzi_file = os.path.join(config.TEMP_DIR, dzi_key)
    tile_dir = os.path.join(config.TEMP_DIR, tiles_base)
    new_key = os.path.relpath(dzi_file, config.TEMP_DIR)
    print(bucket, key, local_file, new_key)

    s3.download_file(bucket, key, local_file)
    creator = ImageCreator(tile_size=config.DEEPZOOM_TILE_SIZE,
                       tile_format=config.DEEPZOOM_TILE_FORMAT,
                       image_quality=config.DEEPZOOM_IMAGE_QUALITY,
                       resize_filter=config.DEEPZOOM_RESIZE_FILTER)
    creator.create(local_file, dzi_file)
    s3.upload_file(dzi_file, config.S3_ZOOM_BUCKET, new_key)

    for directory, directories, files in os.walk(tile_dir, topdown=False):
        for name in files:
            file_path = os.path.join(directory, name)
            file_key = os.path.relpath(file_path, config.TEMP_DIR)

            retry = True
            while retry:
                try:
                    s3.upload_file(file_path, config.S3_ZOOM_BUCKET, file_key)
                    retry = False
                except:
                    pass