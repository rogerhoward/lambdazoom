#!/usr/bin/env python
import os
import flask
import boto3
import config

app = flask.Flask(__name__)


#------------------------------------------------#
#  UI endpoints                                  #
#------------------------------------------------#

@app.route('/')
def index(path=None):
    """
    UI homepage.
    """
    return flask.render_template('index.html', context=config.CONTEXT)


@app.route('/browse/')
@app.route('/browse/<path:path>')
def browse(path=None):
    """
    Dual routes which support browsing a list of zoomable images on your S3 bucket,
    and viewing each one in an Open Seadragon viewer.
    """
    if path:
        return flask.render_template('zoom.html', path=path, context=config.CONTEXT)
    else:
        s3 = boto3.resource('s3')
        this_bucket = s3.Bucket(config.S3_ZOOM_BUCKET)
        zooms = [x.key.replace('.dzi', '') for x in this_bucket.objects.all() if x.key.endswith('.dzi')]

        return flask.render_template('home.html', zooms=zooms, context=config.CONTEXT)


#------------------------------------------------#
# REST endpoints                                 #
#------------------------------------------------#

@app.route('/list/')
def list():
    """
    Simple route which lists all the objects in S3_ZOOM_BUCKET
    Handy for confirming that uploads are working.
    """
    s3 = boto3.resource('s3')

    this_bucket = s3.Bucket(config.S3_ZOOM_BUCKET)

    keys = [x.key for x in this_bucket.objects.all() if x.key.endswith('.dzi')]
    return flask.jsonify({'keys': keys})


@app.route('/info/')
def info():
    """
    Route which returns all environment variables as a JSON object.
    """
    return flask.jsonify({'env': dict(os.environ)})


#------------------------------------------------#
# Supporting endpoints                           #
#------------------------------------------------#

@app.route('/static/<path:filepath>')
    """
    Route for serving static assets directly, rather than using S3.
    Used for CSS, JS and other assets needed for the application.
    """
def serve_static(filepath):
    return flask.send_from_directory(config.STATIC_ROOT, filepath)


#------------------------------------------------#
#  Command line options                          #
#------------------------------------------------#

def run():
    app.run(processes=3, host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    run()

