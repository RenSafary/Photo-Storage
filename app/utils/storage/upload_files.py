from fastapi import UploadFile
import os
from dotenv import load_dotenv

from .s3_connection import connection

def upload_files(
    file_path: str,
    file: UploadFile
):
    load_dotenv()

    BUCKET_NAME = os.getenv("BUCKET_NAME")
    BUCKET = {'Name': BUCKET_NAME}

    s3 = connection()

    s3.upload_fileobj(file.file, BUCKET['Name'], file_path)