import os
from dotenv import load_dotenv
from fastapi.responses import JSONResponse

from .s3_connection import connection

def get_files(username, folder_name):
    load_dotenv()

    BUCKET_NAME = os.getenv("BUCKET_NAME")
    BUCKET = {'Name': BUCKET_NAME}

    s3 = connection()

    key = f"{username}/{folder_name}"
    
    try:

        objects = s3.list_objects_v2(Bucket=BUCKET['Name'], Prefix=key)

        files = []

        if 'Contents' in objects:
            for file in objects['Contents']:
                if not file['Key'].endswith('/'):
                    url = s3.generate_presigned_url(
                        'get_object',
                        Params={'Bucket': BUCKET['Name'], 'Key':file['Key']},
                        ExpiresIn=3600
                    )
                    files.append({
                        'key': file['Key'],
                        'url': url
                    })
        return files
    except Exception as e:
        print(f"Error getting files from S3: {str(e)}")
        return []