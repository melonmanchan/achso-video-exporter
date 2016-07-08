import boto3
from botocore.client import  Config
import config as config

client = boto3.client('s3',
                      aws_secret_access_key=config.S3_SECRET_KEY,
                      aws_access_key_id=config.S3_ACCESS_KEY,
                      config=Config(signature_version='s3v4'))


def upload_file(file_to_upload, location=None):
    """
    Uploads a file to an Amazon S3 bucket.

    Args:
        file_to_upload (string): Path to the file on the filesystem that should be uploaded to the bucket.
        location (string): The path (a Key in AWS terms) where the uploaded file will end up.
                Default is the root of the bucket, with the same name as the original file.

    Returns:
        dict, string: A dictionary that represents the upload response, and the URL of the uploaded file where it can be reached at.
    """
    if location is None:
        location = file_to_upload.rsplit("/")[-1]

    data = open(file_to_upload, 'rb')
    response = client.put_object(Body=data, Bucket=config.S3_BUCKET_NAME, Key=location)
    return response, generate_url(location)


def generate_url(filename):
    """
    Generates an URL for a file in a bucket, interpreted from the filename and S3-related configuration variables

    Args:
        filename (string): The filename of the file!

    Returns:
        string: A full URL to the file (string).
    """
    return "https://s3.{0}.amazonaws.com/{1}/{2}".format(config.S3_BUCKET_REGION, config.S3_BUCKET_NAME, filename)
