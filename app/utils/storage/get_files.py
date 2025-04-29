import os
from dotenv import load_dotenv

from .s3_connection import connection

def get_files():
    load_dotenv()

    BUCKET_NAME = os.getenv("BUCKET_NAME")
    BUCKET = {'Name': BUCKET_NAME}

    s3 = connection()

    for obj in s3.list_objects(Bucket=BUCKET['Name']).get('Contents', []):
        print(obj['Key'])