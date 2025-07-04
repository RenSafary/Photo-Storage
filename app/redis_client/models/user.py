import json
from redis import RedisError
from redis_client.connection import connect
from redis_client.models import files, folders, tags
from models.Users import Users

def record_user_in_rdb(user: str):
    try:
        user = Users.get_or_none(Users.username == user)
        if not user: 
            raise ValueError(f"User '{user}' not found in database")

        rdb = connect()
        user = user.username

        files_data = files.redis_files(user)
        folders_data = folders.redis_folders(user)
        tags_data = tags.redis_tags(user)

        user_data = {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "files": files_data,
            "folders": folders_data,
            "tags": tags_data,
        }

        rdb.setex(f"user_id:{user.id}", 3600, json.dumps(user_data))
        print(f"Cached user data in Redis: user_id:{user.id}")

    except RedisError as re:
        print(f"Redis error: {re}")
    except Exception as e:
        print(f"Failed to cache user data: {e}")