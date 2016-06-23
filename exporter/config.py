DEBUG = True
HOST = '0.0.0.0'
PORT = 5000

S3_BUCKET_NAME = 'aalto-achso-exports'
S3_BUCKET_REGION = 'eu-central-1'
S3_ACCESS_KEY = ''
S3_SECRET_KEY = ''
# Attempt to override defaults with custom values from a file called local_config.py
try:
    from local_config import *
except ImportError:
    pass
