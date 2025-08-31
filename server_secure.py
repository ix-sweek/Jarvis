#!/usr/bin/env python3
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

CERT_PATH = os.getenv('CERT_PATH', Path.home() / 'certs' / 'cert.pem')
KEY_PATH = os.getenv('KEY_PATH', Path.home() / 'certs' / 'key.pem')

# Rest des Codes...
