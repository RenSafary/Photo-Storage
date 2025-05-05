from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os

from utils.storage.s3_connection import connection


def delete_s3_file(file_path: str):
    load_dotenv()

    BUCKET_NAME = os.getenv('BUCKET_NAME')
    BUCKET = {'Name': BUCKET_NAME}

    s3 = connection()

    s3.delete_object(Bucket=BUCKET['Name'], Key=file_path)
    return JSONResponse(
        content="File was deleted.",
        status_code=200
    )