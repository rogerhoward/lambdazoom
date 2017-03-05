#!/usr/bin/env python
import os, sys
import PIL.Image
import config

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


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

STATIC_ROOT = os.path.join(config.PROJECT_DIR, 'static')

ENV = dict(os.environ)

if ENV.get('STAGE'):
    URL_PREFIX = '/{}'.format(ENV.get('STAGE'))
else:
    URL_PREFIX = ''



#------------------------------------------------#
# Context dict for passing to templates          #
#------------------------------------------------#

CONTEXT = {'URL_PREFIX': URL_PREFIX, 'S3_ZOOM_BUCKET': S3_ZOOM_BUCKET}