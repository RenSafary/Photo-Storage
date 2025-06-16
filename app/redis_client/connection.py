from redis import Redis
import json


def connect():
    rd = Redis(host="localhost", port=6379, db=0)

    return rd

"""
rd = connect()

cached = rd.get("user_id:1")
if cached:
    user_data = json.loads(cached)  

print(user_data["username"])

for file in user_data["files"]:
    print(file["id"], file["link"])   
"""