from dotenv import load_dotenv
import os

from utils.storage.s3_connection import connection

def get_size(prefix: str):
    load_dotenv()

    BUCKET_NAME = os.getenv("BUCKET_NAME")
    BUCKET = {'Name': BUCKET_NAME}

    total_size = 0
    total_files = 0

    s3 = connection()

    paginator = s3.get_paginator('list_objects_v2')  # divide bucket by pages if there are more than 100 files
    for page in paginator.paginate(Bucket=BUCKET['Name'], Prefix=prefix):
        if 'Contents' in page:
            for obj in page['Contents']:
                total_size += obj['Size']
                total_files += 1


    total_size = round(total_size / (1024*1024))
    return total_size, total_files