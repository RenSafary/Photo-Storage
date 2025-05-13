from fastapi import UploadFile
import os
from dotenv import load_dotenv
from fastapi.responses import JSONResponse

from .s3_connection import connection
from .size import get_size


def upload_files(prefix: str, file_path: str, file: UploadFile, size):
    load_dotenv()

    total_size, _ = get_size(prefix)
    if (total_size + size) >= 1000:
        return JSONResponse(
            content={"status": "error", "message": "Storage is full"}, status_code=500
        )

    else:
        BUCKET_NAME = os.getenv("BUCKET_NAME")
        BUCKET = {"Name": BUCKET_NAME}

        s3 = connection()

        s3.upload_fileobj(file.file, BUCKET["Name"], file_path)
        return {"status": "success"}
