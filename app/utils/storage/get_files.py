import os
from dotenv import load_dotenv
from typing import Union, List, Dict

from utils.storage.s3_connection import connection

def get_files(username: str, links: Union[str, List[str]]) -> List[Dict[str, str]]:
    load_dotenv()
    BUCKET_NAME = os.getenv("BUCKET_NAME")
    s3 = connection()
    
    files = []
    
    if isinstance(links, list):
        for link in links:
            files.extend(_get_files(s3, BUCKET_NAME, " ", link.link))
    else:
        files = _get_files(s3, BUCKET_NAME, username, links)
    
    return files

def _get_files(s3, bucket_name: str, username: str, link: str) -> List[Dict[str, str]]:
    try:
        key = str(link) if username == " " else f"{username}/{link}"
        
        objects = s3.list_objects_v2(Bucket=bucket_name, Prefix=key)
        files = []
        
        if 'Contents' in objects:
            for file in objects['Contents']:
                if not file['Key'].endswith('/'): 
                    url = s3.generate_presigned_url(
                        'get_object',
                        Params={'Bucket': bucket_name, 'Key': file['Key']},
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