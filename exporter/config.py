DEBUG = True
HOST = '0.0.0.0'
PORT = 5000

# Attempt to override defaults with custom values from a file called local_config.py

try:
    from local_config import *
except ImportError:
    pass
