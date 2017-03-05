#!/usr/bin/env python
import os
import flask
import boto3
import config


app = flask.Flask(__name__)


#------------------------------------------------#
#  Browser endpoints                             #
#------------------------------------------------#

@app.route('/browse/')
@app.route('/browse/<path:path>')
def browse(path=None):
    if path:
        return flask.render_template('zoom.html', path=path, context=config.CONTEXT)
    else:
        s3 = boto3.resource('s3')
        this_bucket = s3.Bucket(config.S3_ZOOM_BUCKET)
        zooms = [x.key.replace('.dzi', '') for x in this_bucket.objects.all() if x.key.endswith('.dzi')]

        return flask.render_template('home.html', zooms=zooms, context=config.CONTEXT)

#------------------------------------------------#
# System status endpoints                        #
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


@app.route('/static/<path:filepath>')
def serve_static(filepath):
    return flask.send_from_directory(config.STATIC_ROOT, filepath)


@app.route('/info/')
def info():
    """
    Simple route which lists all the objects in S3_ZOOM_BUCKET
    Handy for confirming that uploads are working.
    """

    ENV = dict(os.environ)

    return flask.jsonify({'env': ENV})


#------------------------------------------------#
#  Command line options                          #
#------------------------------------------------#

def run():
    app.run(processes=3, host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    run()

