import json
from redis import RedisError
from redis.asyncio import Redis

from redis_client.models import files, folders
from models.Users import Users

async def record_user_in_rdb(username: str):
    rdb = None
    try:

        user = Users.get_or_none(Users.username == username)
        if not user: 
            raise ValueError(f"User '{username}' not found in database")

        rdb = await Redis.from_url("redis://localhost")

        files_data = files.redis_files(user) 
        folders_data = folders.redis_folders(user)

        user_data = {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "files": files_data,
            "folders": folders_data,
        }

        await rdb.setex(
            f"user_id:{user.id}", 
            3600, 
            json.dumps(user_data)
        )
        print(f"Cached user data in Redis: user_id:{user.id}")

    except RedisError as re:
        print(f"Redis error: {re}")
    except Exception as e:
        print(f"Failed to cache user data: {e}")
    finally: 
        if rdb:
            await rdb.close()