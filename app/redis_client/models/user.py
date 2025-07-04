import json
from redis import RedisError

from redis_client.connection import connect
from redis_client.models import files
from redis_client.models import folders
from redis_client.models import tags

from models.Users import Users


def record_user_in_rdb(user: str):
    try:
        # user
        user = Users.get_or_none(Users.username == user)
        
        rdb = connect()
        files_data = files.redis_files(user)
        
        # folders 
        folders_data = folders.redis_folders(user)

        # tags

        tags_data = tags.redis_tags(user)

        user_data = {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "files": files_data,
            "folders": folders_data,
            "tags": tags_data,
        }
        rdb.setex(f"user_id:{user_data['id']}", 3600, json.dumps(user_data))

        print(f"User data loaded in rdb: user_id:{user.id}")
    except RedisError as re:
        print(re)
