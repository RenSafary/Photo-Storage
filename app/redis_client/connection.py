from redis import Redis
import json


def connect():
    rd = Redis(host="localhost", port=6379, db=0)

    return rd


rd = connect()

"""
cached = rd.get("user_id:1")
if cached:
    user_data = json.loads(cached)  

print(user_data["username"])

print("\nfiles\n")

for file in user_data["files"]:
    print(file["id"], file["link"], file["tag_id"], file["folder_id"])   

print("\nfolders:\n")

for folder in user_data["folders"]:
    print(folder["id"],folder["name"])

print("\ntags:\n")

for tag in user_data["tags"]:
    print(tag["id"], tag["name"])
"""