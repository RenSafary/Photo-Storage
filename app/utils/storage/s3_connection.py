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
 
"""print('Загрузка файла в бакет')
s3.upload_file(Filename=FILENAME, Bucket=BUCKET['Name'], Key='hello/hello1.txt')
 
print('Список объектов в бакете')
for obj in s3.list_objects(Bucket=BUCKET['Name']).get('Contents', []):
    print(obj['Key'])
 
print('Чтение файла')
data = s3.get_object(Bucket=BUCKET['Name'], Key='hello1.txt').get('Body')
if data is not None:
    print(data.read())
 
print("Скачивание файла")
s3.download_file(
    Bucket=BUCKET['Name'],
    Key='hello1.txt',
    Filename='./hello2.txt'
)"""