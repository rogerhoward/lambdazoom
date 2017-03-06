# LambdaZoom

LambdaZoom is a Python-based [AWS Lambda](https://aws.amazon.com/lambda/) function which converts uploaded images to the [Deep Zoom](https://en.wikipedia.org/wiki/Deep_Zoom) tiled image format supported by [OpenSeadragon](https://openseadragon.github.io/) and other zoomable image viewers.

## Why Lambda?

AWS Lambda functions allow an event-driven style of programming, and high scalable, async execution of image conversion scripts in a serverless environment. Nice jargon, but what does it mean?

### event-driven
Image conversions run in response to events - in this case, the image conversion script is automatically invoked each time an image is done uploading to an directory ("bucket") on Amazon's S3 service. This greatly simplifies our code - we don't need to sit and constantly check whether a new file has been uploaded, nor do we need to call the script from other code when uploads are complete. Amazon knows when a file is done uploading, and automatically calls the conversion script when ready.

### scalable, async execution
Each image is processed independently of another, in parallel, which means whether you have 2 or 200 images to process, the processing will take roughly the same amount of time. More traditional approachs work in serial, with each image processed only after the previous one is complete, meaning 200 images might take 100 times as long as 2. Not so with Lambdas.

### serverless environment
AWS Lambdas don't depend on being installed on a server (physical or cloud) that must be kept running 24/7, eating your dollars while it may be doing nothing. AWS Lambdas charge you only while they run, giving you a huge degree of flexibility in pricing and true pay-per-use processing, flexibility hard to match with dedicated hardware, or even with auto-provisioned cloud servers.

## Key technologies

LambdaZoom wouldn't be possible without several key technologies:

* [Zappa](http://www.zappa.io) is a Python framework which simplifies the development of Python-based serverless applications.
* [Flask](http://flask.pocoo.org/) is a - no _the_ - Python microframework.
* [deepzoom.py](https://github.com/openzoom/deepzoom.py) is a library that handles the conversion of images into DZI tilesets.
* [Open Seadragon](https://openseadragon.github.io) is an incrediable JavaScript zoom image viewer originally developed by Microsoft.

## Requirements

1. An AWS account, and [credentials properly configured for boto3](http://boto3.readthedocs.io/en/latest/guide/configuration.html)
2. Python 2.7.x (sorry, AWS Lambda doesn't support Python 3 yet)
3. Virtualenv: if you don't know what this is, I recommend [virtualenv-burrito](https://github.com/brainsik/virtualenv-burrito) to get you set. Just run the command in the "install" section on that page.

## How to install

1. Clone this repository
2. At your command line, `cd` into the local repository's directory
2. Create a new virtualenv, eg.: `mkvirtualenv lambdazoom`
3. From within the project directory, `pip install -r requirements`

## Configure zappa_settings.json

1. Create an S3 bucket for deploy/config related stuff, and put the name into `s3_bucket`. This bucket name needs to be unique, and must be writeable by the credentials you're using.
2. Create the S3 bucket you'd like to watch for new files to be processed. Set `arn` to a reference to that bucket. For instance, if the bucket name is `zoom-source` then set it to `arn:aws:s3:::zoom-source`.  This bucket name also must be unique, and must be at least readable by the credentials you're using.

## Configure config.py

1. Create an S3 bucket for where you'd like your DZI and tilesets to be stored after processing, and put the name into `S3_ZOOM_BUCKET`. This bucket name also must be unique, and must be writeable by the credentials you're using.

## Deploy

From within the local directory, and with your virtualenv activated, run `zappa deploy live` if this is the first time you've deployed, or `zappa update live` if not. Once that finishes, run `zappa schedule live` and you're done! 

Anytime you want to redeploy, just run `zappa update live` and then `zappa schedule live` from within the repo directory (and always with the virtualenv activated).

## Test

Just upload an image file into the source bucket you set in `zappa_settings.json`. Give it a few seconds, then check the destination bucket you set in `S3_ZOOM_BUCKET`. Voila!

## Browse

After you deploy, the application will print out the base URL of the Web interface, something like:

```
Your updated Zappa deployment is live!: https://xxxxxxxxx.execute-api.us-east-1.amazonaws.com/live
```

Keep that URL private, and visit it for a basic Web UI for monitoring the service, testing zoom functionality, etc.

## Problems?

Open an issue or find me on Twitter @rogerhoward and I'll try to help.