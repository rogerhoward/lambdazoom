#!/usr/bin/env python
import os, sys
import PIL.Image


#------------------------------------------------#
# S3 settings.                                   #
#------------------------------------------------#

# Set S3_ZOOM_BUCKET to bucket name where zoom files should be stored
S3_ZOOM_BUCKET = 'zoom-zoom' 


#------------------------------------------------#
# Deepzoom and PIL settings.                     #
#------------------------------------------------#

ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'tif', 'png', ]

RESIZE_FILTERS = {
    'cubic': PIL.Image.CUBIC,
    'bilinear': PIL.Image.BILINEAR,
    'bicubic': PIL.Image.BICUBIC,
    'nearest': PIL.Image.NEAREST,
    'antialias': PIL.Image.ANTIALIAS,
    }

DEEPZOOM_TILE_SIZE = 254
DEEPZOOM_TILE_FORMAT = 'jpg'
DEEPZOOM_RESIZE_FILTER = RESIZE_FILTERS['bicubic']
DEEPZOOM_IMAGE_QUALITY = 0.8


#------------------------------------------------#
# Misc settings.                                 #
#------------------------------------------------#

# Path to a writeable filesystem. Shouldn't need to change this.
TEMP_DIR = '/tmp/' 