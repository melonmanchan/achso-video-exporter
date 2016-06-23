import boto3
from botocore.client import  Config
import config as config

client = boto3.client('s3',
                      aws_secret_access_key=config.S3_SECRET_KEY,
                      aws_access_key_id=config.S3_ACCESS_KEY,
                      config=Config(signature_version='s3v4'))


def upload_file(file_to_upload, location=None):
    if location is None:
        location = file_to_upload.rsplit("/")[-1]

    data = open(file_to_upload, 'rb')
    response = client.put_object(Body=data, Bucket=config.S3_BUCKET_NAME, Key=location)
    return response, generate_url(location)


def generate_url(filename):
    return "https://s3.{0}.amazonaws.com/{1}/{2}".format(config.S3_BUCKET_REGION, config.S3_BUCKET_NAME, filename)
