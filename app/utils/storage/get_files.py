import os
from dotenv import load_dotenv

from .s3_connection import connection

def get_files(username, folder_name):
    load_dotenv()

    BUCKET_NAME = os.getenv("BUCKET_NAME")
    BUCKET = {'Name': BUCKET_NAME}

    s3 = connection()

    objects = s3.list_objects_v2(Bucket=BUCKET['Name'], Prefix=f"{username}/{folder_name}/")
    return [
        obj['Key']
        for obj in objects.get('Contents', [])
        if not obj['Key'].endswith('/')
    ]