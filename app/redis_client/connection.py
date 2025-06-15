from redis import Redis


def connect():
    rd = Redis(host="localhost", port=6379, db=0)
    return rd