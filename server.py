#!/usr/bin/env python
import os
import flask
import boto3

import config


app = flask.Flask(__name__)


#------------------------------------------------#
# System status endpoints                        #
#------------------------------------------------#

@app.route('/list/')
def list():
    s3 = boto3.resource('s3')

    this_bucket = s3.Bucket(config.S3_ZOOM_BUCKET)

    keys = [x.key for x in this_bucket.objects.all()]
    return flask.jsonify({'keys': keys})


#------------------------------------------------#
#  Command line options                          #
#------------------------------------------------#

def run(workers, port, flush, debug):
    config.DEBUG = debug
    app.run(processes=3, host='0.0.0.0', port=5000, debug=config.DEBUG)


if __name__ == '__main__':
    run()
