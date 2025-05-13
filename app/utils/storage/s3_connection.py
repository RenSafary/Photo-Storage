import boto3
from botocore.client import Config

 
def connection():    
    return boto3.client(
        's3',
        endpoint_url='https://s3.twcstorage.ru',  
        region_name='ru-1',
        aws_access_key_id='LS49TEFQWUQVYF2AAUFJ',
        aws_secret_access_key='YhP77Ys1izvMYSSsbePCBOcxCfoCrq3RHb3mv5m8',
        config=Config(
            s3={'addressing_style': 'path'},
            signature_version='s3v4', 
        )
    )