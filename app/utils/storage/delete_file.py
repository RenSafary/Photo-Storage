from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os

from utils.storage.s3_connection import connection


def delete_s3_file(file_path: str):
    load_dotenv()

    try:
        BUCKET_NAME = os.getenv('BUCKET_NAME')
        BUCKET = {'Name': BUCKET_NAME}

        s3 = connection()

        s3.delete_object(Bucket=BUCKET['Name'], Key=file_path)
        return JSONResponse(
            status_code=200,
            content={"status":"success", "detail":"File was deleted"}
        )
    except:
        return JSONResponse(
            status_code=500,
            content={"statuc":"error", "detail":"Internal server error"}
        )